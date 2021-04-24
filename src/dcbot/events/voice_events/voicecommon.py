from src.dcbot import botcommon
from src.database import dbcommon
from src.dcbot import client
from src.translation import transget
from discord import PermissionOverwrite
from discord import Embed


async def move_to(member, channel_obj):
    voicechannel = await client.fetch_channel(channel_obj['voicechannel'])
    await member.move_to(voicechannel)


def get_channel_obj_by_channel(channel):
    if channel is None:
        return None
    for channel_obj in botcommon.bot_voice_channels:
        if channel_obj['voicechannel'] == channel.id:
            return channel_obj
        if channel_obj['textchannel'] == channel.id:
            return channel_obj
    return None


def get_channel_obj_by_owner(member):
    if member is None:
        return None
    for channel_obj in botcommon.bot_voice_channels:
        if channel_obj['owner'] == member.id:
            return channel_obj
    return None


async def delete_channel(channel_obj):
    botcommon.bot_voice_channels.remove(channel_obj)
    role = botcommon.main_guild.get_role(channel_obj['role'])
    vc = client.get_channel(channel_obj['voicechannel'])
    tc = client.get_channel(channel_obj['textchannel'])
    await role.delete()
    await vc.delete()
    await tc.delete()


async def send_init_help(channel_obj, botuser):
    shortprefix = dbcommon.get_bot_setting(botcommon.key_bot_prefix, "$")
    tc = client.get_channel(channel_obj['textchannel'])
    embed = Embed(
        title=transget(
            "event.voice.inithelp.embed.title",
            botuser.user_pref_lang),
        description=transget(
            "event.voice.inithelp.embed.description",
            botuser.user_pref_lang),
        color=botcommon.key_color_info)
    embed.add_field(
        name='`' + shortprefix + transget(
            "command.voice.help.toggle.syntax",
            botuser.user_pref_lang) + '`',
        value=transget(
            "command.voice.help.toggle.description",
            botuser.user_pref_lang))
    embed.add_field(
        name='`' + shortprefix + transget(
            "command.voice.help.name.syntax",
            botuser.user_pref_lang) + '`',
        value=transget(
            "command.voice.help.name.description",
            botuser.user_pref_lang))
    embed.add_field(
        name='`' + shortprefix + transget(
            "command.voice.help.transfer.syntax",
            botuser.user_pref_lang) + '`',
        value=transget(
            "command.voice.help.transfer.description",
            botuser.user_pref_lang))
    embed.add_field(
        name='`' + shortprefix + transget(
            "command.voice.help.invite.syntax",
            botuser.user_pref_lang) + '`',
        value=transget(
            "command.voice.help.invite.description",
            botuser.user_pref_lang))
    embed.add_field(
        name='`' + shortprefix + transget(
            "command.voice.help.kick.syntax",
            botuser.user_pref_lang) + '`',
        value=transget(
            "command.voice.help.kick.description",
            botuser.user_pref_lang))
    embed.add_field(
        name='`' + shortprefix + transget(
            "command.voice.help.close.syntax",
            botuser.user_pref_lang) + '`',
        value=transget(
            "command.voice.help.close.description",
            botuser.user_pref_lang))
    embed.add_field(
        name=transget(
            "event.voice.inithelp.embed.more_info.title",
            botuser.user_pref_lang),
        value=transget(
            "event.voice.inithelp.embed.more_info.value",
            botuser.user_pref_lang))
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
