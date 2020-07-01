from resources.dcbot import botcommon
from resources.database import dbcommon
from resources.translation import transget


@botcommon.requires_perm_level(level=botcommon.key_permlevel_admin)
@botcommon.requires_channel([botcommon.key_bot_adminchannel])
async def invoke(message, arg_stack, botuser):

    async def err1():
        await message.channel.send(transget(
            "command_set_admin_channel_error_arg1",
            botuser.user_pref_lang))

    if len(arg_stack) < 2:
        await err1()
        return False
    elif not arg_stack[1].startswith("<#") or not arg_stack[1].endswith(">"):
        await err1()
        return False

    channelid = int(arg_stack[1].lstrip("<#").rstrip(">"))
    dbcommon.set_bot_setting(botcommon.key_bot_adminchannel, channelid)
    await message.add_reaction("✅")
    return True
