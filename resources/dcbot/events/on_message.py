from resources.dcbot import client
from resources.dcbot import botcommon
from resources.translation import transget
from resources.database import dbcommon
from resources.database import sqlsession
from resources.database.models.botuser import BotUser

DD_MAX_INIT_STAGE = 3


def is_command(message_content):
    shortprefix = dbcommon.get_bot_setting('bot_short_prefix', '$')
    if message_content.startswith("<@!" + str(client.user.id) + "> ") or \
            message_content.startswith("<@" + str(client.user.id) + "> ") or \
            message_content.startswith(shortprefix):
        return True
    return False


def get_processed_argstack(message):
    if message.startswith("<@!" + str(client.user.id) + "> ") or \
            message.startswith("<@" + str(client.user.id) + "> "):
        tempmsg = message.split(' ')
        return list(filter(None, tempmsg[1:]))
    shortprefix = dbcommon.get_bot_setting('bot_short_prefix', '$')
    if message.startswith(shortprefix):
        tempmsg = message[1:].strip().split(' ')
        return list(filter(None, tempmsg))


async def on_message_init_mode(message, cmd_arg_stack, init_stage):

    if init_stage == 0:
        if cmd_arg_stack[0] == "init":
            newuser = BotUser(
                user_discord_id=message.author.id,
                user_pref_lang=botcommon.default_user_preferred_language,
                user_permission_level=botcommon.key_permlevel_owner)
            sqlsession.add(newuser)
            sqlsession.commit()
            from resources.dcbot.commands import set_admin_channel
            await set_admin_channel.invoke(
                message,
                [
                    'set_admin_channel',
                    '<#' + str(message.channel.id) + '>'],
                newuser)
            dbcommon.set_bot_setting(botcommon.key_bot_init_stage, 1)
            await message.channel.send(transget(
                'init.stage0.successful',
                newuser.user_pref_lang))
            await message.channel.send(transget(
                    'init.stage1.intro',
                    newuser.user_pref_lang))

    elif init_stage == 1:
        currentuser = dbcommon.get_user_or_create(message.author.id)
        if cmd_arg_stack[0] == "init":
            await message.channel.send(transget(
                'init.stage1.intro',
                currentuser.user_pref_lang))

        elif cmd_arg_stack[0] == "set_bot_prefix":
            from resources.dcbot.commands import set_bot_prefix
            if await set_bot_prefix.invoke(
                    message,
                    cmd_arg_stack,
                    currentuser):
                dbcommon.set_bot_setting(botcommon.key_bot_init_stage, 2)
                await message.channel.send(transget(
                    'init.stage1.successful',
                    currentuser.user_pref_lang))
                await message.channel.send(transget(
                    'init.stage2.intro',
                    currentuser.user_pref_lang))

    elif init_stage == 2:
        currentuser = dbcommon.get_user_or_create(message.author.id)
        if cmd_arg_stack[0] == "init":
            await message.channel.send(transget(
                'init.stage2.intro',
                currentuser.user_pref_lang))

        elif cmd_arg_stack[0] == "set_log_channel":
            from resources.dcbot.commands import set_log_channel
            if await set_log_channel.invoke(
                    message,
                    cmd_arg_stack,
                    currentuser):
                dbcommon.set_bot_setting(botcommon.key_bot_init_stage, 3)
                await message.channel.send(transget(
                    'init.stage2.successful',
                    currentuser.user_pref_lang))
                await message.channel.send(transget(
                    'init.stage3.intro',
                    currentuser.user_pref_lang))

    elif init_stage == 3:
        currentuser = dbcommon.get_user_or_create(message.author.id)
        if cmd_arg_stack[0] == "init":
            await message.channel.send(transget(
                'init.stage3.intro',
                currentuser.user_pref_lang))

        if cmd_arg_stack[0] == "add_user_botchannel":
            from resources.dcbot.commands import add_user_botchannel
            if await add_user_botchannel.invoke(
                    message,
                    cmd_arg_stack,
                    currentuser):
                dbcommon.set_bot_setting(botcommon.key_bot_init_stage, 4)
                await message.channel.send(transget(
                    'init.stage3.successful',
                    currentuser.user_pref_lang))
                await message.channel.send(transget(
                    'init.completed',
                    currentuser.user_pref_lang))

    elif init_stage == 4:
        pass


async def on_message_command_mode(message, cmd_arg_stack):
    print("In command mode!")
    pass


async def process_non_command_messages(message):
    print("In message process mode!")
    pass


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    cmd_arg_stack = get_processed_argstack(message.content)

    init_stage = int(dbcommon.get_bot_setting(botcommon.key_bot_init_stage, 0))
    if init_stage <= DD_MAX_INIT_STAGE:
        await on_message_init_mode(message, cmd_arg_stack, init_stage)
    elif is_command(message.content):
        await on_message_command_mode(message, cmd_arg_stack)
    else:
        await process_non_command_messages(message)
