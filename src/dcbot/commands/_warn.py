from discord import Embed, Forbidden
from src.dcbot import botcommon
from src.dcbot import client
from src.translation import transget
from src.dcbot.botcommon import trytolog
from src.database import sqlsession
from src.database.dbcommon import get_user_or_create
from src.database.models.userwarnings import UserWarnings

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
            await message.channel.send(transget(
                'command.warn.error.user_not_found',
                botuser.user_pref_lang))
            return False
        new_warn = UserWarnings(
            reason=" ".join(arg_stack[2:]),
            issuer=message.author.id,
            warned_user=warned_member.id)
        sqlsession.add(new_warn)
        sqlsession.commit()
        warned_botuser = get_user_or_create(warned_member.id)
        await message.channel.send()
        try:
            # REVIEW: This standard translation needs more information in it.
            await warned_member.send(transget(
                'command.warn.notification.warned',
                warned_botuser.user_pref_lang))
        except Forbidden:
            await message.channel.send(transget(
                'command.warn.notification.warned.public',
                warned_botuser.user_pref_lang).format(
                    mention=warned_member.mention))
        return True
