import os
import json
import asyncio
import requests
from lib.hgg import hgg
from lib.hypixel import hypixel
from resources.dcbot import client
from resources.dcbot import botcommon
from resources.database import dbcommon
from resources.translation import transget
from discord import Embed

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_user,
    'required_channels': [botcommon.key_bot_applychannel]}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    remove_messages = [message]
    metadata = {
        'discord_id': message.author.id}

    if len(arg_stack) == 2 and arg_stack[1] == "on" and \
            botuser.user_permission_level >= botcommon.key_permlevel_moderator:
        # TODO: Check if apply command actually can be enabled!
        #       Key bot_gapplydest_channel must be properly set and available!
        dbcommon.set_bot_setting("bot_gapply_enabled", "true")
        # TODO: Log the changing apply state
        return await _success_and_delete(remove_messages)
    if len(arg_stack) == 2 and arg_stack[1] == "off" and \
            botuser.user_permission_level >= botcommon.key_permlevel_moderator:
        dbcommon.set_bot_setting("bot_gapply_enabled", "false")
        # TODO: Log the changing apply state
        return await _success_and_delete(remove_messages)

    if dbcommon.get_bot_setting(
            "bot_gapply_enabled", default="false") == "false":
        remove_messages.append(await message.channel.send(transget(
            'command.apply.err.disabled',
            botuser.user_pref_lang)))
        return await _error_and_delete(remove_messages)

    # Check if command contains no argument (stack size 1)
    # This means no player name was provided
    if len(arg_stack) == 1:

        remove_messages.append(await message.channel.send(transget(
            'command.apply.err.noname',
            botuser.user_pref_lang)))
        return await _error_and_delete(remove_messages)

    # Check if command contains only one argument (stack size 2)
    # This means no profile name was provided
    if len(arg_stack) == 2:
        remove_messages.append(await message.channel.send(transget(
            'command.apply.err.noprofile',
            botuser.user_pref_lang)))
        return await _error_and_delete(remove_messages)

    # Get the player from the Hypixel API
    hypixelplayer = hypixel.getplayer_by_name(arg_stack[1])
    player_uuid = hypixelplayer['player']['uuid']

    metadata['mc_username'] = arg_stack[1]
    metadata['mc_uuid'] = player_uuid

    # Get a personal applicant message, if provided in command
    private_message = None
    if len(arg_stack) > 2:
        private_message = " ".join(arg_stack[3:])

    metadata['private_message'] = private_message

    # Check if the player actually exists
    if hypixelplayer['player'] is None:
        remove_messages.append(await message.channel.send(transget(
            'command.apply.err.playernotfound',
            botuser.user_pref_lang).format(
                playername=arg_stack[1])))
        return await _error_and_delete(remove_messages)

    # Build the Socialtag for the applying discord user
    actual_dc_tag = message.author.name + "#" + message.author.discriminator

    # Check if the player has linked a discord profile
    if ('socialMedia' not in hypixelplayer['player']) or \
            ('DISCORD' not in
             hypixelplayer['player']['socialMedia']['links']):
        remove_messages.append(await message.channel.send(transget(
            'command.apply.err.playernotlinked',
            botuser.user_pref_lang).format(
                actual_dc_tag=actual_dc_tag
            )))
        return await _error_and_delete(remove_messages)

    # Get the Socialtag the player provided in the Hypixel API
    api_dc_tag = hypixelplayer['player']['socialMedia']['links']['DISCORD']

    # Check if the player has linked actually his own discord profile
    if api_dc_tag != actual_dc_tag:
        remove_messages.append(await message.channel.send(transget(
            'command.apply.err.playerwronglinked',
            botuser.user_pref_lang).format(
                api_dc_tag=api_dc_tag,
                actual_dc_tag=actual_dc_tag)))
        return await _error_and_delete(remove_messages)

    # Check if provided Profile name actually exists
    profile_uuid = None
    for profile in \
            hypixelplayer['player']['stats']['SkyBlock']['profiles'].values():
        if profile['cute_name'].lower() == arg_stack[2].lower():
            profile_uuid = profile['profile_id']

    if profile_uuid is None:
        remove_messages.append(await message.channel.send(transget(
            'command.apply.err.profilenotfound',
            botuser.user_pref_lang).format(
                profile=arg_stack[2])))
        return await _error_and_delete(remove_messages)

    metadata['profile_name'] = arg_stack[2]
    metadata['profile_uuid'] = profile_uuid
    # Gather profile stats to show if current requirements are met
    profile_data = None
    try:
        profile_data = _get_profile_data(metadata)
    except Exception:
        profile_data = None

    if profile_data is not None:
        metadata['pdata_err'] = False
        metadata['slayer_xp'] = profile_data['data']['slayer_xp']
        metadata['skill_avg'] = profile_data['data']['average_level']
        metadata['alchemy_lvl'] = \
            profile_data['data']['levels']['alchemy']['level']
        metadata['fairy_souls'] = \
            profile_data['data']['fairy_souls']['collected']
    else:
        metadata['pdata_err'] = True

    # Check for HGG Entries
    try:
        hgg_check = hgg.check_hgg_by_uuid(player_uuid)
    except Exception:
        hgg_check = "Error"
    if hgg_check == "Error":
        metadata['hgg_report_count'] = "Error"
    elif hgg_check['found'] is False:
        metadata['hgg_report_count'] = 0
    else:
        metadata['hgg_report_count'] = len(hgg_check['user']['reports'])

    embed = _create_embed(metadata)
    if await _send_application(embed) is False:
        remove_messages.append(await message.channel.send(transget(
            'command.apply.err.sendfailure',
            botuser.user_pref_lang).format(
                playername=arg_stack[1])))
        return await _error_and_delete(remove_messages)
    return await _success_and_delete(remove_messages)


def _get_profile_data(metadata):
    tempdata = None
    try:
        req = requests.get(
            'https://sky.derdom.ee/api/v2/profile/' + metadata['mc_uuid'])
        tempdata = json.loads(req.text)
    except requests.ConnectionError:
        return None
    if 'error' in tempdata:
        requests.get(
            'https://sky.derdom.ee/stats/' + metadata['mc_username'])
        try:
            req = requests.get(
                'https://sky.derdom.ee/api/v2/profile/'
                + metadata['mc_uuid'])
            tempdata = json.loads(req.text)
        except requests.ConnectionError:
            return None
        tempdata = json.loads(req.text)
    if 'error' in tempdata:
        return None
    else:
        return tempdata['profiles'][metadata['profile_uuid']]


def _create_embed(metadata):
    embed = Embed(
        title="Neue Gildenbewerbung",
        color=botcommon.key_color_okay)
    embed.add_field(
        name="Ingame-Name",
        value=metadata['mc_username'],
        inline=True)
    embed.add_field(
        name="Discord Member",
        value="<@" + str(metadata['discord_id']) + ">",
        inline=True)
    embed.add_field(
        name="HGG Reports",
        value=metadata['hgg_report_count'],
        inline=True)
    embed.add_field(
        name="Profile",
        value=metadata['profile_name'] + " (" + metadata['profile_uuid'] + ")",
        inline=False)
    if 'pdata_err' in metadata and metadata['pdata_err'] is False:
        embed.add_field(
            name="Skill Average",
            value="{:.2f}".format(metadata['skill_avg']),
            inline=True)
        embed.add_field(
            name="Total Slayer XP",
            value=metadata['slayer_xp'],
            inline=True)
        embed.add_field(
            name="Fairy Souls",
            value=metadata['fairy_souls'],
            inline=True)
        embed.add_field(
            name="Alchemy Level",
            value=metadata['alchemy_lvl'],
            inline=True)
    else:
        embed.add_field(
            name="Profile Data Error",
            value="Unknown Error while retrieving Profile data.",
            inline=True)
    embed.add_field(
        name="Stats Viewer Link",
        value="https://sky.derdom.ee/stats/" + metadata['mc_username'] + "/"
              + metadata['profile_name'],
        inline=False)
    if metadata['private_message'] is not None \
            and metadata['private_message'] != "":
        embed.add_field(
            name="Angehängte Nachricht",
            value=metadata['private_message'],
            inline=False)
        pass
    return embed


async def _send_application(embed):
    destchannel_id = dbcommon.get_bot_setting(
        botcommon.key_bot_applydestchannel, 0)
    try:
        destchannel = await client.fetch_channel(destchannel_id)
    except Exception:
        return False
    else:
        if destchannel is None:
            return False
        else:
            message = await destchannel.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            return True


async def _error_and_delete(remove_messages):
    await remove_messages[0].add_reaction("❌")
    await asyncio.sleep(10)
    for message in remove_messages:
        await message.delete()
    return False


async def _success_and_delete(remove_messages):
    await remove_messages[0].add_reaction("✅")
    await asyncio.sleep(5)
    for message in remove_messages:
        await message.delete()
    return True
