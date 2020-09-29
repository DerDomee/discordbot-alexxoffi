import functools
from resources.database import dbcommon
from resources.dcbot import client
from resources.translation import transget

# Server Keys
key_bot_mainserver = "bot_main_server"

# Singlechannel keys
key_bot_adminchannel = "bot_admin_channel"
key_bot_logchannel = "bot_log_channel"
key_bot_applychannel = "bot_gapply_channel"
key_bot_applydestchannel = "bot_gapplydest_channel"
key_bot_splashchannel = "bot_gsplash_channel"

# Multichannel keys
key_bot_userchannel = "bot_user_botchannel"

# Permission keys
key_permlevel_fullmuted = -10
key_permlevel_restricted = -1
key_permlevel_user = 0
key_permlevel_elevated = 1
key_permlevel_moderator = 10
key_permlevel_supermod = 50
key_permlevel_admin = 90
key_permlevel_owner = 100

# More bot settings keys
key_bot_init_stage = "bot_init_stage"
key_bot_prefix = "bot_shortprefix"
default_user_preferred_language = "en"

key_color_info = 0xDEDEDE
key_color_muted = 0x2E2E2E
key_color_okay = 0x7DDE4D
key_color_warning = 0xEFA43D
key_color_danger = 0xEF3D3D

# Common quick-access variables for the bot, may be None if not initialized yet
main_guild = None

# Voice channel object:
bot_voice_channels = []

# Currently registered commands
registered_bot_commands = []
# Currently registered message processors
registered_message_processors = []

# Is the bot currently shutting down? This is used for disabling events
# while cleaning up the server and is set from inside the 'stop' command
is_bot_stopping = False


# Decorator for permission constraints on commands
def requires_perm_level(level):

    def decorator(func):
        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            if args[2].user_permission_level >= level:
                return await func(*args, **kwargs)
            else:
                return None
        return decorated
    return decorator


# Decorator for channel constraints on commands
def requires_channel(channel_key_list):
    def decorator(func):
        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            full_channel_list = []
            for channel_key in channel_key_list:
                channels = dbcommon.get_channel_ids_from_key(channel_key)
                full_channel_list = full_channel_list + channels
            full_channel_list = list(dict.fromkeys(full_channel_list))
            if full_channel_list == [None] or full_channel_list == [] or \
                    full_channel_list is None:
                return await func(*args, **kwargs)
            full_channel_list = [int(x) for x in full_channel_list]
            if args[0].channel.id in full_channel_list:
                return await func(*args, **kwargs)
        return decorated
    return decorator


async def trytolog(message, arg_stack, botuser, embed):
    logchannel_id = dbcommon.get_bot_setting(key_bot_logchannel, 0)
    try:
        logchannel = await client.fetch_channel(logchannel_id)
    except Exception:
        await message.channel.send(
            transget('dcbot.log.error.channel', botuser.user_pref_lang))
        await message.channel.send(embed=embed)
        return
    else:
        if logchannel is None:
            await message.channel.send(
                transget('dcbot.log.error.channel', botuser.user_pref_lang))
            await message.channel.send(embed=embed)
            return
        else:
            await logchannel.send(embed=embed)
            return
