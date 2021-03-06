from discord import Embed
from src.dcbot import botcommon
from src.database import dbcommon

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_admin,
    'required_channels': [botcommon.key_bot_adminchannel]}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) == 1:
        return False
    if len(arg_stack) == 2:
        if arg_stack[1].startswith("<#") and arg_stack[1].endswith(">"):
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
            await _log_action(message, arg_stack, botuser)
            return True
        else:
            return False


async def _log_action(message, arg_stack, botuser):
    embed = Embed(
        title="New user channel added",
        description="Channel " + arg_stack[1] + " was added to "
                    "command-enabled channels.",
        color=botcommon.key_color_info)
    footertext = "Requested by " + str(message.author.name) + "#" \
        + str(message.author.discriminator) + " (" \
        + str(message.author.id) + ")"
    embed.set_footer(text=footertext)
    await botcommon.trytolog(message, arg_stack, botuser, embed)
