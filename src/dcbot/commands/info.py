import os
from src.dcbot import botcommon
from src.dcbot import client
from src.database import dbcommon
from src.translation import transget
from discord import Embed

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_user,
    'required_channels': [botcommon.key_bot_userchannel,
                          botcommon.key_bot_adminchannel]}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    embed = Embed(
        title=transget(
            'command.info.embed.title',
            botuser.user_pref_lang).format(
                bot_title=transget(
                    'bot.title',
                    botuser.user_pref_lang)),
        description=transget(
            'command.info.embed.desc',
            botuser.user_pref_lang),
        color=0xdfdfdf)

    embed.set_thumbnail(
        url=str(client.user.avatar_url))

    embed.add_field(
        name=transget(
            'dcbot.features.title',
            botuser.user_pref_lang),
        value=transget(
            'dcbot.features.features',
            botuser.user_pref_lang),
        inline=False)

    embed.add_field(
        name=transget(
            'command.info.embed.field.author.title',
            botuser.user_pref_lang),
        value="<@285720078031388673>",
        inline=True)

    embed.add_field(
        name=transget(
            'dcbot.contributor.title',
            botuser.user_pref_lang),
        value=transget(
            'dcbot.contributor.contributors',
            botuser.user_pref_lang),
        inline=True)

    versiontag = os.popen('git describe --tags --abbrev=0').read().rstrip('\n')
    versioncommit = os.popen('git rev-parse --short HEAD').read().rstrip('\n')

    versionstring = str(versiontag) + " (" + str(versioncommit) + ")"

    embed.add_field(
        name=transget(
            'command.info.embed.field.version.title',
            botuser.user_pref_lang),
        value=versionstring,
        inline=True)

    embed.add_field(
        name=transget(
            'command.info.embed.field.upstream.title',
            botuser.user_pref_lang),
        value=transget(
            'command.info.embed.field.upstream.value',
            botuser.user_pref_lang),
        inline=False)

    embed.add_field(
        name=transget(
            'command.info.embed.field.prefix.title',
            botuser.user_pref_lang),
        value=transget(
            'command.info.embed.field.prefix.value',
            botuser.user_pref_lang).format(
            longprefix="<@" + str(client.user.id) + ">",
            shortprefix=dbcommon.get_bot_setting(
                botcommon.key_bot_prefix,
                '$'
            )
        ),
        inline=True)

    embed.add_field(
        name=transget(
            'command.info.embed.field.bugreports.title',
            botuser.user_pref_lang),
        value=transget(
            'command.info.embed.field.bugreports.value',
            botuser.user_pref_lang),
        inline=False)

    footertext = "Requested by " + str(message.author.name) + "#" \
        + str(message.author.discriminator) + " (" \
        + str(message.author.id) + ")"
    embed.set_footer(text=footertext)

    await message.channel.send(embed=embed)
