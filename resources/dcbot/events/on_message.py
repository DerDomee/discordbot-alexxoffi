from resources.dcbot import client
from resources.dcbot import botcommon
from resources.translation import transget
from resources.database import dbcommon
from resources.database import sqlsession
from resources.database.models.botuser import BotUser

DD_MAX_INIT_STAGE = 4


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
                'init_stage_0_successful',
                newuser.user_pref_lang))
            await message.channel.send(transget(
                    'init_stage_1_intro',
                    newuser.user_pref_lang))
    elif init_stage == 1:
        if cmd_arg_stack[0] == "init":
            # TODO: Show help message telling the user
            #       to use command 'set_bot_prefix'
            print("In Init stage 1")
        elif cmd_arg_stack[0] == "set_bot_prefix":
            # TODO: Simulate valid call of function 'set_bot_prefix',
            #       then setting 'init_stage' to 2.
            pass
    elif init_stage == 2:
        if cmd_arg_stack[0] == "init":
            # TODO: Show help message telling the user
            #       to use command 'set_log_channel'
            print("In Init stage 2")
        elif cmd_arg_stack[0] == "set_log_channel":
            # TODO: Simulate valid call of function 'set_log_channel',
            #       then setting 'init_stage' to 3
            pass
    elif init_stage == 3:
        if cmd_arg_stack[0] == "init":
            # TODO: Show help message telling the user
            #       to use command 'add_user_botchannel'
            print("In Init stage 3")
        if cmd_arg_stack[0] == "add_user_botchannel":
            # TODO: Simulate valid call of function 'add_user_botchannel',
            #       then setting 'init_stage' to 4
            pass
    elif init_stage == 4:
        pass


async def on_message_command_mode(message, cmd_arg_stack):
    pass


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    cmd_arg_stack = get_processed_argstack(message.content)

    init_stage = int(dbcommon.get_bot_setting(botcommon.key_bot_init_stage, 0))
    if init_stage <= DD_MAX_INIT_STAGE:
        await on_message_init_mode(message, cmd_arg_stack, init_stage)
    else:
        await on_message_command_mode(message, cmd_arg_stack)
