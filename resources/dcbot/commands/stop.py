from discord import Embed
from resources.dcbot import botcommon
from resources.dcbot import client
from resources.dcbot.botcommon import trytolog

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_owner,
    'required_channels': [botcommon.key_bot_adminchannel],
    'command_syntax': ""}


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):

    # This embed needs to be filled for trytolog to work.
    embed = Embed(
        title="Bot shuts down",
        description="Due to an admin command the bot shuts down now.",
        color=botcommon.key_color_danger)
    footertext = "Requested by " + str(message.author.name) + "#" \
        + str(message.author.discriminator) + " (" \
        + str(message.author.id) + ")"
    embed.set_footer(text=footertext)
    await trytolog(message, arg_stack, botuser, embed)

    print("Gracefully shut down bot due to admin command")
    await client.logout()
    return True
