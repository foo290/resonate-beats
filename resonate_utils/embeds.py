import discord
from .settings import configs
from .track_utils import show_track_duration
from .decorators import export
import datetime as dt

COMMAND_PREFIX = configs.COMMAND_PREFIX
BOT_NAME = configs.BOT_NAME
NOW_PLAYING_GIF_URL = configs.NOW_PLAYING_GIF_URL
INITIAL_CONNECT_GIF_URL = configs.INITIAL_CONNECT_GIF_URL


@export
class MusicEmbeds:
    def __init__(self):
        pass

    @staticmethod
    def show_state(state):
        embed = discord.Embed(
            description=state,
        )
        return embed

    @staticmethod
    def show_player_info(*args):
        cp, ct, ct_index, requester, rptmode, c_vol, m_vol, tracks = args
        embed = discord.Embed(
            title='Info Panel',
            description='general information of current player.',
            timestamp=dt.datetime.utcnow()
        )
        embed.add_field(
            name='General Info. ',
            value=f"**Current Position** : {cp}\n"
                  f"**Current Track** : {ct}\n"
                  f"**Current Track Index** : {ct_index} (Actual index in Queue.)\n"
                  f"**Repeat Mode** : {rptmode}\n"
                  f"**Current Volume** : {c_vol}\n"
                  f"**Max Volume** : {m_vol}\n",
            inline=False
        )
        embed.add_field(
            name="Songs snap (upto 10 only...)",
            value='\n'.join([f"**{i + 1} ->** {t}" for i, t in enumerate(tracks)]),
            inline=False
        )
        return embed

    @staticmethod
    def track_added(track, position, addedby, icon, color, search_engine=None):
        embed = discord.Embed(
            title='Track Added! ✅ ',
            description='A new track is added in queue... 🎧',
            color=color,
            timestamp=dt.datetime.utcnow()
        )
        embed.add_field(name='Track Name :', value=f"🎶 [{track.title}]({track.info.get('uri', '')})", inline=False)
        embed.add_field(name='Added at : ', value=position)
        embed.add_field(name='Duration :', value=f'{show_track_duration(track.length)}')
        if search_engine:
            embed.add_field(name='Found on : ', value=f"{search_engine}")
        thumbnail = track.thumb
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        embed.set_image(url=r'https://firebasestorage.googleapis.com/v0/b/discord-bot-294607.appspot.com/o/bot%2Fgifs%2Fother_gifs%2FAS_divider.gif?alt=media&token=9d5aa995-7a36-4cc5-b92e-a19bd5c03143')

        embed.set_footer(text=f"Added by : {addedby}", icon_url=icon)

        return embed

    @staticmethod
    def choose_track_embed(ctx, tracks, search_engine=None, show_limit=5):
        embed = discord.Embed(
            title=f'{search_engine}',
            description=(
                "\n\n".join(
                    f"**{i + 1}.** [{_t.title}]({_t.info.get('uri', '')}) ({show_track_duration(_t.length)})"
                    for i, _t in enumerate(tracks[:show_limit])
                )
            ),
            color=ctx.author.color,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_footer(text=f'Invoked by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)

        return embed

    @staticmethod
    def show_playlist(all_songs, currently_playing, upcoming_songs, showlimit=5, **kwargs):
        playlist_page = kwargs['page_stride'] - 1
        without_paginated = kwargs.get('full_playlist', [])

        embed = discord.Embed(
            title=f'🎵 Song Queue...',
            description=f'*Current Playlist* 🎵\n\n',
            # f'**Total Songs** : \n'
            # f'**Total Duration** : \n',
            colour=kwargs['color'],
            timestamp=dt.datetime.utcnow()
        )
        embed.add_field(
            name='Total Songs :',
            value=f'Song Count : {kwargs.get("playlist_length", "N/A")}'
        )
        embed.add_field(
            name='Total Duration :',
            value=f'Approx : {kwargs["total_duration"]} mins.'
        )
        embed.add_field(name='🎶 All Songs',
                        value="\n".join(
                            [
                                f"**{without_paginated.index(song) + 1}.** "
                                f"*[{song.title}]({song.info.get('uri', '')})* 🎶\n"
                                f"```Duration : {show_track_duration(song.length)}```"
                                for song in all_songs[playlist_page]
                            ]
                        ),
                        inline=False)
        embed.set_footer(
            text=f"Page : {playlist_page + 1} of {len(all_songs)}",
            icon_url=kwargs['requester_icon']
        )
        embed.add_field(
            name="Currently playing ",
            value=f"🔊 [{currently_playing.title}]({currently_playing.info.get('uri', '')})\n",
            inline=False
        )
        if upcoming_songs:
            embed.add_field(
                name="Coming Up Next! ",
                value="\n\n".join(f"📍 [{_t.title}]({_t.info.get('uri', '')})"
                                  for _t in upcoming_songs[:configs.UPCOMING_TRACKS_LIMIT]),
                inline=False
            )

        return embed

    @staticmethod
    def now_playing(track, display_name, icon, info, clr=discord.Color.blurple(), thumb=None, **kwargs):
        embed = discord.Embed(
            title=f"{configs.R_BEATS} Now Playing . . .",
            description=f"🔊 [{track}]({info.get('uri', '')})\n\n"
                        f"**Playing : ** {kwargs.get('current_song_index') + 1} of {kwargs.get('total_length')} songs.",
            colour=clr,
            timestamp=dt.datetime.utcnow(),
        )
        embed.set_footer(text=f'Requested by {display_name}', icon_url=icon)
        if thumb:
            embed.set_thumbnail(url=NOW_PLAYING_GIF_URL)
            embed.set_image(url=thumb)
        else:
            embed.set_image(url=NOW_PLAYING_GIF_URL)

        return embed

    @staticmethod
    def initial_connected(display_name, chanel_name, icon, clr):
        embed = discord.Embed(

            description='Thanks for inviting me to the party 🥳 Lets drop some beats. 🎛',
            color=clr,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_image(url=INITIAL_CONNECT_GIF_URL)
        embed.set_author(name=f"Connected to the {chanel_name} Successfully.")
        embed.set_footer(text=f'Requested by : {display_name}', icon_url=icon)
        return embed

    @staticmethod
    def show_info():
        ...
