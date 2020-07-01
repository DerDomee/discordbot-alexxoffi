from resources.database import dbcommon
import json


def requires_permission_level(botuser, permission_level):
    if botuser.user_permission_level < permission_level:
        return false
    return true


def requires_channel(current_channel, channel_key_list):
    requirement_fullfilled = False

    for key in channel_key_list:
        channels_raw_json = dbcommon.get_bot_setting(channel_key_list, None)
        if channels_raw_json is not None:
            channel_list = json.loads(channels)
            for channel in channel_list['channels']:
                if current_channel is channel:
                    requirement_fullfilled = True
    return requirement_fullfilled
