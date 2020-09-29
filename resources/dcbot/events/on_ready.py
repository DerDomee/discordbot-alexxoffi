import pkgutil
from resources.dcbot import client
from resources.dcbot import botcommon
from resources.dcbot import messageprocessors
from resources.dcbot import commands
from resources.translation import transget


@client.event
async def on_ready():
    # Setting the first guild (which is the only guild per definition) to a
    # commonly accessible variable
    botcommon.main_guild = client.guilds[0]
    # Place all commands in a register used for the help command
    for importer, modname, ispkg in pkgutil.iter_modules(commands.__path__):
        if not str(modname).startswith('_'):
            botcommon.registered_bot_commands.append(modname)
    # Place all message processors in a register to call everyone of them
    # on every message ever sent
    for importer, modname, ispkg in pkgutil.iter_modules(
            messageprocessors.__path__):
        if not str(modname).startswith('_'):
            botcommon.registered_message_processors.append(modname)
    # Log the ready-state of the bot in the console.
    message = transget("dcbot.readymessage").format(
        client=client.user)
    print(message)
