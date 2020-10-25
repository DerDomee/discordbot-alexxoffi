from src.database.models.botsettings import BotSettings
from src.database.models.botuser import BotUser
from src.database import sqlsession
from src.dcbot import botcommon
import json


def get_bot_setting(key, default=None):
    setting = sqlsession.query(BotSettings).filter_by(setting_key=key).first()
    value = default
    if setting is not None:
        value = setting.setting_value
    return value


def set_bot_setting(key, value):
    setting = sqlsession.query(BotSettings).filter_by(setting_key=key).first()
    if setting is None:
        newsetting = BotSettings(
            setting_key=key,
            setting_value=value)
        sqlsession.add(newsetting)
        sqlsession.commit()
        return
    setting.setting_value = value
    sqlsession.commit()
    return


def get_user_or_create(discordid):
    user = sqlsession.query(BotUser).filter_by(
        user_discord_id=discordid).first()
    if user is None:
        newuser = BotUser(
            user_discord_id=discordid,
            user_pref_lang="en",
            user_permission_level=botcommon.key_permlevel_user)
        sqlsession.add(newuser)
        sqlsession.commit()
        return newuser
    return user


def get_user(discordid):
    user = sqlsession.query(BotUser).filter_by(
        user_discord_id=discordid).first()
    return user


def get_channel_ids_from_key(key):
    key_value = get_bot_setting(key)
    if key == botcommon.key_bot_userchannel:
        if key_value is None:
            return []
        channel_list = json.loads(key_value)['channels']
        return channel_list

    return [key_value]


def set_channelsetting_value_from_list(channels):
    channelstring = {'channels': channels}
    return json.dumps(channelstring)
