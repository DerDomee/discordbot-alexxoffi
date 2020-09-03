import os
import json
import asyncio
from lib.hypixel import hypixel
from resources.dcbot import botcommon
from resources.translation import transget

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_user,
    'required_channels': [botcommon.key_bot_applychannel]}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    remove_messages = [message]

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

    return await _success_and_delete(remove_messages)


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
