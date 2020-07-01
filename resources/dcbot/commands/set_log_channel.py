from resources.dcbot import botcommon


@botcommon.requires_perm_level(level=botcommon.key_permlevel_admin)
@botcommon.requires_channel([botcommon.key_bot_adminchannel])
async def invoke(message, arg_stack, botuser):
    print("##################################")
    print("# CAUTION! UNIMPLEMENTED FUNCTION!")
    print("##################################")
    return True
