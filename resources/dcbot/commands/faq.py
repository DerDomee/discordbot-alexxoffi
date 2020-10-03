from discord import Embed
from resources.dcbot import botcommon
from resources.translation import transget
from resources.dcbot import client
from resources.dcbot.botcommon import trytolog

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_moderator,
    'required_channels': None}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
async def invoke(message, arg_stack, botuser):

    if len(arg_stack) != 3:
        await message.channel.send(transget(
            "command.faq.err.wrongsyntax",
            botuser.user_pref_lang))
        return False

    question = arg_stack[1]
    answer = arg_stack[2]

    embed = Embed(
        title=question,
        description=answer,
        color=botcommon.key_color_info)

    await message.channel.send(embed=embed)
    await message.delete()
