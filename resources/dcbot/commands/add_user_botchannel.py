from resources.dcbot import botcommon
from resources.database import dbcommon


@botcommon.requires_perm_level(level=botcommon.key_permlevel_admin)
@botcommon.requires_channel([botcommon.key_bot_adminchannel])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) is 1:
        return False
    if len(arg_stack) is 2:
        if arg_stack[1] == "help":
            # TODO: Send Help Message
            pass
        elif arg_stack[1].startswith("<#") and arg_stack[1].endswith(">"):
            new_channelid = int(arg_stack[1].lstrip("<#").rstrip(">"))
            channel_list = dbcommon.get_channel_ids_from_key(
                botcommon.key_bot_userchannel)
            channel_list.append(new_channelid)
            channel_list = list(dict.fromkeys(channel_list))
            channelstring = dbcommon.set_channelsetting_value_from_list(
                channel_list)
            dbcommon.set_bot_setting(
                botcommon.key_bot_userchannel,
                channelstring)
            return True
        else:
            return False
