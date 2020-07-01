from resources.dcbot import botcommon


@botcommon.requires_perm_level(level=botcommon.key_permlevel_owner)
@botcommon.requires_channel([botcommon.key_bot_adminchannel])
async def invoke(message, arg_stack, botuser):
    print("Print from inside the stop function")
