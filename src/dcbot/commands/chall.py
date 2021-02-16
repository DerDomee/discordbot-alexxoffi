from asyncio import TimeoutError
from src.dcbot import botcommon
from src.dcbot import client
from lib.hypixel.hypixelv2 import SBAPIRequest, RequestType

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_user,
    'required_channels': [botcommon.key_bot_userchannel,
                          botcommon.key_bot_adminchannel]}

NUMBER_REACTIONS = ['1️⃣', '2️⃣', '3️⃣',
                    '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


async def _get_available_profiles(
        message, arg_stack, botuser, response_message):
    uuidrequest = SBAPIRequest(RequestType.GETUUID, (arg_stack[2],))
    uuid = await botcommon.hypixel_api.request(uuidrequest, 5)
    if 'dd_error' in uuid:
        await response_message.edit(
            content=f"{message.author.mention}, this player does not exist.")
        return False
    uuid = uuid['id']
    profilesrequest = SBAPIRequest(RequestType.PROFILES, (uuid,))
    profiles = await botcommon.hypixel_api.request(profilesrequest, 10)
    if 'dd_error' in profiles:
        print(profiles)
        await response_message.edit(
            content=f"{message.author.mention}, there was an error while "
            + "getting your skyblock profiles. Try again later.")
        return False
    if profiles['profiles'] is None:
        await response_message.edit(
            content=f"{message.author.mention}, this "
            + "player does not have a skyblock profile.")
        return False
    return list(profiles['profiles'])


async def _get_selected_profile(
        message, arg_stack, botuser, response_message, available_profiles):
    if len(available_profiles) == 1:
        return available_profiles[0]
    available_text = f"{message.author.mention}, please select your profile:"
    for index, profile in enumerate(available_profiles):
        emote = NUMBER_REACTIONS[index]
        pname = profile['cute_name']
        available_text += f"\n{emote} {pname}"
    await response_message.edit(content=available_text)
    for i in range(len(available_profiles)):
        await response_message.add_reaction(NUMBER_REACTIONS[i])

    def pselect_check(reaction, user):
        return user.id == message.author.id and \
            reaction.message.id == response_message.id and str(
                reaction) in NUMBER_REACTIONS[:len(available_profiles)]

    try:
        reaction, reactionuser = await client.wait_for(
            'reaction_add', check=pselect_check, timeout=30.0
        )
    except TimeoutError:
        await response_message.clear_reactions()
        await response_message.edit(
            content=f"{message.author.mention}, session closed!"
        )
        return False
    else:
        selected_profile = available_profiles[NUMBER_REACTIONS.index(
            str(reaction))]
        await response_message.clear_reactions()
        return selected_profile
    return False


async def _get_challenge_type(message, arg_stack, botuser, response_message):
    available_types = [e.name for e in botcommon.StatTypes]
    await response_message.edit(
        content=f"{message.author.mention}, Select the type of the challenge:"
                + f"```{' / '.join(available_types)}```")

    def typeselect_check(typemessage):
        return typemessage.channel.id == message.channel.id and \
            typemessage.author.id == message.author.id

    challtype = None
    while challtype is None:
        try:
            typemessage = await client.wait_for(
                'message', check=typeselect_check, timeout=60.0)
        except TimeoutError:
            await response_message.edit(
                content=f"{message.author.mention}, session closed!"
            )
            return False
        else:
            selected_type = typemessage.content
            await typemessage.delete()
            if selected_type in botcommon.StatTypes.__members__:
                challtype = botcommon.StatTypes[selected_type]
    return challtype.name


async def _create_challenge(message, arg_stack, botuser):
    response_message = await message.channel.send(
        f"{message.author.mention}, creating...")

    challenge_type = await _get_challenge_type(
        message, arg_stack, botuser, response_message)
    if challenge_type is False:
        return False

    await response_message.edit(
        content=f"{message.author.mention}, selected type: {challenge_type}")


async def _join_challenge(message, arg_stack, botuser):
    response_message = await message.channel.send(
        f"{message.author.mention}, fetching...")
    available_profiles = await _get_available_profiles(
        message, arg_stack, botuser, response_message)
    if available_profiles is False:
        return False
    selected_profile = await _get_selected_profile(
        message, arg_stack, botuser, response_message, available_profiles)
    if selected_profile is False:
        return False

    await response_message.edit(
        content=f"{message.author.mention}, selected profile: "
        + f"{selected_profile['cute_name']}")
    return True


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) == 2:
        if arg_stack[1].lower() == "create":
            return await _create_challenge(message, arg_stack, botuser)
    elif len(arg_stack) == 3:
        if arg_stack[1].lower() == "join":
            return await _join_challenge(message, arg_stack, botuser)
