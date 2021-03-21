import os
import signal
import pkgutil
from src.dcbot import client
from src.dcbot import botcommon
from src.dcbot import messageprocessors
from src.dcbot import commands
from src.dcbot.commands import stop
from src.translation import transget
from lib.hypixel import hypixelv2


def signal_handler(signal, frame):
    print("\nPROCESS SIGNAL (SIGINT) Captured! (CTRL+C)")
    client.loop.create_task(stop.controlled_stop())


@client.event
async def on_ready():

    if not botcommon.is_initial_start:
        print("Bot reconnected to discord after connection loss")
        return
    botcommon.is_initial_start = False

    # Setting the first guild (which is the only guild per definition) to a
    # commonly accessible variable
    print("Initializing the bot...")
    print(f"Setting main guild to {str(client.guilds[0])}")
    botcommon.main_guild = client.guilds[0]

    # Place all commands in a register used for the help command
    print("Getting all enabled commands...")
    for importer, modname, ispkg in pkgutil.iter_modules(commands.__path__):
        if not str(modname).startswith('_'):
            botcommon.registered_bot_commands.append(modname)

    # Place all message processors in a register to call everyone of them
    # on every message ever sent
    print("Getting all enabled message processors...")
    for importer, modname, ispkg in pkgutil.iter_modules(
            messageprocessors.__path__):
        if not str(modname).startswith('_'):
            botcommon.registered_message_processors.append(modname)

    print("Starting Hypixel API...")
    botcommon.hypixel_api = hypixelv2.SkyblockAPI(
        os.getenv('DD_HYPIXEL_API_KEY', ''))
    botcommon.hypixel_api.start()

    print("Starting Challenge Event scheduler...")
    botcommon.challenge_scheduler = botcommon.ChallengeScheduler()
    botcommon.challenge_scheduler.start()

    print("Load previously tracked challenge events")
    botcommon.challenge_scheduler.load_all_tracked()

    print("Initializing Signal Handler, Press CTRL+C once (!) to shut down "
          + "the bot at any time!")
    signal.signal(signal.SIGINT, signal_handler)

    # Log the ready-state of the bot in the console.
    message = transget("dcbot.readymessage").format(
        client=client.user)
    print(message)
