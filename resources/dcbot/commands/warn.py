from discord import Embed, Forbidden
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.dcbot.botcommon import trytolog
from resources.database import sqlsession
from resources.database.models.userwarnings import UserWarnings

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_moderator,
    'required_channels': None}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
async def invoke(message, arg_stack, botuser):

    if len(arg_stack) < 3:
        return False
    else:
        try:
            warned_member = await message.guild.fetch_member(arg_stack[1])
        except Exception:
            warned_member = None
        if warned_member is None:
            await message.channel.send("User not found.")
            return False
        new_warn = UserWarnings(
            reason=" ".join(arg_stack[2:]),
            issuer=message.author.id,
            warned_user=warned_member.id)
        sqlsession.add(new_warn)
        sqlsession.commit()
        await message.channel.send("User warned.")
        try:
            await warned_member.send("You have been warned.")
        except Forbidden:
            await message.channel.send("User does not allow private messages "
                                       "from this bot, so ping the user here: "
                                       + warned_member.mention)
        return True
