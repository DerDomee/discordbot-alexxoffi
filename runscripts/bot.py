#!/usr/bin/python
from src.dcbot import client
import sys
import os
from pathlib import Path

Path('./data/xp_events/').mkdir(parents=True, exist_ok=True)

from src.database import sqlengine  # noqa: F401

discord_bot_token = os.getenv('DD_DISCORD_BOTTOKEN', default=None)

if discord_bot_token is None:
    sys.stderr.write(
        "\u001b[31mNo Discord bot token found in environment!\u001b[0m")
    exit(1)

client.run(discord_bot_token)

sys.exit(0)
