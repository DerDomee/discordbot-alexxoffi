from discord import PermissionOverwrite
from src.dcbot import client
from src.dcbot import botcommon
from src.dcbot.events.voice_events import voicecommon


async def create_public(member, before, after):
    vc_category = client.get_channel(after.channel.category_id)
    new_role = await botcommon.main_guild.create_role(
        name="vc-pub-" + member.display_name)

    overwrites = voicecommon.get_public_overwrites(new_role)

    new_voice_channel = await botcommon.main_guild.create_voice_channel(
        name="Public by " + member.display_name,
        overwrites=overwrites['vc'],
        category=vc_category)

    new_text_channel = await botcommon.main_guild.create_text_channel(
        name="Public by " + member.display_name,
        overwrites=overwrites['tc'],
        category=vc_category)
    channel_obj = {
        'role': new_role.id,
        'voicechannel': new_voice_channel.id,
        'textchannel': new_text_channel.id,
        'owner': member.id,
        'type': "public",
        'renamed': False,
        'editcount': 0}

    # Send a initializing message in new_text_channel with
    # some help for voice commands.

    return channel_obj


async def create_private(member, before, after):
    vc_category = client.get_channel(after.channel.category_id)
    new_role = await botcommon.main_guild.create_role(
        name="vc-prv-" + member.display_name)

    overwrites = voicecommon.get_private_overwrites(new_role)
    new_voice_channel = await botcommon.main_guild.create_voice_channel(
        name="Private by " + member.display_name,
        category=vc_category,
        overwrites=overwrites['vc'])
    new_text_channel = await botcommon.main_guild.create_text_channel(
        name="Private by " + member.display_name,
        overwrites=overwrites['tc'],
        category=vc_category)
    channel_obj = {
        'role': new_role.id,
        'voicechannel': new_voice_channel.id,
        'textchannel': new_text_channel.id,
        'owner': member.id,
        'type': "private",
        'renamed': False,
        'editcount': 0}

    # Send a initializing message in new_text_channel with
    # some help for voice commands.

    return channel_obj
