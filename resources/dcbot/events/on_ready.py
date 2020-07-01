from resources.dcbot import client
from resources.translation import transget


@client.event
async def on_ready():
    message = transget("dcbot.readymessage").format(
        client=client.user)
    print(message)
