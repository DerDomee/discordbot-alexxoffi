from src.dcbot import client
from src.dcbot import botcommon
from src.database import dbcommon
from src.dcbot.events.voice_events import new_voice
from src.dcbot.events.voice_events import voicecommon


@client.event
async def on_voice_state_update(member, before, after):

    # If bot is currently shutting down, don't do anything at all.
    if botcommon.is_bot_stopping:
        return

    botuser = dbcommon.get_user_or_create(member.id)

    cid_new_publicvoice = int(dbcommon.get_bot_setting(
        botcommon.key_bot_newpublicvoicechannel))
    cid_new_privatevoice = int(dbcommon.get_bot_setting(
        botcommon.key_bot_newprivatevoicechannel))

    if botcommon.is_bot_stopping is True:
        return

    # When new channel is the "Create new Public Talk" channel
    if after.channel is not None and after.channel.id == cid_new_publicvoice:
        channel_obj = await new_voice.create_public(member, before, after)
        botcommon.bot_voice_channels.append(channel_obj)
        try:
            await voicecommon.move_to(member, channel_obj)
        except Exception:
            await voicecommon.delete_channel(channel_obj)
        await voicecommon.send_init_help(channel_obj, botuser)

    # When new channel is the "Create new Private Talk" channel
    if after.channel is not None and after.channel.id == cid_new_privatevoice:
        channel_obj = await new_voice.create_private(member, before, after)
        botcommon.bot_voice_channels.append(channel_obj)
        role = botcommon.main_guild.get_role(channel_obj['role'])
        await member.add_roles(role)
        try:
            await voicecommon.move_to(member, channel_obj)
        except Exception:
            await voicecommon.delete_channel(channel_obj)
        await voicecommon.send_init_help(channel_obj, botuser)

    # When old channel is dynamic
    if voicecommon.get_channel_obj_by_channel(before.channel) is not None:
        channel_obj = voicecommon.get_channel_obj_by_channel(before.channel)
        if channel_obj['type'] == "public":
            # Only take away role when channel is public.
            # Roles for private channels are taken away by commands only.
            role = botcommon.main_guild.get_role(channel_obj['role'])
            await member.remove_roles(role)
        # Remove channel if it is empty now
        vc = await client.fetch_channel(channel_obj['voicechannel'])
        if len(vc.members) == 0:
            await voicecommon.delete_channel(channel_obj)

    # Check if new channel is dynamic
    if voicecommon.get_channel_obj_by_channel(after.channel) is not None:
        channel_obj = voicecommon.get_channel_obj_by_channel(after.channel)
        if channel_obj['type'] == "public":
            # Only give role when channel is public.
            # Roles for private channels are given by commands only.
            role = botcommon.main_guild.get_role(channel_obj['role'])
            await member.add_roles(role)
