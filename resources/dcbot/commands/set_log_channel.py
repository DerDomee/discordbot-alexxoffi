from discord import Embed
from resources.dcbot import botcommon
from resources.database import dbcommon

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_admin,
    'required_channels': [botcommon.key_bot_adminchannel]}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
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
    dbcommon.set_bot_setting(botcommon.key_bot_logchannel, channelid)
    await message.add_reaction("✅")
    await _log_action(message, arg_stack, botuser)
    return True


async def _log_action(message, arg_stack, botuser):
    embed = Embed(
        title="New log channel set",
        description="Channel " + arg_stack[1] + " is now the new "
                    "log channel for bot actions."
                    "This old channel will go quiet now.",
        color=botcommon.key_color_warning)
    footertext = "Requested by " + str(message.author.name) + "#" \
        + str(message.author.discriminator) + " (" \
        + str(message.author.id) + ")"
    embed.set_footer(text=footertext)
    await botcommon.trytolog(message, arg_stack, botuser, embed)
