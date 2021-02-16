from asyncio import TimeoutError
from datetime import datetime
from discord import Embed
from src.dcbot import botcommon
from src.dcbot import client
from lib.hypixel.hypixelv2 import SBAPIRequest, RequestType
import uuid

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
                challtype = botcommon.StatTypes[selected_type].name
    return challtype


async def _determine_challenge_start_time(
        message, arg_stack, botuser, response_message):
    await response_message.edit(
        content=f"{message.author.mention}, please enter a start time "
        + "for the challenge in following format: `dd.mm.yyyy-hh:mm:ss`. "
        + "Examples: ```01.01.2021-00:00:00\n23.07.2022-21:00:00```")

    def timeselect_check(timemessage):
        return timemessage.channel.id == message.channel.id and \
            timemessage.author.id == message.author.id

    time = None
    while time is None:
        try:
            timemessage = await client.wait_for(
                'message', check=timeselect_check, timeout=60.0)
        except TimeoutError:
            await response_message.edit(
                content=f"{message.author.mention}, session closed!")
            return False
        else:
            entered_time = timemessage.content
            await timemessage.delete()
            try:
                dt = datetime.strptime(entered_time, '%d.%m.%Y-%H:%M:%S')
            except ValueError:
                await response_message.edit(
                    content=f"{message.author.mention}, wrong time format. "
                    + "Please use following format: `dd.mm.yyyy-hh:mm:ss`. "
                    + "Examples: ```01.01.2021-00:00:00\n"
                    + "23.07.2022-21:00:00```")
                continue
            if not dt > datetime.now():
                await response_message.edit(
                    content=f"{message.author.mention}, time must be in the "
                    + "future. Please use following format: "
                    + "`dd.mm.yyyy-hh:mm:ss`. Examples: "
                    + "```01.01.2021-00:00:00\n23.07.2022-21:00:00```")
                continue
            else:
                time = dt
    return time


async def _determine_challenge_end_time(
        message, arg_stack, botuser, response_message, start_time):
    await response_message.edit(
        content=f"{message.author.mention}, please enter a end time "
        + "for the challenge in following format: `dd.mm.yyyy-hh:mm:ss`. "
        + "Examples: ```01.01.2021-00:00:00\n23.07.2022-21:00:00```")

    def timeselect_check(timemessage):
        return timemessage.channel.id == message.channel.id and \
            timemessage.author.id == message.author.id

    time = None
    while time is None:
        try:
            timemessage = await client.wait_for(
                'message', check=timeselect_check, timeout=60.0)
        except TimeoutError:
            await response_message.edit(
                content=f"{message.author.mention}, session closed!")
            return False
        else:
            entered_time = timemessage.content
            await timemessage.delete()
            try:
                dt = datetime.strptime(entered_time, '%d.%m.%Y-%H:%M:%S')
            except ValueError:
                await response_message.edit(
                    content=f"{message.author.mention}, wrong time format. "
                    + "Please use following format: `dd.mm.yyyy-hh:mm:ss`. "
                    + "Examples: ```01.01.2021-00:00:00\n"
                    + "23.07.2022-21:00:00```")
                continue
            if not dt > start_time:
                await response_message.edit(
                    content=f"{message.author.mention}, end time must be "
                    + "after start time. Please use following format: "
                    + "`dd.mm.yyyy-hh:mm:ss`. Examples: "
                    + "```01.01.2021-00:00:00\n23.07.2022-21:00:00```")
                continue
            else:
                time = dt
    return time


async def _get_payin_coins(message, arg_stack, botuser, response_message):
    await response_message.edit(
        content=f"{message.author.mention}, enter a [integer] of coins needed "
        + "to pay-in and join the challenge. Enter `0` for no pay-in.")

    def payin_check(payinmessage):
        return payinmessage.channel.id == message.channel.id and \
            payinmessage.author.id == message.author.id

    payin = None
    while payin is None:
        try:
            payinmessage = await client.wait_for(
                'message', check=payin_check, timeout=60.0)
        except TimeoutError:
            await response_message.edit(
                content=f"{message.author.mention}, session closed!")
            return False
        else:
            entered_value = payinmessage.content
            await payinmessage.delete()
            try:
                needed_coins = int(entered_value)
            except ValueError:
                await response_message.edit(
                    content=f"{message.author.mention}, please only enter an "
                    + "integer number for pay-in. Enter `0` for no pay-in")
                continue
            payin = needed_coins
    return payin


async def _determine_auto_accept_mode(
        message, arg_stack, botuser, response_message, payin_coins):
    if payin_coins == 0:
        await response_message.edit(
            content=f"{message.author.mention}, should entering users be "
            + "auto-accepted? No Pay-In needed for this challenge, so 'YES' "
            + "is recommended.")
    else:
        await response_message.edit(
            content=f"{message.author.mention}, should entering users be "
            + "auto-accepted? Pay-In is needed for this challenge, so 'NO' "
            + "is recommended.")
    await response_message.add_reaction("✅")
    await response_message.add_reaction("❌")

    def autoaccept_check(reaction, user):
        return user.id == message.author.id and \
            reaction.message.id == response_message.id and str(reaction) in \
            ['✅', '❌']

    try:
        reaction, reactionuser = await client.wait_for(
            'reaction_add', check=autoaccept_check, timeout=30.0
        )
    except TimeoutError:
        await response_message.clear_reactions()
        await response_message.edit(
            content=f"{message.author.mention}, session closed!"
        )
        return False
    else:
        await response_message.clear_reactions()
        if str(reaction) == "✅":
            return True
        else:
            return False

    await response_message.clear_reactions()
    return None


async def _get_challenge_name(message, arg_stack, botuser, response_message):
    await response_message.edit(
        content=f"{message.author.mention}, please choose a displayname of "
        + "the challenge with up to 40 characters.")

    def namemsgcheck(namemessage):
        return namemessage.channel.id == message.channel.id and \
            namemessage.author.id == message.author.id

    chosen_name = None
    while chosen_name is None:
        try:
            namemessage = await client.wait_for(
                'message', check=namemsgcheck, timeout=60.0)
        except TimeoutError:
            await response_message.edit(
                content=f"{message.author.mention}, session closed!")
            return False
        else:
            entered_name = namemessage.content
            await namemessage.delete()
            if len(entered_name) > 40:
                continue
            chosen_name = entered_name
    return chosen_name


async def _get_challenge_preview(challenge):
    embed = Embed(
        title=challenge['title'],
        description=f"UUID: `{challenge['uuid']}`")
    embed.add_field(
        name="Challenge Type",
        value=challenge['type'],
        inline=True)
    embed.add_field(
        name="Status",
        value=challenge['status'])
    embed.add_field(
        name="Start",
        value=datetime.fromtimestamp(challenge['start_time']))
    embed.add_field(
        name="End",
        value=datetime.fromtimestamp(challenge['end_time']))
    if challenge['pay_in'] == 0:
        embed.add_field(name="Pay-In", value="Not needed")
    else:
        embed.add_field(name="Pay-In", value=challenge['pay_in'])
    embed.add_field(
        name="Auto-Accept on join",
        value=challenge['auto_accept'])
    return embed


async def _create_challenge(message, arg_stack, botuser):
    response_message = await message.channel.send(
        f"{message.author.mention}, creating...")

    challenge_type = await _get_challenge_type(
        message, arg_stack, botuser, response_message)
    if challenge_type is False:
        return False

    start_time = await _determine_challenge_start_time(
        message, arg_stack, botuser, response_message)
    if start_time is False:
        return False

    end_time = await _determine_challenge_end_time(
        message, arg_stack, botuser, response_message, start_time)
    if end_time is False:
        return False

    payin_coins = await _get_payin_coins(
        message, arg_stack, botuser, response_message)
    if payin_coins is False:
        return False

    auto_accept = await _determine_auto_accept_mode(
        message, arg_stack, botuser, response_message, payin_coins)
    if auto_accept is None:
        return False

    challenge_name = await _get_challenge_name(
        message, arg_stack, botuser, response_message)
    if challenge_name is False:
        return False

    challenge_uuid = uuid.uuid4()

    final_challenge = {
        'uuid': challenge_uuid,
        'title': challenge_name,
        'type': challenge_type,
        'status': 'OPEN',
        'start_time': start_time.timestamp(),
        'end_time': end_time.timestamp(),
        'pay_in': payin_coins,
        'auto_accept': auto_accept
    }

    embed = await _get_challenge_preview(final_challenge)

    await response_message.edit(
        content=f"{message.author.mention}, confirm this challenge or abort.",
        embed=embed)


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
