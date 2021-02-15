from src.dcbot import botcommon
from src.dcbot import client
import asyncio
from src.translation import transget
from lib.hypixel.hypixelv2 import SBAPIRequest, RequestType

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_user,
    'required_channels': [botcommon.key_bot_userchannel,
                          botcommon.key_bot_adminchannel]}

NUMBER_REACTIONS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', ]


async def _get_available_profiles(message, arg_stack, botuser):
    uuidrequest = SBAPIRequest(RequestType.GETUUID, (arg_stack[1],))
    uuid = await botcommon.hypixel_api.request(uuidrequest, 5)
    if 'dd_error' in uuid:
        await message.channel.send(f"{message.author.mention}, this player does not exist.")
        return False
    uuid = uuid['id']
    profilesrequest = SBAPIRequest(RequestType.PROFILES, (uuid,))
    profiles = await botcommon.hypixel_api.request(profilesrequest, 5)
    if 'dd_error' in profiles:
        await message.channel.send(f"{message.author.mention}, there was an error while getting your skyblock profiles. Try again later.")
        return False
    if profiles['profiles'] == None:
        await message.channel.send(f"{message.author.mention}, this player does not have a skyblock profile.")
        return False
    return list(profiles['profiles'])


async def _get_selected_profile(message, arg_stack, botuser, available_profiles):
    if len(available_profiles) == 1:
        return available_profiles[0]
    available_text = f"{message.author.mention}, please select your profile:"
    for index, profile in enumerate(available_profiles):
        emote = NUMBER_REACTIONS[index]
        pname = profile['cute_name']
        available_text += f"\n{emote} {pname}"
    pselector = await message.channel.send(available_text)
    for i in range(len(available_profiles)):
        await pselector.add_reaction(NUMBER_REACTIONS[i])

    def pselect_check(reaction, user):
        return user.id == message.author.id and reaction.message.id == pselector.id and str(reaction) in NUMBER_REACTIONS[:len(available_profiles)]

    try:
        reaction, reactionuser = await client.wait_for('reaction_add', check=pselect_check, timeout=30.0)
    except asyncio.TimeoutError:
        await pselector.delete()
        await message.channel.send(f"{message.author.mention}, session closed!")
        return False
    else:
        selected_profile = available_profiles[NUMBER_REACTIONS.index(str(reaction))]
        await pselector.delete()
        return selected_profile
    return False


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) >= 2:
        available_profiles = await _get_available_profiles(message, arg_stack, botuser)
        if available_profiles is False:
            return False
        selected_profile = await _get_selected_profile(message, arg_stack, botuser, available_profiles)
        if selected_profile is False:
            return False

        await message.channel.send(f"{message.author.mention}, selected profile: {selected_profile['cute_name']}")
