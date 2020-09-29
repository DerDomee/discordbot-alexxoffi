from discord import Embed
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.dcbot.events.voice_events import voicecommon

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': None}


async def toggle(message, arg_stack, botuser, channel_obj):
    # Maybe this whole "channel updating" process lets me run into a rate limit
    # and maybe I can fix this with setting a "last_updated" field in
    # channel_obj and only allow new updates like every two minutes?
    if channel_obj['type'] == "public":
        print("Toggling from public to private channel")
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
        new_channel_obj = channel_obj.copy()
        print(new_channel_obj)
        botcommon.bot_voice_channels.remove(channel_obj)
        botcommon.bot_voice_channels.append(new_channel_obj)
        return True
    else:
        print("Toggling from private to public channel")
        role = botcommon.main_guild.get_role(channel_obj['role'])
        overwrites = voicecommon.get_public_overwrites(role)
        vc = client.get_channel(channel_obj['voicechannel'])
        tc = message.channel
        print("Role, Channels and Overwrites initialized")
        await role.edit(name="vc-pub-" + message.author.display_name)
        print("Role updated.")
        if channel_obj['renamed'] is False:
            print("Channel Update with additional renaming...")
            await vc.edit(
                name="Public by " + message.author.display_name,
                overwrites=overwrites['vc'])
            await tc.edit(
                name="Public by " + message.author.display_name,
                overwrites=overwrites['tc'])
            print("...finished!")
        else:
            print("Channel update without renaming...")
            await vc.edit(overwrites=overwrites['vc'])
            await tc.edit(overwrites=overwrites['tc'])
            print("...finished!")
        print("The API-sided part of toggling is finished.")
        channel_obj['type'] = "public"
        new_channel_obj = channel_obj.copy()
        print(new_channel_obj)
        botcommon.bot_voice_channels.remove(channel_obj)
        botcommon.bot_voice_channels.append(new_channel_obj)
        return True
    return False


async def name(message, arg_stack, botuser, channel_obj):
    # Let the owner manually rename the channel.
    # Do the renaming for voice AND text channel.
    return False


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
    channel_obj = voicecommon.get_channel_obj(message.channel)
    if channel_obj is None:
        return False

    if message.author.id != channel_obj['owner']:
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
