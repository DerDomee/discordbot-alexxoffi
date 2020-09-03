import pkgutil
from resources.dcbot import client
from resources.dcbot import botcommon
from resources.dcbot import messageprocessors
from resources.dcbot import commands
from resources.translation import transget


@client.event
async def on_ready():
    for importer, modname, ispkg in pkgutil.iter_modules(commands.__path__):
        if not str(modname).startswith('_'):
            botcommon.registered_bot_commands.append(modname)
    for importer, modname, ispkg in pkgutil.iter_modules(
            messageprocessors.__path__):
        if not str(modname).startswith('_'):
            botcommon.registered_message_processors.append(modname)
    message = transget("dcbot.readymessage").format(
        client=client.user)
    print(message)
