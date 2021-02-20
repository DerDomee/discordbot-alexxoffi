from asyncio import TimeoutError
from datetime import datetime, timedelta
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


async def _get_available_challenges(
        message, arg_stack, botuser, response_message):
    all_tracked_challenges = botcommon.challenge_scheduler.getAllTasks()
    open_challenges = []
    for challenge in all_tracked_challenges:
        if challenge.status == botcommon.ChallengeStatus.OPEN:
            open_challenges.append(challenge)
    if len(open_challenges) == 0:
        await response_message.edit(
            content=f"{message.author.mention}, there are no open challenges "
            + "you can currently join.")
        return False
    return open_challenges


async def _get_minecraft_name(message, arg_stack, botuser, response_message):
    await response_message.edit(
        content=f"{message.author.mention}, please enter your Minecraft "
        + "username")

    def mcnamemsgcheck(mcnamemessage):
        return mcnamemessage.author.id == message.author.id and \
            mcnamemessage.channel.id == message.channel.id

    mc_uuid = None
    mc_name = None
    while mc_uuid is None:
        try:
            mcnamemessage = await client.wait_for(
                'message', check=mcnamemsgcheck, timeout=30.0)
        except TimeoutError:
            await response_message.edit(
                content=f"{message.author.mention}, session closed!")
            return False, False
        else:
            entered_name = mcnamemessage.content
            await mcnamemessage.delete()
            await response_message.edit(
                content=f"{message.author.mention}, fetching...")
            uuidrequest = SBAPIRequest(RequestType.GETUUID, (entered_name,))
            uuid = await botcommon.hypixel_api.request(uuidrequest, 5)
            if 'dd_error' in uuid:
                await response_message.edit(
                    content=f"{message.author.mention}, the user "
                    + f"'{entered_name}' does not exist. Please enter your "
                    + "real minecraft username!")
                continue
            mc_uuid = uuid['id']
            mc_name = entered_name
    return mc_name, mc_uuid


async def _get_available_profiles(
        message, arg_stack, botuser, response_message, mcuuid):
    profilesrequest = SBAPIRequest(RequestType.PROFILES, (mcuuid,))
    profiles = await botcommon.hypixel_api.request(profilesrequest, 10)
    if 'dd_error' in profiles:
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
            'reaction_add', check=pselect_check, timeout=30.0)
    except TimeoutError:
        await response_message.clear_reactions()
        await response_message.edit(
            content=f"{message.author.mention}, session closed!")
        return False
    else:
        selected_profile = available_profiles[NUMBER_REACTIONS.index(
            str(reaction))]
        await response_message.clear_reactions()
        return selected_profile
    return False


async def _get_selected_challenge(
        message, arg_stack, botuser, response_message, available_challenges):
    if len(available_challenges) == 1:
        return available_challenges[0]
    available_text = f"{message.author.mention}, please select the " \
        + "challenge you want to join:"
    for index, challenge in enumerate(available_challenges):
        emote = NUMBER_REACTIONS[index]
        chall_title = challenge.title
        chall_type = challenge.type.name
        available_text += f"\n{emote} `{chall_title}`, {chall_type}"
    await response_message.edit(content=available_text)
    for i in range(len(available_challenges)):
        await response_message.add_reaction(NUMBER_REACTIONS[i])

    def cselect_check(reaction, user):
        return user.id == message.author.id and \
            reaction.message.id == response_message.id and str(
                reaction) in NUMBER_REACTIONS[:len(available_challenges)]
    try:
        reaction, reactionuser = await client.wait_for(
            'reaction_add', check=cselect_check, timeout=30.0)
    except TimeoutError:
        await response_message.clear_reactions()
        await response_message.edit(
            content=f"{message.author.mention}, session closed!")
        return False
    else:
        selected_challenge = available_challenges[NUMBER_REACTIONS.index(
            str(reaction))]
        await response_message.clear_reactions()
        return selected_challenge
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


async def _get_channel_to_announce(
        message, arg_stack, botuser, response_message):
    await response_message.edit(
        content=f"{message.author.mention}, mention a channel where the "
        + "challenge will be announced.")

    def announcemsgcheck(announcemessage):
        return announcemessage.channel.id == message.channel.id and \
            announcemessage.author.id == message.author.id

    chosen_channel = None
    while chosen_channel is None:
        try:
            announcemessage = await client.wait_for(
                'message', check=announcemsgcheck, timeout=60.0)
        except TimeoutError:
            await response_message.edit(
                content=f"{message.author.mention}, session closed!")
            return False
        else:
            entered_channel = announcemessage.content
            await announcemessage.delete()
            channel = await botcommon.get_channel_by_id_or_ping(
                entered_channel)
            if channel is None:
                await response_message.edit(
                    content=f"{message.author.mention}, please enter a valid "
                    + "channel where the challenge will be announced.")
                continue
            chosen_channel = channel
    return chosen_channel


def _determine_entries_closing_time(start_time, auto_accept):

    if auto_accept:
        return start_time + timedelta(minutes=-15)
    else:
        return start_time + timedelta(hours=-1)


async def _get_challenge_preview(challenge, announcement_channel):
    embed = Embed(
        title=challenge.title,
        description=f"UUID: `{challenge.uuid}`")
    embed.add_field(
        name="Challenge Type",
        value=challenge.type.name,
        inline=True)
    embed.add_field(
        name="Status",
        value=challenge.status)
    embed.add_field(
        name="Entries close time",
        value=challenge.entries_close_time)
    embed.add_field(
        name="Start",
        value=challenge.start_time)
    embed.add_field(
        name="End",
        value=challenge.end_time)
    if challenge.pay_in == 0:
        embed.add_field(name="Pay-In", value="Not needed")
    else:
        embed.add_field(name="Pay-In", value=challenge.pay_in)
    embed.add_field(
        name="Auto-Accept on join",
        value=challenge.auto_accept)
    embed.add_field(
        name="Announcement channel",
        value=announcement_channel.mention)
    return embed


async def _confirm_challenge_creation(
        message, arg_stack, botuser, response_message, final_challenge,
        announcement_channel):
    embed = await _get_challenge_preview(final_challenge, announcement_channel)

    await response_message.edit(
        content=f"{message.author.mention}, confirm this challenge or abort.",
        embed=embed)
    await response_message.add_reaction("✅")
    await response_message.add_reaction("❌")

    def confirmation_check(reaction, user):
        return user.id == message.author.id and \
            reaction.message.id == response_message.id and str(reaction) in \
            ['✅', '❌']

    try:
        reaction, reactionuser = await client.wait_for(
            'reaction_add', check=confirmation_check, timeout=30.0
        )
    except TimeoutError:
        await response_message.clear_reactions()
        await response_message.edit(
            content=f"{message.author.mention}, session closed!",
            embed=None)
        return False
    else:
        await response_message.clear_reactions()
        if str(reaction) == "✅":
            await response_message.edit(
                content=f"{message.author.mention}, created challenge!,",
                embed=None)
            return True
        else:
            await response_message.edit(
                content=f"{message.author.mention}, challenge creation "
                + "aborted!",
                embed=None)
            return False

    await response_message.clear_reactions()
    return False


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

    announcement_channel = await _get_channel_to_announce(
        message, arg_stack, botuser, response_message)
    if announcement_channel is False:
        return False

    challenge_uuid = str(uuid.uuid4())
    entries_close_time = _determine_entries_closing_time(
        start_time, auto_accept)

    final_challenge = botcommon.ChallengeEvent({
        'uuid': challenge_uuid,
        'title': challenge_name,
        'type': challenge_type,
        'status': botcommon.ChallengeStatus.OPEN,
        'start_time': start_time,
        'entries_close_time': entries_close_time,
        'end_time': end_time,
        'pay_in': payin_coins,
        'auto_accept': auto_accept,
        'announcement_channel_id': announcement_channel.id,
        'players': []
    })

    confirmation = await _confirm_challenge_creation(
        message, arg_stack, botuser, response_message, final_challenge,
        announcement_channel)
    if confirmation is False or confirmation is None:
        return False

    announcement_message = await announcement_channel.send(
        embed=final_challenge.get_embed())

    final_challenge.announcement_message_id = announcement_message.id

    botcommon.challenge_scheduler.addTask(final_challenge)


async def _await_join_confirmation(
        message, arg_stack, botuser, response_message, selected_profile,
        selected_challenge, mcuuid, mcname):
    stat_preview = botcommon.get_profile_challenge_stat(
        selected_profile, mcuuid, selected_challenge.type)
    if stat_preview is None:
        await response_message.edit(
            content=f"{message.author.mention}, your API seems to be "
            + "disabled. You cannot join with disabled API and you will get "
            + "disqualified if you disable your API before or during the "
            + "event!")
        return False
    profilename = selected_profile['cute_name']
    challname = selected_challenge.title
    embed = Embed(title="Confirm your entry")
    embed.add_field(name="MC-Name", value=mcname, inline=False)
    embed.add_field(name="Profile", value=profilename, inline=False)
    embed.add_field(name="Challenge", value=challname, inline=False)
    embed.add_field(name="Stat preview", value=stat_preview, inline=False)
    embed.add_field(
        name="Warning",
        value="If you disable your API at any point from now until the end of "
        + "the event, you will get disqualified!")

    await response_message.edit(
        content=f"{message.author.mention}", embed=embed)
    await response_message.add_reaction("✅")
    await response_message.add_reaction("❌")

    def confirmation_check(reaction, user):
        return user.id == message.author.id and \
            reaction.message.id == response_message.id and str(reaction) in \
            ['✅', '❌']

    try:
        reaction, reactionuser = await client.wait_for(
            'reaction_add', check=confirmation_check, timeout=60.0
        )
    except TimeoutError:
        await response_message.clear_reactions()
        await response_message.edit(
            content=f"{message.author.mention}, session closed!",
            embed=None)
        return False
    else:
        await response_message.clear_reactions()
        if str(reaction) == "✅":
            await response_message.edit(
                content=f"{message.author.mention}, joining...", embed=None)
            return True
        else:
            await response_message.edit(
                content=f"{message.author.mention}, aborting...", embed=None)
            return False

    await response_message.clear_reactions()
    return False


async def _join_challenge(message, arg_stack, botuser):
    response_message = await message.channel.send(
        f"{message.author.mention}, preparing...")

    available_challenges = await _get_available_challenges(
        message, arg_stack, botuser, response_message)
    if available_challenges is False:
        return False

    mcname, mcuuid = await _get_minecraft_name(
        message, arg_stack, botuser, response_message)
    if mcname is False:
        return False

    available_profiles = await _get_available_profiles(
        message, arg_stack, botuser, response_message, mcuuid)
    if available_profiles is False:
        return False

    selected_profile = await _get_selected_profile(
        message, arg_stack, botuser, response_message, available_profiles)
    if selected_profile is False:
        return False

    selected_challenge = await _get_selected_challenge(
        message, arg_stack, botuser, response_message, available_challenges)
    if selected_challenge is False:
        return False

    confirmation = await _await_join_confirmation(
        message, arg_stack, botuser, response_message, selected_profile,
        selected_challenge, mcuuid, mcname)
    if confirmation is None or confirmation is False:
        return False

    player_data = {
        'mcname': mcname,
        'mcuuid': mcuuid,
        'discordid': message.author.id,
        'state': "ACCEPTED" if selected_challenge.auto_accept else "PENDING"
    }
    selected_challenge.players.append(player_data)
    await selected_challenge.update_challenge_embed()

    await response_message.edit(
        content=f"{message.author.mention}, successfully joined the "
        + "challenge!")

    return True


async def _list_challenges(message, arg_stack, botuser):
    available_challenges = botcommon.challenge_scheduler.getAllTasks()
    if len(available_challenges) == 0:
        await message.channel.send(
            f"{message.author.mention}, there are no tracked events.")
        return True
    available_text = f"{message.author.mention}, currently tracked events:"
    for challenge in available_challenges:
        available_text += f"\n {challenge.title} (`{challenge.uuid}`) - "
        available_text += f"`{challenge.type.name}`, `{challenge.status}`"
    await message.channel.send(available_text)
    return True


async def _accept_player(message, arg_stack, botuser):
    # TODO: Check if author is admin/moderator
    # TODO: Ask Author for mc-name/mc-uuid/discord-ping/discord-id of user
    # TODO: Check if this user is currently trying to attend to a challenge
    # TODO: If multiple challenges are available, let Author choose which
    # TODO: Update this player and accept him in the challenge
    # TODO: Update the challenges announcement embed
    return True


async def _get_pending_players(message, arg_stack, botuser):
    pending_players = []
    for challenge in botcommon.challenge_scheduler.getAllTasks():
        if challenge.status is botcommon.ChallengeStatus.OPEN or \
                challenge.status is botcommon.ChallengeStatus.PENDING:
            for player in challenge.get_pending_players():
                pending_players.append((player, challenge))
    if len(pending_players) == 0:
        await message.channel.send(
            f"{message.author.mention}, there are no pending players in any "
            + "currently tracked event.")
        return True
    playertext = ""
    for player in pending_players:
        mcname = player[0]['mcname']
        challtitle = player[1].title
        challuuid = player[1].uuid
        playertext += f"\n`{mcname}` in `{challtitle}` (`{challuuid}`)"

    await message.channel.send(
        f"{message.author.mention}, currently pending players:{playertext}")

    return True


async def _get_tracked_challenge_by_uuid(
        message, arg_stack, botuser, response_message):
    await response_message.edit(
        content=f"{message.author.mention}, enter the UUID of the challenge "
        + "you want to discard")

    def uuidmsgcheck(uuidmessage):
        return uuidmessage.channel.id == message.channel.id and \
            uuidmessage.author.id == message.author.id

    challenge = None
    while challenge is None:
        try:
            uuidmessage = await client.wait_for(
                'message', check=uuidmsgcheck, timeout=60.0)
        except TimeoutError:
            await response_message.edit(
                content=f"{message.author.mention}, session closed!")
            return False
        else:
            entered_uuid = uuidmessage.content
            await uuidmessage.delete()
            challenge = botcommon.challenge_scheduler.getTask(entered_uuid)
            if challenge is None:
                await response_message.edit(
                    content=f"{message.author.mention}, no event with this "
                    + "uuid is currently tracked. Aborting.")
                return False
    return challenge


async def _discard_challenge(message, arg_stack, botuser):
    response_message = await message.channel.send(
        f"{message.author.mention}, preparing...")

    selected_challenge = await _get_tracked_challenge_by_uuid(
        message, arg_stack, botuser, response_message)
    if selected_challenge is False:
        return False
    await selected_challenge.discard()
    await response_message.edit(
        content=f"{message.author.mention}, challenge "
        + f"'{selected_challenge.title}' was discarded and untracked.")
    return True


async def _get_player_status(message, arg_stack, botuser):
    # TODO: Get all currently tracked challenges that the player is found in
    # TODO: Show the current status of the player for all challenges
    return False


async def _get_player_results(message, arg_stack, botuser):
    # TODO: Ask user for challenge UUID
    # TODO: Find challenge in archived data or return if not found
    # TODO: When player did not joined this event, insult the user and return
    # TODO: When player has state "PENDING", "DISQUALIFIED" or "ERRORED",
    #       Show a message explaining his state and return
    # TODO: Actually show the result of the player in this challenge
    return False


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
@botcommon.requires_channel(CMD_METADATA['required_channels'])
async def invoke(message, arg_stack, botuser):
    if len(arg_stack) >= 2:
        if arg_stack[1].lower() == "create":
            return await _create_challenge(message, arg_stack, botuser)

        if arg_stack[1].lower() == "join":
            return await _join_challenge(message, arg_stack, botuser)

        if arg_stack[1].lower() == "list":
            return await _list_challenges(message, arg_stack, botuser)

        if arg_stack[1].lower() == "accept":
            return await _accept_player(message, arg_stack, botuser)

        if arg_stack[1].lower() == "discard":
            return await _discard_challenge(message, arg_stack, botuser)

        if arg_stack[1].lower() == "pending":
            return await _get_pending_players(message, arg_stack, botuser)

        if arg_stack[1].lower() == "status":
            return await _get_player_status(message, arg_stack, botuser)

        if arg_stack[1].lower() == "results":
            return await _get_player_results(message, arg_stack, botuser)

    await message.channel.send("Wrong syntax - see `help chall` for usage")


async def get_help(argstack, botuser, sp):
    embed = Embed(
        title="Hypixel Skyblock skill-leveling events",
        description="Manage or attend to skill-leveling events")
    embed.add_field(
        name="Syntax",
        value=f"`{sp}challenge create` - Create a new challenge event (Admins "
              + f"only)\n`{sp}challenge join` - Join a challenge event"
              + f"\n`{sp}challenge list` - List all available events"
              + f"\n`{sp}challenge accept` - Accept a player entry in an "
              + "event (Admins only)"
              + f"\n`{sp}challenge pending` - List players currently waiting "
              + "for entry seat approval"
              + f"\n`{sp}challenge discard` - Discard an event, as if it "
              + "never happened (Admins only)"
              + f"\n`{sp}challenge status` - See if you have a seat in an"
              + "event and watch your status"
              + f"\n`{sp}challenge results` - See your results in a past "
              + "event")
    return [embed]
