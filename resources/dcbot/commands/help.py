import importlib
from discord import Embed
from resources.database import sqlsession
from resources.dcbot import botcommon
from resources.dcbot import commands
from resources.translation import transget

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': [botcommon.key_bot_adminchannel,
                          botcommon.key_bot_userchannel]}


async def _do_general_help(message, arg_stack, botuser):
    helpmsg = transget(
        'command.help.general_help.header',
        botuser.user_pref_lang) + "\n```md\n"
    for command in botcommon.registered_bot_commands:
        cmdimport = importlib.import_module(
            '.' + command,
            'resources.dcbot.commands')
        cmdmeta = cmdimport.CMD_METADATA
        if botuser.user_permission_level >= cmdmeta['required_permlevel']:
            helpmsg += "<" + command + "> " + transget(
                'command.' + command + '.meta.description',
                botuser.user_pref_lang) + "\n"
    helpmsg += "```"
    await message.channel.send(helpmsg)


async def _do_specific_help(message, arg_stack, botuser):
    try:
        cmdimport = importlib.import_module(
            '.' + arg_stack[1],
            'resources.dcbot.commands')
    except ModuleNotFoundError as e:
        # TODO: Translate this
        await message.channel.send("Command not found")
    else:
        try:
            if botuser.user_permission_level >= \
                    cmdimport.CMD_METADATA['required_permlevel']:
                await cmdimport.print_help(message, arg_stack, botuser)
            else:
                await message.channel.send(
                    "You have no permission to get help for this command.")
        except Exception as e:
            await message.channel.send(
                "This command has no function to print help.")


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) is 1:
        await _do_general_help(message, arg_stack, botuser)
    else:
        await _do_specific_help(message, arg_stack, botuser)
