from discord import PermissionOverwrite
from resources.dcbot import client
from resources.dcbot import botcommon


async def create_public(member, before, after):
    vc_category = client.get_channel(after.channel.category_id)
    new_role = await botcommon.main_guild.create_role(
        name="vc-pub-" + member.display_name)
    new_voice_channel = await botcommon.main_guild.create_voice_channel(
        name="Public by " + member.display_name,
        category=vc_category)

    default_role = botcommon.main_guild.default_role
    tc_overwrites = {
        default_role: PermissionOverwrite(read_messages=False),
        new_role: PermissionOverwrite(read_messages=True)}

    new_text_channel = await botcommon.main_guild.create_text_channel(
        name="Public by " + member.display_name,
        overwrites=tc_overwrites,
        category=vc_category)
    channel_obj = {
        'role': new_role,
        'voicechannel': new_voice_channel,
        'textchannel': new_text_channel,
        'owner': member,
        'type': "public"}
    return channel_obj


async def create_private(member, before, after):
    pass
