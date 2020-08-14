from discord import Embed, Forbidden
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.dcbot.botcommon import trytolog
from resources.database import sqlsession
from resources.database.models.userwarnings import UserWarnings

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': [botcommon.key_bot_userchannel,
                          botcommon.key_bot_adminchannel]}


def _is_user_id(id):
    # TODO: Check if argument is a Discord User ID
    # and if this User is actually a member of the server
    pass


def _get_user_data(id):
    # TODO: Get User Data from the ID
    # Gathering data from Discord API and the Database
    pass


def _create_embed_from_data(data):
    # TODO: Parse given data and create an embed showing this data
    pass


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):

    if len(arg_stack) is 1:
        data = _get_user_data(message.author.id)
        embed = _create_embed_from_data(data)
        await message.channel.send(embed=embed)
        return True
    elif len(arg_stack) is 2:
        if not _is_user_id(arg_stack[1]):
            message.channel.send("Arg 1 is not a user ID.")
            return False
        if botuser.user_permission_level <= botcommon.key_permlevel_moderator:
            message.channel.send("No Permission.")
            return False
        data = _get_user_data(arg_stack[1])
        embed = _create_embed_from_data(data)
        await message.channel.send(embed=embed)
        return True
    else:
        return False
