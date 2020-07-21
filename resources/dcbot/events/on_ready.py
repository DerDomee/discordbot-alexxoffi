import pkgutil
from resources.dcbot import client
from resources.dcbot import botcommon
from resources.dcbot import commands
from resources.translation import transget


@client.event
async def on_ready():
    for importer, modname, ispkg in pkgutil.iter_modules(commands.__path__):
        botcommon.registered_bot_commands.append(modname)
    # Can remove this debug print later
    print(botcommon.registered_bot_commands)
    message = transget("dcbot.readymessage").format(
        client=client.user)
    print(message)
