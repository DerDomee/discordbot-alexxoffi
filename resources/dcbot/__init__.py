import discord
from resources.translation import transget

client = discord.Client()

@client.event
async def on_ready():
    message = transget("dcbot.readymessage").format(
        client=client.user)
    print(message)
