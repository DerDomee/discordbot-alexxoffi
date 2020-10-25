#!/usr/bin/python
import os
import sys
from src.database import sqlengine
from src.dcbot import client

discord_bot_token = os.getenv('DD_DISCORD_BOTTOKEN', default=None)

if discord_bot_token is None:
    sys.stderr.write(
        "\u001b[31mNo Discord bot token found in environment!\u001b[0m")
    exit(1)

client.run(discord_bot_token)

sys.exit(0)
