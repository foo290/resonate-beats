"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This module is provides support for music configurations.

Abbreviation:
    --> settings groups : A dict is referred as settings group coz every dict contains settings related to
                          some specific task.

Every group of settings are dicts and joined in a single dict later in utils.configMapper.

These settings are accessed by "." (dot) operator with exact names like :
        config.MUSIC_HOST  ----> Gives host name

Once you define a new setting group as dict, add that in the Config class at bottom.
Remember these are dicts, Keys are unique in all settings groups as they are joined as one later.
Two settings groups cannot have same keys, even if they are different dicts here. For ex :
    > If "ACTIVITY_TYPE" is already used in "BOT_CONFIGS" settings group, it cannot be used in any other settings group.

"""

import os
from .configMapper import Config

# This bot uses Wavelink wrapper for lavalink server.
# MUSIC_SERVER_CONFIGS = {
#     # 'MUSIC_HOST': "lava-link-server.herokuapp.com",
#     'MUSIC_HOST': "127.0.0.1",
#     'MUSIC_PORT': 2333,
#     'REST_URI': "http://127.0.0.1:2333",
#     'MUSIC_SERVER_PW': "serverserveserverdata",
#     'MUSIC_SERVER_REGION': "na",
#     'MUSIC_SEARCH_ENGINE': "soundcloud",
# }

MUSIC_PLAYER_CONFIGS = {
    'DEFAULT_VOLUME': 50,
    'MAX_VOLUME': 100
}

SEARCH_ENGINE_CONFIGS = {
    'SONG_RESULTS_LIMIT': 5
}

MUSIC_SERVER_CONFIGS = {
    'MUSIC_HOST': "lava-link-server.herokuapp.com",
    'MUSIC_PORT': 80,
    'REST_URI': "http://lava-link-server.herokuapp.com",
    'MUSIC_SERVER_PW': "serverserveserverdata",
    'MUSIC_SERVER_REGION': "na",
    'MUSIC_SEARCH_ENGINE': "soundcloud",
}

MUSIC_CHANNEL_CONFIGS = {
    'RESTRICT_CMDS_TO_MUSIC_CHANNEL': False,
    'MUSIC_CMD_CHANNEL': 769254977863417887,
    'BOT_LEAVE_DELAY': 10,
    'NOW_PLAYING_GIF_URL': r"https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fmusic-player%2Fnowplaying.gif?alt=media&token=356810ce-8fdc-4854-8f81-19453abba445",
    'INITIAL_CONNECT_GIF_URL': r"https://i.gifer.com/7d20.gif",
}

PLAYER_UTILITIES_CONFIGS = {
    'PAGINATION_LIMIT': 6,
    'UPCOMING_TRACKS_LIMIT': 2,
}

CUSTOM_EMOJIS = {
    'YT': '<:yt:775306162622955611> YouTube',
    'SC': '<:sc:775309222032048178> SoundCloud',
    'R_BEATS': '<:resonate:775316195745726504>',

}

LOGGING = {
    'STDOUT_LOGS': True,
    'WRITE_LOGS': True,
    'LOG_FILE': 'logs/agness.log',
}

# Every settings group should be included here in order to be accessed internally.
configs = Config(
    LOGGING,
    SEARCH_ENGINE_CONFIGS,
    MUSIC_SERVER_CONFIGS,
    MUSIC_PLAYER_CONFIGS,
    MUSIC_CHANNEL_CONFIGS,
    PLAYER_UTILITIES_CONFIGS,
    CUSTOM_EMOJIS
)

__all__ = [
    'configs'
]