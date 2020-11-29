"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8 feel free to make it.

This module contains configuration for music player.

"""

from dataclasses import dataclass


@dataclass()
class Configs(object):

    # Bot Configs
    SHOW_TYPING: bool = False
    TYPING_INTERVAL: float = 0.1  # In seconds

    # MUSIC_PLAYER_CONFIGS
    DEFAULT_VOLUME: int = 50
    MAX_VOLUME: int = 100

    # SEARCH_ENGINE_CONFIGS
    SONG_RESULTS_LIMIT: int = 5

    MUSIC_HOST: str = "127.0.0.1"
    MUSIC_PORT: int = 2333
    REST_URI: str = "http://127.0.0.1:2333"
    MUSIC_SERVER_PW: str = os.environ.get('MUSIC_SERVER_PW')
    MUSIC_SERVER_REGION: str = "na"

    # MUSIC_CHANNEL_CONFIGS
    RESTRICT_CMDS_TO_MUSIC_CHANNEL: bool = True
    MUSIC_CMD_CHANNEL: int = 769254977863417887
    BOT_LEAVE_DELAY: int = 10
    NOW_PLAYING_GIF_URL: str = "https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fmusic-player%2Fnow_palying%2Feq_effects.gif?alt=media&token=412acdcf-8bf3-4673-855c-2e35f66a04cf"
    INITIAL_CONNECT_GIF_URL: str = "https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fmusic-player%2Ffirst_connect%2Ffirst_connect_1.gif?alt=media&token=f60a80ee-0124-42ab-9cb1-a139e0a8f83b"

    # PLAYER_UTILITIES_CONFIGS
    PAGINATION_LIMIT: int = 6
    UPCOMING_TRACKS_LIMIT: int = 2

    # CUSTOM_EMOJIS (These are optional but if set, the emojis will be used as icons on embeds)
    YT: str = "<:yt:775306162622955611> YouTube"
    SC: str = "<:sc:775309222032048178> SoundCloud"
    R_BEATS: str = "<:resonate:782280388332355586>"

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
