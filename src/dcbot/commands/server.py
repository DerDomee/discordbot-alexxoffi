from src.dcbot import botcommon
from src.translation import transget
from discord import Embed, Status

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_user,
    'required_channels': [botcommon.key_bot_userchannel,
                          botcommon.key_bot_adminchannel]}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    embed = Embed(
        title=message.guild.name,
        description=transget(
            'command.server.embed.desc',
            botuser.user_pref_lang),
        color=botcommon.key_color_info)
    embed.set_thumbnail(url=message.guild.icon_url)
    created = message.guild.created_at.date()

    embed.add_field(
        name=transget(
            'command.server.embed.field.creation_date.title',
            botuser.user_pref_lang),
        value=f"{created.day}.{created.month}.{created.year}"
    )

    embed.add_field(
        name=transget(
            'command.server.embed.field.owner.title',
            botuser.user_pref_lang
        ),
        value=message.guild.owner.mention
    )

    onlinecount = sum(
        m.status != Status.offline for m in message.guild.members)
    embed.add_field(
        name=transget(
            'command.server.embed.field.members.title',
            botuser.user_pref_lang
        ).format(member_count=message.guild.member_count),
        value=transget(
            'command.server.embed.field.members.value',
            botuser.user_pref_lang
        ).format(member_count=onlinecount)
    )

    footertext = "Requested by " + str(message.author.name) + "#" \
        + str(message.author.discriminator) + " (" \
        + str(message.author.id) + ")"
    embed.set_footer(text=footertext)

    await message.channel.send(embed=embed)
