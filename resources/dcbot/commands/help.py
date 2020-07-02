from resources.dcbot import botcommon
from resources.translation import transget
from resources.database import sqlsession


@botcommon.requires_perm_level(level=botcommon.key_permlevel_restricted)
@botcommon.requires_channel([
    botcommon.key_bot_adminchannel,
    botcommon.key_bot_userchannel])
async def invoke(message, arg_stack, botuser):
    await message.channel.send("Hier kommt später Hilfe.")
