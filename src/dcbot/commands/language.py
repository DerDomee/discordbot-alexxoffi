from src.dcbot import botcommon
from src.translation import transget
from src.database import sqlsession

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': [botcommon.key_bot_adminchannel,
                          botcommon.key_bot_userchannel]}

SUPPORTED_LANGS = ["en", "de"]


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):

    if len(arg_stack) == 1:
        return False
    if len(arg_stack) == 2:
        if arg_stack[1] == "get":
            await message.channel.send(
                transget(
                    'command.language.get.text',
                    botuser.user_pref_lang
                ).format(
                    lang=botuser.user_pref_lang
                )
            )
            pass
    if len(arg_stack) == 3:
        if arg_stack[1] == "set":
            if arg_stack[2] in SUPPORTED_LANGS:
                botuser.user_pref_lang = arg_stack[2]
                sqlsession.commit()
                await message.channel.send(
                    transget(
                        'command.language.set.success',
                        botuser.user_pref_lang
                    ).format(
                        lang=botuser.user_pref_lang
                    )
                )
            else:
                print("provided lang not supported")
