import os
from discord import Embed
from resources.dcbot import botcommon
from resources.database import dbcommon


async def invoke(message):
    bottoken = os.getenv('DD_DISCORD_BOTTOKEN', default=None)
    if bottoken in message.content:
        await message.delete()

        embed = Embed(
            title="The Bot Token has been leaked!",
            color=botcommon.key_color_danger)
        embed.add_field(
            name="User",
            value=message.author.mention)
        embed.add_field(
            name="Channel",
            value="<#" + message.channel.id + ">")
        embed.add_field(
            name="Message",
            value=message.content.replace(bottoken, "<token>"))

        return{'continue': False}
    return {'continue': True}
