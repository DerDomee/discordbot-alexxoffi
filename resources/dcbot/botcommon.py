import functools
from resources.database import dbcommon

# Server Keys
key_bot_mainserver = "bot_main_server"

# Channel Keys
key_bot_adminchannel = "bot_admin_channel"
key_bot_userchannel = "bot_user_botchannel"
key_bot_logchannel = "bot_log_channel"

# Permission keys
key_permlevel_fullmuted = -10
key_permlevel_restricted = -1
key_permlevel_user = 0
key_permlevel_elevated = 1
key_permlevel_moderator = 10
key_permlevel_admin = 50
key_permlevel_owner = 100

# More bot settings keys
key_bot_init_stage = "bot_init_stage"
key_bot_prefix = "bot_shortprefix"
default_user_preferred_language = "en"

registered_bot_commands = []


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


# Implement trytolog: try to get log channel. If it is available, post *embed
# in log channel. If it is not available, post *embed in *message.channel
def trytolog(message, arg_stack, botuser, embed):
    mainserver = dbcommon.get_bot_setting(key_bot_mainserver)
    botchannel = dbcommon.get_bot_setting(key_bot_logchannel)
    pass
