import importlib
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
    helpmsg = transget(
        'command.help.general_help.header',
        botuser.user_pref_lang) + "\n```"
    for command in botcommon.registered_bot_commands:
        cmdimport = importlib.import_module(
            '.' + command,
            'resources.dcbot.commands')
        cmdmeta = cmdimport.CMD_METADATA
        if botuser.user_permission_level >= cmdmeta['required_permlevel']:
            helpmsg += command + " - " + transget(
                'command.' + command + '.meta.description',
                botuser.user_pref_lang) + "\n"
    helpmsg += "```"
    await message.channel.send(helpmsg)


async def _do_specific_help(message, arg_stack, botuser):
    await message.channel.send("Hier kommt noch spezifische Befehl-Hilfe!")


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) is 1:
        await _do_general_help(message, arg_stack, botuser)
    else:
        await _do_specific_help(message, arg_stack, botuser)
