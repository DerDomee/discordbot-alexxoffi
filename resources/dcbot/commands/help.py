from discord import Embed
from resources.database import sqlsession
from resources.dcbot import botcommon
from resources.dcbot import commands
from resources.translation import transget

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': [botcommon.key_bot_adminchannel,
                          botcommon.key_bot_userchannel],
    'command_syntax': "[command_name]"}


async def _do_general_help(message, arg_stack, botuser):
    helpmessage = "{help_general_title}\n\n" \
                  "Usage: {bot_shortprefix}help or" \
                  "{bot_shortprefix}help <command>\n\n"
    await message.channel.send("```" + helpmessage + "```")


async def _do_specific_help(message, arg_stack, botuser):
    await_message.channel.send("Hier kommt noch spezifische Befehl-Hilfe!")


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) is 1:
        await _do_general_help(message, arg_stack, botuser)
        print(botcommon.registered_bot_commands)
    else:
        await _do_specific_help(message, arg_stack, botuser)
