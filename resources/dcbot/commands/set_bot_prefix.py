from resources.dcbot import botcommon
from resources.database import dbcommon


@botcommon.requires_perm_level(level=botcommon.key_permlevel_admin)
@botcommon.requires_channel([botcommon.key_bot_adminchannel])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) == 1:
        return False
    if len(arg_stack) == 2:
        if arg_stack[1] == "help":
            pass
        elif len(arg_stack[1]) == 1:
            allowed_prefixes = "!§$%&/=?.:#+*|\\"
            if not arg_stack[1] in allowed_prefixes:
                return False
            dbcommon.set_bot_setting(
                botcommon.key_bot_prefix,
                arg_stack[1])
            return True
        else:
            return False
