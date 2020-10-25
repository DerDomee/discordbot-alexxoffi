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
        if len(arg_stack[1]) == 1:
            allowed_prefixes = "!§$%&/=?.:#+*|\\"
            if not arg_stack[1] in allowed_prefixes:
                return False
            dbcommon.set_bot_setting(
                botcommon.key_bot_prefix,
                arg_stack[1])
            await _log_action(message, arg_stack, botuser)
            return True
        else:
            return False


async def _log_action(message, arg_stack, botuser):
    newprefix = dbcommon.get_bot_setting(botcommon.key_bot_prefix, '$')
    embed = Embed(
        title="New command prefix set",
        description="`" + newprefix + "` is now the new "
                    "short prefix for commands.",
        color=botcommon.key_color_warning)
    footertext = "Requested by " + str(message.author.name) + "#" \
        + str(message.author.discriminator) + " (" \
        + str(message.author.id) + ")"
    embed.set_footer(text=footertext)
    await botcommon.trytolog(message, arg_stack, botuser, embed)
