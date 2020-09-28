from discord import Embed
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.dcbot.botcommon import trytolog

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': None}


def toggle(message, arg_stack, botuser, channel_obj):
    # Change visibility from public to private and vice-versa.
    # Double-Check if channel is renamed. When its not renamed, subsititute the
    # Word "Public" in channel name for "Private" and vice-versa.
    # Do the renaming for voice AND text channel.
    return False


def name(message, arg_stack, botuser, channel_obj):
    # Let the owner manually rename the channel.
    # Do the renaming for voice AND text channel.
    return False


def transfer(message, arg_stack, botuser, channel_obj):
    # Change the channel owner in channel_obj.
    return False


def invite(message, arg_stack, botuser, channel_obj):
    # Only when this channel is a private channel: Grant the channel's server
    # role to given member.
    return False


def kick(message, arg_stack, botuser, channel_obj):
    # Kick the given member out of the channel. If this channel is public,
    # then obviously the member can rejoin, making this command kind of
    # useless.
    # If this channel is private, also remove the channel's server role from
    # given user, so he is not able to re-join.
    return False


def close(message, arg_stack, botuser, channel_obj):
    # Instantly closes the channel, removing the voice channel, text channel
    # and the corresponding server role.
    return False


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
async def invoke(message, arg_stack, botuser):

    # Test if channel is a dynamic voice-linked text channel.
    # If it is, create a variable "channel_obj", containing the correct
    # element from 'botcommon.bot_voice_channels'.
    # If it is not a dynamic channel, return False.
    channel_obj = None

    # Test if user is the owner of the voice channel.
    # If not, return False.

    # arg_stack[1] contains subcommand 'toggle/name/transfer/invite/kick/close'
    if arg_stack[1] == 'toggle':
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
        # Print error for unknown command
