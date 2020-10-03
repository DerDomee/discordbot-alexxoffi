from resources.dcbot import botcommon
from resources.dcbot import client
from discord import PermissionOverwrite
from discord import Embed


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
    role = botcommon.main_guild.get_role(channel_obj['role'])
    vc = client.get_channel(channel_obj['voicechannel'])
    tc = client.get_channel(channel_obj['textchannel'])
    await role.delete()
    await vc.delete()
    await tc.delete()
    botcommon.bot_voice_channels.remove(channel_obj)


async def send_init_help(channel_obj):
    tc = client.get_channel(channel_obj['textchannel'])
    embed = Embed(
        title="Welcome to your voice channel!",
        description=("You can use following commands in this channel only:"),
        color=botcommon.key_color_info)
    embed.add_field(
        name="`voice toggle`",
        value="Toggle the channel visibility between public and private. "
              + "**This edits the channel.**")
    embed.add_field(
        name="`voice name <new-name>`",
        value="Set a custom name for the channel. Names are limited to 20 "
              + "alphanumeric characters. **This edits the channel.**")
    embed.add_field(
        name="`voice transfer <user-ping|user-id>`",
        value="Transfer the channel ownership to another user, that must be "
              + "currently connected to this channel.")
    embed.add_field(
        name="`voice invite <user-ping|user-id>`",
        value="**Only private channels**: Make this channel visible for a "
              + "specified user. You can use this command in every channel "
              + "on this server.")
    embed.add_field(
        name="`voice kick <user-ping|user-id>`",
        value="**Only private channels**: Kick a user and make this channel "
              + "invisible for him again.")
    embed.add_field(
        name="`voice close`",
        value="Manually delete this channel. ")
    embed.add_field(
        name="\nMore information",
        inline=False,
        value="**1.** If the owner leaves without transferring ownership, "
              + "a new owner is randomly chosen.\n"
              + "**2.** As soon as the channel is empty, it is removed.\n"
              + "**3.** When a user disconnects from a private channel, he "
              + "still can see the channel and reconnect. To prevent "
              + "reconnecting, the owner must manually kick the user.\n\n"
              + "**4.** You can use 'channel editing' commands **up to 2 "
              + "times altogether** due to anti-spam.")
    await tc.send(embed=embed)


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
