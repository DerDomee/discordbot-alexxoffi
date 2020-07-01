import functools


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
default_user_preferred_language = "en"


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
            # TODO: create decorator logic
            return await func(*args, **kwargs)
        return decorated
    return decorator
