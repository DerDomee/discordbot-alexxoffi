from discord import Embed, Forbidden
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.database import dbcommon
from resources.dcbot.botcommon import trytolog
from resources.database import sqlsession
from resources.database.models.userwarnings import UserWarnings

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': [botcommon.key_bot_userchannel,
                          botcommon.key_bot_adminchannel]}

# TODO: THIS WHOLE FILE NEEDS PROPER TRANSLATION SUPPORT!


async def _get_member_efficiently(id, guild):
    # REVIEW: This might be finished. Lookaround pls
    try:
        int(id)
    except ValueError:
        return None
    discordmember = guild.get_member(id)
    if discordmember is None:
        discordmember = await guild.fetch_member(id)
    if discordmember is None:
        return None
    return discordmember


async def _get_user_data(member, botuser=None):
    # TODO: Add more information about the member and botuser
    if botuser is None:
        botuser = dbcommon.get_user_or_create(member.id)
    data = {}
    data['username'] = member.display_name
    data['firstjoined'] = member.joined_at
    data['permlevel'] = botuser.user_permission_level
    return data


def _create_embed_from_data(data):
    # TODO: Render more information from data dict (uses information from
    #       _get_user_data function)
    embed = Embed(
        title=data['username'],
        description="Information on server member",
        color=botcommon.key_color_info)
    embed.add_field(
        name="First joined",
        value=data['firstjoined'])
    embed.add_field(
        name="Permission level",
        value=data['permlevel'])
    return embed


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):

    if len(arg_stack) == 1:
        dcmember = await _get_member_efficiently(
            message.author.id,
            message.guild)
        data = await _get_user_data(dcmember, botuser)
        embed = _create_embed_from_data(data)
        await message.channel.send(embed=embed)
        return True
    elif len(arg_stack) == 2:
        if botuser.user_permission_level <= botcommon.key_permlevel_moderator:
            await message.channel.send("No Permission.")
            return False
        dcmember = await _get_member_efficiently(arg_stack[1], message.guild)
        if dcmember is None:
            await message.channel.send("Arg-1 is not a guild member ID.")
            return False
        data = await _get_user_data(dcmember)
        embed = _create_embed_from_data(data)
        await message.channel.send(embed=embed)
        return True
    else:
        return False
