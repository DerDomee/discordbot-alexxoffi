from discord import Embed
from resources.dcbot import botcommon
from resources.database import dbcommon
from resources.translation import transget

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_admin,
    'required_channels': [botcommon.key_bot_adminchannel]}


async def get_help(arg_stack, botuser, shortprefix):
    return[]


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) != 3:
        return False
    channel = await botcommon.get_channel_by_id_or_ping(arg_stack[2])
    if channel is None:
        return False

    channelid = channel.id

    channelkey = None

    if arg_stack[1] == "admin":
        channelkey = botcommon.key_bot_adminchannel
    elif arg_stack[1] == "log":
        channelkey = botcommon.key_bot_logchannel
    elif arg_stack[1] == "apply":
        channelkey = botcommon.key_bot_applychannel
    elif arg_stack[1] == "applydest":
        channelkey = botcommon.key_bot_applydestchannel
    elif arg_stack[1] == "voice_newpublic":
        channelkey = botcommon.key_bot_newpublicvoicechannel
    elif arg_stack[1] == "voice_newprivate":
        channelkey = botcommon.key_bot_newprivatevoicechannel
    else:
        await message.channel.send(transget(
            'command.chanset.info.unknown_channelkey',
            botuser.user_pref_lang))
        channelkey = 'bot_' + arg_stack[1] + '_channel'

    dbcommon.set_bot_setting(channelkey, channelid)

    await _log_action(message, arg_stack, botuser, channelkey, channelid)

    return True


async def _log_action(message, arg_stack, botuser, channelkey, channelid):
    embed = Embed(
        title="Channel key set or override",
        description="The channel key `{}` now points to channel {} with the"
                    " ID `{}`".format(
                        channelkey,
                        "<#" + str(channelid) + ">",
                        channelid),
        color=botcommon.key_color_warning)
    footertext = "Requested by " + str(message.author.name) + "#" \
        + str(message.author.discriminator) + " (" \
        + str(message.author.id) + ")"
    embed.set_footer(text=footertext)
    await botcommon.trytolog(message, arg_stack, botuser, embed)
