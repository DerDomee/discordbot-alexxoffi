from src.dcbot import client
from src.dcbot import botcommon
from src.dcbot.botcommon import trytolog
from src.database import sqlsession
from src.database import dbcommon

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_admin,
    'required_channels': [botcommon.key_bot_adminchannel]}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    user_id = arg_stack[1]
    perm_level = arg_stack[2]

    try:
        int(user_id)
        int(perm_level)
    except ValueError:
        await message.channel.send("Value Error")
        return False

    if user_id == message.author.id:
        await message.channel.send("Shall not edit thyself!")
        return False

    dbuser = dbcommon.get_user(user_id)

    if dbuser is None:
        await message.channel.send("Botuser not found")
        return False

    dbuser.user_permission_level = perm_level
    sqlsession.commit()
