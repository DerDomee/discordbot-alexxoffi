from resources.dcbot import client
from resources.dcbot import botcommon
from resources.dcbot.events.voice_events import new_voice
from resources.dcbot.events.voice_events import voicecommon


@client.event
async def on_voice_state_update(member, before, after):
    # Should create a new public channel
    if after.channel is not None and after.channel.id == 679801626747469960:
        channel_obj = await new_voice.create_public(member, before, after)
        botcommon.bot_voice_channels.append(channel_obj)
        try:
            await voicecommon.move_to(member, channel_obj)
        except Exception:
            await voicecommon.delete_channel(channel_obj)
    # Should create a new private channel
    if after.channel is not None and after.channel.id == 759136424661876766:
        channel_obj = await new_voice.create_private(member, before, after)
        botcommon.bot_voice_channels.append(channel_obj)
        try:
            await voicecommon.move_to(member, channel_obj)
        except Exception:
            await voicecommon.delete_channel(channel_obj)

    # Check if old channel is dynamic
    if voicecommon.get_channel_obj(before.channel) is not None:
        channel_obj = voicecommon.get_channel_obj(before.channel)
        await member.remove_roles(channel_obj['role'])
        # Remove channel if it is empty now
        if len(channel_obj['voicechannel'].members) is 0:
            await voicecommon.delete_channel(channel_obj)

    # Check if new channel is dynamic
    if voicecommon.get_channel_obj(after.channel) is not None:
        channel_obj = voicecommon.get_channel_obj(after.channel)
        await member.add_roles(channel_obj['role'])
