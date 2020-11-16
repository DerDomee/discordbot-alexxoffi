import re
from src.translation import transget
from src.dcbot import botcommon
from src.dcbot import client
from src.dcbot.events.voice_events import voicecommon

CMD_METADATA = {
    'required_permlevel': botcommon.key_permlevel_restricted,
    'required_channels': None}


async def toggle(message, arg_stack, botuser, channel_obj):
    if channel_obj['editcount'] >= 2:
        await message.channel.send(transget(
            "command.voice.edits_used_up",
            botuser.user_pref_lang))
        return False

    if channel_obj['type'] == "public":
        channel_obj['editcount'] += 1
        role = botcommon.main_guild.get_role(channel_obj['role'])
        overwrites = voicecommon.get_private_overwrites(role)
        vc = client.get_channel(channel_obj['voicechannel'])
        tc = message.channel
        await vc.edit(overwrites=overwrites['vc'])
        await tc.edit(overwrites=overwrites['tc'])
        await role.edit(name="vc-prv-" + message.author.display_name)
        if channel_obj['renamed'] is False:
            await vc.edit(name="Private by " + message.author.display_name)
            await tc.edit(name="Private by " + message.author.display_name)
        channel_obj['type'] = "private"
        await message.channel.send(transget(
            "command.voice.toggle.to_private.success",
            botuser.user_pref_lang))
        await message.channel.send(transget(
            "command.voice.edits_notice",
            botuser.user_pref_lang).format(
                current_edits=str(channel_obj['editcount']),
                remaining_edits=str(2 - channel_obj['editcount'])))
        return True
    else:
        channel_obj['editcount'] += 1
        role = botcommon.main_guild.get_role(channel_obj['role'])
        overwrites = voicecommon.get_public_overwrites(role)
        vc = client.get_channel(channel_obj['voicechannel'])
        tc = message.channel
        await role.edit(name="vc-pub-" + message.author.display_name)
        if channel_obj['renamed'] is False:
            await vc.edit(
                name="Public by " + message.author.display_name,
                overwrites=overwrites['vc'])
            await tc.edit(
                name="Public by " + message.author.display_name,
                overwrites=overwrites['tc'])
        else:
            await vc.edit(overwrites=overwrites['vc'])
            await tc.edit(overwrites=overwrites['tc'])
        channel_obj['type'] = "public"
        await message.channel.send(transget(
            "command.voice.toggle.to_public.success",
            botuser.user_pref_lang))
        await message.channel.send(transget(
            "command.voice.edits_notice",
            botuser.user_pref_lang).format(
                current_edits=str(channel_obj['editcount']),
                remaining_edits=str(2 - channel_obj['editcount'])))
        return True
    return False


async def name(message, arg_stack, botuser, channel_obj):
    if channel_obj['editcount'] >= 2:
        await message.channel.send(transget(
            "command.voice.edits_used_up",
            botuser.user_pref_lang))
        return False

    if len(arg_stack) <= 2:
        await message.channel.send(transget(
            "command.voice.name.missing_name_argument",
            botuser.user_pref_lang))
        return False

    new_name = " ".join(arg_stack[2:])
    new_name = re.sub('[^A-Za-z1-9\\s\\-]', '', new_name)
    new_name = (new_name[:20]) if len(new_name) > 20 else new_name
    tc = client.get_channel(channel_obj['textchannel'])
    vc = client.get_channel(channel_obj['voicechannel'])

    await tc.edit(name=new_name)
    await vc.edit(name=new_name)

    channel_obj['editcount'] += 1
    channel_obj['renamed'] = True

    await message.channel.send(transget(
        "command.voice.name.renamed",
        botuser.user_pref_lang).format(
            new_name=new_name))
    await message.channel.send(transget(
        "command.voice.edits_notice",
        botuser.user_pref_lang).format(
            current_edits=str(channel_obj['editcount']),
            remaining_edits=str(2 - channel_obj['editcount'])))


async def transfer(message, arg_stack, botuser, channel_obj):

    transfer_member = await botcommon.get_member_by_id_or_ping(arg_stack[2])
    if transfer_member is None:
        await message.channel.send(transget(
            'command.voice.transfer.user_not_found',
            botuser.user_pref_lang))
        return False

    if transfer_member.id == message.author.id:
        await message.channel.send(transget(
            'command.voice.transfer.self_not_permitted',
            botuser.user_pref_lang))
        return False

    channel_obj['owner'] = transfer_member.id
    previous_owner = message.author.mention
    new_owner = transfer_member.mention
    await message.channel.send(transget(
        'command.voice.transfer.successful').format(
            previous_mention=previous_owner,
            new_mention=new_owner))


async def invite(message, arg_stack, botuser, channel_obj):
    if channel_obj['type'] != "private":
        await message.channel.send(transget(
            'command.voice.invite.channel_not_private',
            botuser.user_pref_lang))
        return False

    invite_member = await botcommon.get_member_by_id_or_ping(arg_stack[2])
    if invite_member is None:
        await message.channel.send(transget(
            'command.voice.invite.user_not_found',
            botuser.user_pref_lang))
        return False

    if invite_member.id == message.author.id:
        await message.channel.send(transget(
            'command.voice.invite.self_not_permitted',
            botuser.user_pref_lang))
        return False

    role = botcommon.main_guild.get_role(channel_obj['role'])
    if role is None:
        await message.channel.send(transget(
            'command.voice.invite.rolecheck_failed',
            botuser.user_pref_lang))
        return False
    await invite_member.add_roles(role)
    return True


async def kick(message, arg_stack, botuser, channel_obj):
    if channel_obj['type'] != "private":
        await message.channel.send(transget(
            'command.voice.kick.channel_not_private',
            botuser.user_pref_lang))
        return False

    kick_member = await botcommon.get_member_by_id_or_ping(arg_stack[2])
    if kick_member is None:
        await message.channel.send(transget(
            'command.voice.kick.user_not_found',
            botuser.user_pref_lang))
        return False

    if kick_member.id == message.author.id:
        await message.channel.send(transget(
            'command.voice.kick.self_not_permitted',
            botuser.user_pref_lang))
        return False

    role = botcommon.main_guild.get_role(channel_obj['role'])
    if role is None:
        await message.channel.send(transget(
            'command.voice.kick.rolecheck_failed',
            botuser.user_pref_lang))
        return False

    await kick_member.remove_roles(role)
    await kick_member.move_to(channel=None)
    return True


async def close(message, arg_stack, botuser, channel_obj):
    await voicecommon.delete_channel(channel_obj)
    return True


@botcommon.requires_perm_level(level=CMD_METADATA['required_permlevel'])
async def invoke(message, arg_stack, botuser):

    channel_obj = voicecommon.get_channel_obj_by_owner(message.author)
    if channel_obj is None:
        return False

    # arg_stack[1] contains subcommand 'toggle/name/transfer/invite/kick/close'
    if len(arg_stack) <= 1:
        return False
    elif arg_stack[1] == 'toggle':
        if channel_obj['textchannel'] != message.channel.id:
            return False
        return await toggle(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'name':
        if channel_obj['textchannel'] != message.channel.id:
            return False
        return await name(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'transfer':
        if channel_obj['textchannel'] != message.channel.id:
            return False
        return await transfer(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'invite':
        return await invite(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'kick':
        if channel_obj['textchannel'] != message.channel.id:
            return False
        return await kick(message, arg_stack, botuser, channel_obj)
    elif arg_stack[1] == 'close':
        if channel_obj['textchannel'] != message.channel.id:
            return False
        return await close(message, arg_stack, botuser, channel_obj)
    else:
        pass
        # Print error for unknown command
