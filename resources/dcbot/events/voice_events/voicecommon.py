from resources.dcbot import botcommon
from resources.dcbot import client
from discord import PermissionOverwrite


async def move_to(member, channel_obj):
    voicechannel = await client.fetch_channel(channel_obj['voicechannel'])
    await member.move_to(voicechannel)


def get_channel_obj(channel):
    if channel is None:
        return None
    for channel_obj in botcommon.bot_voice_channels:
        if channel_obj['voicechannel'] == channel.id:
            return channel_obj
        if channel_obj['textchannel'] == channel.id:
            return channel_obj
    return None


async def delete_channel(channel_obj):
    print("Init deletion")
    role = botcommon.main_guild.get_role(channel_obj['role'])
    vc = await client.fetch_channel(channel_obj['voicechannel'])
    tc = await client.fetch_channel(channel_obj['textchannel'])
    print("Role and Channels initialized. Deleting now...")
    await role.delete()
    await vc.delete()
    await tc.delete()
    print("API-sided calls are finished. Deletion successful")
    botcommon.bot_voice_channels.remove(channel_obj)
    print("Internal deletion successful")


def get_public_overwrites(specific_role):
    vc_overwrites = {
        botcommon.main_guild.default_role: PermissionOverwrite(
            view_channel=True),
        specific_role: PermissionOverwrite(
            view_channel=True)}
    tc_overwrites = {
        botcommon.main_guild.default_role: PermissionOverwrite(
            read_messages=False),
        specific_role: PermissionOverwrite(
            read_messages=True)}
    retval = {
        'vc': vc_overwrites,
        'tc': tc_overwrites}
    return retval


def get_private_overwrites(specific_role):
    vc_overwrites = {
        botcommon.main_guild.default_role: PermissionOverwrite(
            view_channel=False),
        specific_role: PermissionOverwrite(
            view_channel=True)}
    tc_overwrites = {
        botcommon.main_guild.default_role: PermissionOverwrite(
            read_messages=False),
        specific_role: PermissionOverwrite(
            read_messages=True)}
    retval = {
        'vc': vc_overwrites,
        'tc': tc_overwrites}
    return retval
