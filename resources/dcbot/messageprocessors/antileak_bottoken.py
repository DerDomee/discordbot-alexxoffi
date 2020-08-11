import os
from discord import Embed
from resources.dcbot import botcommon
from resources.database import dbcommon


async def invoke(message):
    bottoken = os.getenv('DD_DISCORD_BOTTOKEN', default=None)
    if bottoken in message.content:
        await message.delete()

        # TODO: Automute user on server

        embed = Embed(
            title="The Bot Token has been leaked!",
            color=botcommon.key_color_danger)
        embed.add_field(
            name="User",
            value=message.author.mention,
            inline=True)
        embed.add_field(
            name="Channel",
            value="<#" + str(message.channel.id) + ">",
            inline=True)
        embed.add_field(
            name="Message",
            value=message.content.replace(bottoken, "<token>"),
            inline=False)

        await botcommon.trytolog(message, None, None, embed)

        return{'continue': False}
    return {'continue': True}
