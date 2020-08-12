from resources.dcbot import botcommon
from resources.database import dbcommon

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_admin,
    'required_channels': [botcommon.key_bot_adminchannel]}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
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
