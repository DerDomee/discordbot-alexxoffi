import os
from resources.database import sqlengine
from resources.dcbot import client

discord_bot_token = os.getenv('DD_DISCORD_BOTTOKEN', default=None)

if discord_bot_token is None:
    print("No Discord bot token found in environment!")
    exit(1)

client.run(discord_bot_token)
