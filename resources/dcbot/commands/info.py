import os
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.database import dbcommon
from resources.translation import transget
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
            'command.info.embed.field.author.title',
            botuser.user_pref_lang),
        value="<@285720078031388673>",
        inline=True)

    embed.add_field(
        name=transget(
            'command.info.embed.field.version.title',
            botuser.user_pref_lang),
        value=os.getenv('DD_BOT_VERSION', "0.1.0-SNAPSHOT"),
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
                    '$')
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
