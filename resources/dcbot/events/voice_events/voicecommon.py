from resources.dcbot import botcommon


async def move_to(member, channel_obj):
    await member.move_to(channel_obj['voicechannel'])


def get_channel_obj(channel):
    if channel is None:
        return None
    for channel_obj in botcommon.bot_voice_channels:
        if channel_obj['voicechannel'] == channel:
            return channel_obj
    return None


async def delete_channel(channel_obj):
    await channel_obj['role'].delete()
    await channel_obj['voicechannel'].delete()
    await channel_obj['textchannel'].delete()
    botcommon.bot_voice_channels.remove(channel_obj)
