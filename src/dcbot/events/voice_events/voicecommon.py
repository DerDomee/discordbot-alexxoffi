from src.dcbot import botcommon
from src.dcbot import client
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


async def send_init_help(channel_obj):
    tc = client.get_channel(channel_obj['textchannel'])
    embed = Embed(
        title="Willkommen in deinem Voice Channel!",
        description=("Diese Commands kannst du in diesem Channel nutzen:"),
        color=botcommon.key_color_info)
    embed.add_field(
        name="`voice toggle`",
        value="Ändert die Sichtbarkeit des Channels zwischen Privat und Öffentlich."
              + "**Das verändert den Kanal.**")
    embed.add_field(
        name="`voice name <new-name>`",
        value="Verändert den Namen eines Channels | Maximal 20 Zeichen. | "
              + "Nur Alphanumerische Zeichen **Das verändert den Kanal.**")
    embed.add_field(
        name="`voice transfer <user-ping|user-id>`",
        value="Überträgt den Channelbesitz an einen anderen User. "
              + "Der Nutzer muss im Channel sein.")
    embed.add_field(
        name="`voice invite <user-ping|user-id>`",
        value="**Nur möglich in privaten Channelss**: Macht den Channel für einen "
              + "bestimmten User sichtbar. Dieser Command kann überall auf dem "
              + "Server benutzt werden.")
    embed.add_field(
        name="`voice kick <user-ping|user-id>`",
        value="**Nur möglich in privaten Channels**:  Kickt einen bestimmten User aus dem Channel "
              + "und macht ihn wieder unsichtbar.")
    embed.add_field(
        name="`voice close`",
        value="Schließt manuell den Channel. (Man kann auch einfach aus dem Channel raus gehen.)")
    embed.add_field(
        name="\nMehr Informationen:",
        inline=False,
        value="**1.** Wenn der Besitzer des Channels aus dem Channel geht wird "
              + "ein neuer Besitzer zufällig ausgewählt.\n"
              + "**2.** Wenn der Channel leer ist wird er automatisch gelöscht.\n"
              + "**3.** Wenn ein User aus dem Channel geht, kann "
              + "er ihn noch immer sehen und ihn betreten. Um dies "
              + "zu verhindern, muss der Besitzer ihn manuell kicken.\n\n"
              + "**4.** Um Spam zuverhindern kannst du bestimmte Commands"
              + "2mal benutzen.")
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
