from discord import Embed
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.dcbot.botcommon import trytolog


@botcommon.requires_perm_level(level=botcommon.key_permlevel_owner)
@botcommon.requires_channel([botcommon.key_bot_adminchannel])
async def invoke(message, arg_stack, botuser):

    # This embed needs to be filled for trytolog to work.
    embed = discord.Embed()
    # trytolog might not be implemented in botcommon
    trytolog(message, arg_stack, botuser, embed)

    await client.logout()
    return True
