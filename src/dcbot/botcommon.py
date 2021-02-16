import functools
from enum import Enum, unique
from src.database import dbcommon
from src.dcbot import client
from src.translation import transget

# Server Keys
key_bot_mainserver = "bot_main_server"

# Singlechannel keys
key_bot_adminchannel = "bot_admin_channel"
key_bot_logchannel = "bot_log_channel"
key_bot_applychannel = "bot_gapply_channel"
key_bot_applydestchannel = "bot_gapplydest_channel"
key_bot_splashchannel = "bot_gsplash_channel"
key_bot_newpublicvoicechannel = "bot_newpublicvoice_channel"
key_bot_newprivatevoicechannel = "bot_newprivatevoice_channel"

# Multichannel keys
key_bot_userchannel = "bot_user_botchannel"

# Permission keys
key_permlevel_fullmuted = -10
key_permlevel_restricted = -1
key_permlevel_user = 0
key_permlevel_elevated = 1
key_permlevel_moderator = 10
key_permlevel_supermod = 50
key_permlevel_admin = 90
key_permlevel_owner = 100

# More bot settings keys
key_bot_init_stage = "bot_init_stage"
key_bot_prefix = "bot_shortprefix"
default_user_preferred_language = "de"

key_color_info = 0xDEDEDE
key_color_muted = 0x2E2E2E
key_color_okay = 0x7DDE4D
key_color_warning = 0xEFA43D
key_color_danger = 0xEF3D3D

# Common quick-access variables for the bot, may be None if not initialized yet
main_guild = None

# Voice channel object:
bot_voice_channels = []

# Currently registered commands
registered_bot_commands = []
# Currently registered message processors
registered_message_processors = []

# Hypixel API
hypixel_api = None

# Is the bot currently shutting down? This is used for disabling events
# while cleaning up the server and is set from inside the 'stop' command
is_bot_stopping = False


# Stat types for Hypixel skyblock skill leveling challenges
# Name "Skill leveling challenges" is bad - it supports all stats,
# not only skills
@unique
class StatTypes(Enum):
    FARMING = "experience_skill_farming"
    COMBAT = "experience_skill_combat"
    MINING = "experience_skill_mining"
    FORAGING = "experience_skill_foraging"
    FISHING = "experience_skill_fishing"
    ENCHANTING = "experience_skill_enchanting"
    ALCHEMY = "experience_skill_alchemy"
    TAMING = "experience_skill_taming"
    CARPENTRY = "experience_skill_carpentry"
    RUNECRAFTING = "experience_skill_runecrafting"
    CATACOMBS = "dungeons/dungeon_types/catacombs/experience"
    SLAYER_REVENANT = "slayer_bosses/zombie/xp"
    SLAYER_TARANTULA = "slayer_bosses/spider/xp"
    SLAYER_SVEN = "slayer_bosses/wolf/xp"

    @classmethod
    def has_value(cls, value):
        return str(value) in cls._value2member_map_

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return f"{self.value}"


async def get_member_by_id_or_ping(selector):
    user_id = selector.lstrip("<@!").lstrip("<@").rstrip(">")
    guild = main_guild
    try:
        member = guild.get_member(user_id)
        if member is None:
            member = await guild.fetch_member(user_id)
        return member
    except Exception:
        return None


async def get_channel_by_id_or_ping(selector):
    channel_id = selector.lstrip("<#").rstrip(">")
    guild = main_guild
    try:
        channel = guild.get_channel(channel_id)
        if channel is None:
            channel = await client.fetch_channel(channel_id)
        return channel
    except Exception:
        return None


# Decorator for permission constraints on commands
def requires_perm_level(level):

    def decorator(func):
        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            if args[2].user_permission_level >= level:
                return await func(*args, **kwargs)
            else:
                return None
        return decorated
    return decorator


# Decorator for channel constraints on commands
def requires_channel(channel_key_list):
    def decorator(func):
        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            full_channel_list = []
            for channel_key in channel_key_list:
                channels = dbcommon.get_channel_ids_from_key(channel_key)
                full_channel_list = full_channel_list + channels
            full_channel_list = list(dict.fromkeys(full_channel_list))
            if full_channel_list == [None] or full_channel_list == [] or \
                    full_channel_list is None:
                return await func(*args, **kwargs)
            full_channel_list = [int(x) for x in full_channel_list]
            if args[0].channel.id in full_channel_list:
                return await func(*args, **kwargs)
        return decorated
    return decorator


async def trytolog(message, arg_stack, botuser, embed):
    logchannel_id = dbcommon.get_bot_setting(key_bot_logchannel, 0)
    try:
        logchannel = await client.fetch_channel(logchannel_id)
    except Exception:
        await message.channel.send(
            transget('dcbot.log.error.channel', botuser.user_pref_lang))
        await message.channel.send(embed=embed)
        return
    else:
        if logchannel is None:
            await message.channel.send(
                transget('dcbot.log.error.channel', botuser.user_pref_lang))
            await message.channel.send(embed=embed)
            return
        else:
            await logchannel.send(embed=embed)
            return
