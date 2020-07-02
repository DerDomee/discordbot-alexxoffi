from resources.dcbot import botcommon
from resources.dcbot import client


@botcommon.requires_perm_level(level=botcommon.key_permlevel_owner)
@botcommon.requires_channel([botcommon.key_bot_adminchannel])
async def invoke(message, arg_stack, botuser):
    await client.logout()
    return True
