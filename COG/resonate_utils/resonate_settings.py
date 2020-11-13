"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8 feel free to make it.

This module contains configuration for music player.

"""

from dataclasses import dataclass
import os


@dataclass()
class Configs(object):
    # MUSIC_PLAYER_CONFIGS
    DEFAULT_VOLUME: int = 50
    MAX_VOLUME: int = 100

    # SEARCH_ENGINE_CONFIGS
    SONG_RESULTS_LIMIT: int = 5

    # MUSIC_SERVER_CONFIGS
    MUSIC_HOST: str = "lava-link-server.herokuapp.com"
    MUSIC_PORT: int = 80
    REST_URI: str = "http://lava-link-server.herokuapp.com"
    MUSIC_SERVER_PW: str = os.environ.get('MUSIC_SERVER_PW')
    MUSIC_SERVER_REGION: str = "na"

    # MUSIC_CHANNEL_CONFIGS
    RESTRICT_CMDS_TO_MUSIC_CHANNEL: bool = False
    MUSIC_CMD_CHANNEL: int = 769254977863417887
    BOT_LEAVE_DELAY: int = 10
    NOW_PLAYING_GIF_URL: str = r"https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fmusic-player%2Fnowplaying.gif?alt=media&token=356810ce-8fdc-4854-8f81-19453abba445"
    INITIAL_CONNECT_GIF_URL: str = r"https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fmusic-player%2Ffirstconnect.gif?alt=media&token=a188374e-6c63-4054-9226-5b54d29392df"

    # PLAYER_UTILITIES_CONFIGS
    PAGINATION_LIMIT: int = 6
    UPCOMING_TRACKS_LIMIT: int = 2

    # CUSTOM_EMOJIS
    YT: str = "<:yt:775306162622955611> YouTube"
    SC: str = "<:sc:775309222032048178> SoundCloud"
    R_BEATS: str = "<:resonate:775316195745726504>"

    # Logging
    STDOUT_LOGS: bool = True
    WRITE_LOGS: bool = True
    LOG_FILE: str = "logs/music.log"


# Commands and their aliases
CMD_ALIASES = {
    'connect': [
        'join',
    ],
    'leave': [
      'lv'
    ],
    'play': [
        'p',
    ],
    'stop': [
        's',
    ],
    'next': [
        '+1',
    ],
    'previous': [
        '-1',
    ],
    'pause': [
        'ps',
    ],
    'remove': [
        'rm',
    ],
    'playlist': [
        'pl',
    ],
    'seek': [
        'sk',
    ],
    'volume': [
        'v',
    ],
    'information': [
        'info',
    ],
    'repeat': [
        'rp'
    ],
    'reset_playlist': [
        'rstpl'
    ],
    'shuffle': [
        'shfl'
    ],
    'player_mute': [
        'm'
    ],
    'player_unmute': [
        'um'
    ],

}

__all__ = [
    "Configs", "CMD_ALIASES"
]
