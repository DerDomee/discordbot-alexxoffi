import re
from discord import Embed
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.dcbot.events.voice_events import voicecommon

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': None}


async def toggle(message, arg_stack, botuser, channel_obj):
    if channel_obj['editcount'] >= 2:
        await message.channel.send(
            "You can not edit this channel more than 2 times due to "
            "anti-spam.")
        return False

    if channel_obj['type'] == "public":
        channel_obj['editcount'] += 1
        role = botcommon.main_guild.get_role(channel_obj['role'])
        overwrites = voicecommon.get_private_overwrites(role)
        vc = client.get_channel(channel_obj['voicechannel'])
        tc = message.channel
        await vc.edit(overwrites=overwrites['vc'])
        await tc.edit(overwrites=overwrites['tc'])
        await role.edit(name="vc-prv-" + message.author.display_name)
        if channel_obj['renamed'] is False:
            await vc.edit(name="Private by " + message.author.display_name)
            await tc.edit(name="Private by " + message.author.display_name)
        channel_obj['type'] = "private"
        await message.channel.send(
            "You successfully changed the visiblity from public to private.\n"
            + "This channel was edited " + str(channel_obj['editcount']) + " "
            + "times now, so you have " + str(2 - channel_obj['editcount'])
            + " edits left.")
        return True
    else:
        channel_obj['editcount'] += 1
        role = botcommon.main_guild.get_role(channel_obj['role'])
        overwrites = voicecommon.get_public_overwrites(role)
        vc = client.get_channel(channel_obj['voicechannel'])
        tc = message.channel
        await role.edit(name="vc-pub-" + message.author.display_name)
        if channel_obj['renamed'] is False:
            await vc.edit(
                name="Public by " + message.author.display_name,
                overwrites=overwrites['vc'])
            await tc.edit(
                name="Public by " + message.author.display_name,
                overwrites=overwrites['tc'])
        else:
            await vc.edit(overwrites=overwrites['vc'])
            await tc.edit(overwrites=overwrites['tc'])
        channel_obj['type'] = "public"
        await message.channel.send(
            "You successfully changed the visiblity from private to public.\n"
            + "This channel was edited " + str(channel_obj['editcount']) + " "
            + "times now, so you have " + str(2 - channel_obj['editcount'])
            + " edits left.")
        return True
    return False


async def name(message, arg_stack, botuser, channel_obj):
    if channel_obj['editcount'] >= 2:
        await message.channel.send(
            "You can not edit this channel more than 2 times due to "
            "anti-spam.")
        return False

    if len(arg_stack) <= 2:
        await message.channel.send("You must specify the desired name.")

    new_name = " ".join(arg_stack[2:])
    new_name = re.sub('[^A-Za-z1-9\\s\\-]', '', new_name)
    new_name = (new_name[:20]) if len(new_name) > 20 else new_name
    tc = client.get_channel(channel_obj['textchannel'])
    vc = client.get_channel(channel_obj['voicechannel'])

    await tc.edit(name=new_name)
    await vc.edit(name=new_name)

    channel_obj['editcount'] += 1
    channel_obj['renamed'] = True

    await message.channel.send(
        "You successfully changed the channel name to " + str(new_name) + ".\n"
        + "This channel was edited " + str(channel_obj['editcount']) + " "
        + "times now, so you have " + str(2 - channel_obj['editcount'])
        + " edits left.")


async def transfer(message, arg_stack, botuser, channel_obj):
    # Change the channel owner in channel_obj.
    return False


async def invite(message, arg_stack, botuser, channel_obj):
    # Only when this channel is a private channel: Grant the channel's server
    # role to given member.
    return False


async def kick(message, arg_stack, botuser, channel_obj):
    # Kick the given member out of the channel. If this channel is public,
    # then obviously the member can rejoin, making this command kind of
    # useless.
    # If this channel is private, also remove the channel's server role from
    # given user, so he is not able to re-join.
    return False


async def close(message, arg_stack, botuser, channel_obj):
    # Instantly closes the channel, removing the voice channel, text channel
    # and the corresponding server role.
    return False


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
async def invoke(message, arg_stack, botuser):

    channel_obj = voicecommon.get_channel_by_owner(message.author.id)
    if channel_obj is None:
        return False

    # arg_stack[1] contains subcommand 'toggle/name/transfer/invite/kick/close'
    if len(arg_stack) <= 1:
        return False
    elif arg_stack[1] == 'toggle':
        return await toggle(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'name':
        return await name(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'transfer':
        return await transfer(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'invite':
        return await invite(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'kick':
        return await kick(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'close':
        return await close(message, arg_stack, botuser, channel_obj)
    else:
        pass
        # Print error for unknown command
