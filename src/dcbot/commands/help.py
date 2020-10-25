import importlib
from discord import Embed
from src.database import sqlsession
from src.database import dbcommon
from src.dcbot import botcommon
from src.dcbot import commands
from src.translation import transget

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': [botcommon.key_bot_adminchannel,
                          botcommon.key_bot_userchannel]}


async def get_help(arg_stack, botuser, shortprefix):
    return[]


async def _do_general_help(message, arg_stack, botuser):
    shortprefix = dbcommon.get_bot_setting(botcommon.key_bot_prefix, "$")
    helpmsg = transget(
        'command.help.general_help.header',
        botuser.user_pref_lang).format(
            shortprefix=shortprefix) + "\n```md\n"
    for command in botcommon.registered_bot_commands:
        cmdimport = importlib.import_module(
            '.' + command,
            'src.dcbot.commands')
        cmdmeta = cmdimport.CMD_METADATA
        if botuser.user_permission_level >= cmdmeta['required_permlevel']:
            helpmsg += "<" + command + "> " + transget(
                'command.' + command + '.meta.description',
                botuser.user_pref_lang) + "\n"
    helpmsg += "```"
    await message.channel.send(helpmsg)


async def _do_specific_help(message, arg_stack, botuser):
    shortprefix = dbcommon.get_bot_setting(botcommon.key_bot_prefix, "$")
    try:
        cmdimport = importlib.import_module(
            '.' + arg_stack[1],
            'src.dcbot.commands')
    except ModuleNotFoundError:
        # TODO: Translate this
        await message.channel.send("Command not found")
    else:
        try:
            if botuser.user_permission_level >= \
                    cmdimport.CMD_METADATA['required_permlevel']:
                cmdhelp = await cmdimport.get_help(
                    arg_stack, botuser, shortprefix)
                for embed in cmdhelp:
                    await message.channel.send(embed=embed)
                if cmdhelp is None or cmdhelp == []:
                    await message.channel.send(
                        "This command does not implement help functions.")
            else:
                await message.channel.send(
                    "You have no permission to get help for this command.")
        except Exception:
            await message.channel.send(
                "This command has no function to print help.")


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) == 1:
        await _do_general_help(message, arg_stack, botuser)
    else:
        await _do_specific_help(message, arg_stack, botuser)
