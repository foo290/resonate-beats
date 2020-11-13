"""
NOTE : This project follows PEP 8 Styling Guide. If anything is not according to PEP 8, feel free to make it.

This extension module is the whole brain of the music player.
Music player uses Lavalink and wavelink to stream music.
"""

import discord
import wavelink
import typing as t
import re
import asyncio
from discord.ext import commands
from AGNESS_BOT.bot.resonate_utils import (
    Configs,
    paginate,
    logger,
    MusicEmbeds,
    scale_to_10,
    Player,
    RepeatMode,
    check_valid_channel,
    show_track_duration,
    CMD_ALIASES
)

# Custom exceptions
from AGNESS_BOT.bot.resonate_utils import (
    AlreadyConnectedToChannel,
    NotVoiceChannel,
    QueueIsEmpty,
    InvalidRemoveIndex,
    PlayerIsAlreadyPaused,
    NoMoreTracks,
    NoPreviousTracks,
    InvalidRepeatMode,
    RestrictedCommandToMusicChannel
)

cooldown_warn = 0

putlog = logger.get_custom_logger(__name__)

REST_URI = Configs.REST_URI
MUSIC_HOST = Configs.MUSIC_HOST
MUSIC_PORT = Configs.MUSIC_PORT
MAX_VOLUME = Configs.MAX_VOLUME
DEFAULT_VOLUME = Configs.DEFAULT_VOLUME
MUSIC_SERVER_PW = Configs.MUSIC_SERVER_PW
MUSIC_SERVER_REGION = Configs.MUSIC_SERVER_REGION
BOT_LEAVE_CHANNEL_DELAY = Configs.BOT_LEAVE_DELAY
MUSIC_CHANNEL = Configs.MUSIC_CMD_CHANNEL
PAGINATION_LIMIT = Configs.PAGINATION_LIMIT


music_embeds = MusicEmbeds()

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|" \
            r"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

JUMP_REGEX = r"^([1-9][0-9]{0,2}|1000)$"
SEEK_REGEX = r'^[+|-]([1-9]|[1-5][0-9]|60)$'


class Music(commands.Cog, wavelink.WavelinkMixin):
    """
    This is the main class contains commands for music player. Every settings for player is been configured in
    Player command which is inherited from Player in utils.music_utils .
    """

    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())
        self.initial_connect_embed = None
        self.current_volume = DEFAULT_VOLUME
        self.cooldown = 10
        self.cooldown_lock = False
        self.cooldown_tries = 0
        self.music_channel = self.bot.get_channel(Configs.MUSIC_CMD_CHANNEL)
        self.song_index = 0  # used to play songs directly by no. This variable should be managed manually.

    @staticmethod
    def check_query_or_jump(q):
        try:
            int(q)
            if re.match(JUMP_REGEX, q):
                return True
            return False
        except ValueError:
            return False

    def get_player(self, obj):
        """
        A get player utility implemented to quickly grab the player either by ctx or guild.
        :param obj: Either ctx or guild
        :return: player
        """
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    async def cog_check(self, ctx):
        """
        This function ensures that music commands are not being used in DMs.
        :param ctx: Context passed by DC command
        :return: None
        """
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send('Music commands are not allowed in DMs')
            return False
        return True

    async def start_nodes(self):
        """
        Main Node function which declares and initialize the node to connect to lava link server.
        :return: None
        """
        putlog.debug('Starting Music Node...')
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": MUSIC_HOST,
                "port": MUSIC_PORT,
                "rest_uri": REST_URI,
                "password": MUSIC_SERVER_PW,
                "identifier": 'MAIN ',
                "region": MUSIC_SERVER_REGION,
                "heartbeat": 10
            }
        }
        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    async def remove_initial_connect_embed(self):
        """
        This method removes the gif/message sent first on joining the voice channel.
        :return: None
        """

        if self.initial_connect_embed:
            await self.initial_connect_embed.delete()
            self.initial_connect_embed = None
            return
        return

    @commands.command(name='connect_node')
    @check_valid_channel
    async def node_connect(self, ctx):
        await ctx.send('Connecting Node...')
        await self.start_nodes()
        await ctx.send('Node Connected!')

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        """
        This function triggers when the node is connected successfully to lava link server.
        :param node: The node defined in class
        :return: None
        """
        putlog.debug(f"Wavelink node {node.identifier} connected.      OK!")

    @commands.command(name='connect', aliases=CMD_ALIASES['connect'])
    @check_valid_channel
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        """
        :param ctx: context passed by DC command
        :param channel: An optional argument to pass discord channel.
        :return: None
        """

        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)

        embed = music_embeds.initial_connected(
            ctx.author.display_name,
            channel.name,
            ctx.author.avatar_url,
            ctx.author.color
        )
        self.initial_connect_embed = await ctx.send(embed=embed)
        await player.set_volume(DEFAULT_VOLUME)
        putlog.info('Bot has joined the voice channel.')

    @commands.command(name='disconnect', aliases=CMD_ALIASES['leave'])
    @check_valid_channel
    async def disconnect_command(self, ctx):
        """
        This function is used to disconnect the bot from voice channel.
        :param ctx: Context
        :return: None
        """
        putlog.warning('Disconnecting Node.')
        player = self.get_player(ctx)
        await ctx.send('Leaving...')
        await player.teardown()
        await ctx.send('Disconnected!')
        await player.delete_now_playing_embed()
        await self.remove_initial_connect_embed()
        putlog.warning('Node Disconnected by disconnect_command!')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        This is an event function which listens the events happening in the voice channel like member joined or leaves
        :param member: Members in the channel
        :param before: before state of joining of any member
        :param after: after state of joining of any member
        :return: None
        """
        if not member.bot and after.channel is None:
            await asyncio.sleep(BOT_LEAVE_CHANNEL_DELAY)  # After 10 seconds, bot will be removed
            if not [m for m in before.channel.members if not m.bot]:
                putlog.warning(
                    f'No human is in voice channel. DemonBot will leave the channel after : {BOT_LEAVE_CHANNEL_DELAY}s')
                await self.remove_initial_connect_embed()
                await self.get_player(member.guild).delete_now_playing_embed()
                await self.get_player(member.guild).teardown()
                putlog.warning(f'DemonBot left channel after {BOT_LEAVE_CHANNEL_DELAY}s coz no human was in there.')

    @wavelink.WavelinkMixin.listener('on_track_stuck')
    @wavelink.WavelinkMixin.listener('on_track_end')
    @wavelink.WavelinkMixin.listener('on_track_exception')
    async def on_player_stop(self, node, payload):
        """
        The control is passed to this function on any of the condition from above decorators.
        :param node:
        :param payload:
        :return:
        """
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            putlog.debug('Repeat single song mode activated. Playing current song on loop.')
            await payload.player.repeat_track()
        elif self.song_index != 0:
            putlog.debug(
                'Control received by play command after validating the command that its a song jump by number.')
            putlog.debug('Passing control to advance() method and setting self.song_index=0 again.')
            await payload.player.advance(self.song_index)
            self.song_index = 0
        else:
            putlog.debug('Command is not a song jump. Passing control to advance()')
            await payload.player.advance()

    async def manage_cooldown(self, ctx):
        await asyncio.sleep(self.cooldown)
        self.cooldown_tries = 0
        self.cooldown_lock = False
        putlog.info(f'Cooldown removed. Cooldown tries is set to {self.cooldown_tries}. Cooldown lock removed.')
        await ctx.send('Cooldown removed! You can request song by link now.')
        return

    @commands.command(name='play', aliases=CMD_ALIASES['play'])
    @check_valid_channel
    async def play_command(self, ctx, *, query: t.Optional[str]):
        """
        A play command to search and give option for songs to play.
        :param ctx: context passed by DC
        :param query: The song name
        :return: None
        """
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)
        # ----------------------------------------------------------------------
        if query is None:  # Resume Track Checks
            putlog.debug('Resume player command given')
            if player.queue.is_empty:
                putlog.debug('Resume player command given but queue is empty. Raising Exception!')
                raise QueueIsEmpty
            if not player.is_paused:
                putlog.debug('Resume command given but player is already playing. Sending message to user.')
                await ctx.send('🔊  Player is already playing...')
            else:  # Resume Music
                putlog.debug('Resume command given and executing successfully.')
                await player.set_pause(False)
                await player.set_volume(self.current_volume)  # Gives fading audio effect
                await ctx.send('▶    Playback resumed')

        # ----------------------------------------------------------------------
        else:  # Query Search
            putlog.debug(f'Query is {query}')
            if self.check_query_or_jump(query):  # Jump tracks by number (index)
                putlog.debug('validating command if it is a song jump or another query.')
                if int(query) in range(1, player.queue.length + 1):
                    self.song_index = int(query)
                    await player.stop()  # Gives control to >> on_player_stop()
                    putlog.debug(f'Jump index set to {self.song_index},'
                                 f' Playback stopped and control passed to on_player_stop() method.')
                else:
                    await ctx.send('Index given is not in range of playlist! 🙄 🙁')
            else:
                putlog.debug('Query was not a song jump. now checking if query is a link')
                query = query.strip("<>")  # search by link

                await self.search_engine_manager(ctx, query, player)

    async def search_engine_manager(self, ctx, query, player):
        if not re.match(URL_REGEX, query):
            putlog.debug('Query is song name. NOT A LINK')
            songs = await self.wavelink.get_tracks(f"ytsearch:{query}")
            if songs:
                await player.add_tracks(ctx, songs, search_engine=Configs.YT)
            else:
                temp = await self.wavelink.get_tracks(f"scsearch:{query}")
                await player.add_tracks(ctx, temp, search_engine=Configs.SC)
            return

        await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

        # ----------------------------------------------------------------------

    @commands.command(name='pause', aliases=CMD_ALIASES['pause'])
    @check_valid_channel
    async def pause_command(self, ctx):
        """
        This function provides the functionality to pause the current song.
        :param ctx: Context
        :return: None
        """
        player = self.get_player(ctx)
        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_volume(0)
        await player.set_pause(True)
        await ctx.send('⏸    Playback Paused!')

    @commands.command(name='stop', aliases=CMD_ALIASES['stop'])
    @check_valid_channel
    async def stop_command(self, ctx):
        """
        This function stops the current music stream and clears the queue
        :param ctx: context
        :return: None
        """
        player = self.get_player(ctx)
        if player.is_playing:
            putlog.debug('Song stop requested. Stopping player and destroying playlist.')
            player.queue.empty()
            await player.set_volume(0)  # Gives fading audio effect
            await player.stop()
            await ctx.send('Playback Stopped')
            await player.delete_now_playing_embed()
            putlog.debug('Player stopped and playlist destroyed.')
        else:
            putlog.warning('Player is already stopped, still stop command is invoked!')
            await ctx.send('Do you hear anything? ... NO!. coz player is already stopped. 😋')

    @commands.command(name='next', aliases=CMD_ALIASES['next'])
    @check_valid_channel
    async def next_command(self, ctx):
        """
        This function provides the functionality to skip a song form the current playlist and play the next one.
        :param ctx: context
        :return: None | Raises NoMoreTracks if no next song found
        """
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.send(f'Playing next track   ⏭')

    @commands.command(name='previous', aliases=CMD_ALIASES['previous'])
    @check_valid_channel
    async def previous_command(self, ctx):
        """
        This function provides the functionality to play the previous song in the playlist.
        :param ctx: context
        :return: None
        """
        player = self.get_player(ctx)
        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        await ctx.send('Playing previous track in queue.  ⏮')

    @commands.command(name='remove', aliases=CMD_ALIASES['remove'])
    @check_valid_channel
    async def remove_command(self, ctx, ind: str):
        putlog.debug(f"Track remove request receive. Index specified : {ind}")
        try:
            ind = int(ind)
            player = self.get_player(ctx)
            track_to_remove = player.queue.get_track_by_index(ind)

            if ind == player.queue.position:
                putlog.debug("Remove index was equal to current playing song. Stopping the player, playing next"
                             " and removing song")
                await player.stop()
                await ctx.send(f"Track removed : {track_to_remove.title}")
                player.queue.remove_track_by_index(ind)
                return

            if player.queue.remove_track_by_index(ind):
                await ctx.send(f"Track removed : {track_to_remove.title}")
            else:
                await ctx.send('There was some problem removing this track.r')

        except ValueError:
            await ctx.send('Please specify the index of song you want to remove as integer number.')

    @commands.command(name='seek', aliases=CMD_ALIASES['seek'])
    @check_valid_channel
    async def seek_command(self, ctx, stride: t.Optional[int] = 1):
        player = self.get_player(ctx)
        ct = player.queue.current_track

        length = ct.duration
        seek_length = scale_to_10(int(length), int(stride))
        if seek_length is not False:
            await player.seek(seek_length)
            await ctx.send(
                f"Song is seeked by {seek_length // 1000} seconds, Current position is : "
                f"{show_track_duration(seek_length)}")
        else:
            await ctx.send('stride is wrong')

    @commands.command(name='repeat', aliases=CMD_ALIASES['repeat'])
    @check_valid_channel
    async def repeat_command(self, ctx, mode: str):
        mode = mode.lower()
        if mode not in ("none", '1', 'all', 'current'):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        putlog.debug(f'Repeat mode set to {mode}')

        if mode == 'none':
            response = f"Repeat Mode has been set to {mode.title()}. No song will be repeated."
        elif mode in ('1', 'current'):
            response = f'Repeat mode has been set to {mode}. Current song is on loop  🔂'
        elif mode == 'all':
            response = f'Repeat mode has been set to {mode}. ' \
                       f'Current playlist will be played over and over. Enjoy the party 🎉 🥳'
        else:
            response = f"Repeat Mode has been set to {mode}."

        await ctx.send(response)

    @commands.command(name="volume", aliases=CMD_ALIASES['volume'])
    @check_valid_channel
    async def set_player_volume(self, ctx, v: t.Optional[str]):
        try:
            if v:
                v = int(v)
                if v <= MAX_VOLUME:
                    player = self.get_player(ctx)
                    await player.set_volume(v)
                    if v > self.current_volume:
                        await ctx.send(f'Volume Raised by : {v - self.current_volume}  ⤴.  Player volume is : {v}.  ')
                    elif v < self.current_volume:
                        await ctx.send(
                            f'Volume Decreased by : {self.current_volume - v}  ⤵.  Player volume set to {v}.  ')
                    else:
                        await ctx.send(f'Player volume not changed. Current volume : {self.current_volume}.')
                    self.current_volume = v
                else:
                    await ctx.send(f'Set volume in range 0-100')
            else:
                await ctx.send(f'Current volume level is : {self.current_volume}.')
        except ValueError:
            await ctx.send(f"Volume must be Integer")

    @commands.command(name='player_mute', aliases=CMD_ALIASES['player_mute'])
    @check_valid_channel
    async def mute_command(self, ctx):
        player = self.get_player(ctx)
        await player.set_volume(0)
        await ctx.send('Player is muted!  🔇')

    @commands.command(name='player_unmute', aliases=CMD_ALIASES['player_unmute'])
    @check_valid_channel
    async def unmute_command(self, ctx):
        player = self.get_player(ctx)
        await player.set_volume(self.current_volume)
        await ctx.send('Player mute removed!  🔊')

    @commands.command(name='shuffle', aliases=CMD_ALIASES['shuffle'])
    @check_valid_channel
    async def shuffle_command(self, ctx):
        """
        Shuffles the playlist.
        :param ctx: context
        :return: None
        """
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.send('Queue shuffled')

    @commands.command(name='playlist', aliases=CMD_ALIASES['playlist'])
    @check_valid_channel
    async def queue_command(self, ctx, page_stride: t.Optional[int] = 1):
        player = self.get_player(ctx)
        all_songs = list(paginate(player.queue.all_tracks, PAGINATION_LIMIT))

        if player.queue.is_empty:
            raise QueueIsEmpty
        if page_stride > len(all_songs):
            await ctx.send('That Page is not available...')
            return
        currently_playing = player.queue.current_track
        upcoming_song = player.queue.upcoming
        total_duration = player.queue.total_duration

        def _check(r, u):
            return (
                r.emoji == '🗑' and u == ctx.author and r.message.id == plst.id
            )

        # Show Playlist
        plst = await ctx.send(
            embed=music_embeds.show_playlist(
                all_songs,
                currently_playing,
                upcoming_song,
                requester=ctx.author.display_name,
                requester_icon=ctx.author.avatar_url,
                color=ctx.author.color,
                total_duration=total_duration,
                page_stride=page_stride,
                full_playlist=player.queue.all_tracks,
                playlist_length=player.queue.length
            )  # Accepts kwargs
        )
        await plst.add_reaction('🗑')
        reaction, _ = await self.bot.wait_for('reaction_add', check=_check)
        if reaction:
            await plst.delete()

    @commands.command(name='information', aliases=CMD_ALIASES['information'])
    @check_valid_channel
    async def information_command(self, ctx):
        player = self.get_player(ctx)
        current_pos = player.queue.position
        current_track = player.queue.current_track.title
        current_track_index = player.queue.track_index(player.queue.current_track)
        requester = player.song_and_requester.get(current_track.title, '')
        repeat_mode = player.queue.repeat_mode
        current_vol = self.current_volume
        max_vol = MAX_VOLUME
        songs = player.queue.all_tracks[:10]

        await ctx.send(
            embed=music_embeds.show_player_info(
                current_pos, current_track, current_track_index,
                requester, repeat_mode, current_vol, max_vol,
                songs
            )
        )

    @commands.command(name='reset_playlist', aliases=CMD_ALIASES['reset_playlist'])
    @check_valid_channel
    async def reset_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        self.song_index = 0
        self.current_volume = DEFAULT_VOLUME
        await player.stop()
        await ctx.send('Player reset complete!')

    @commands.command(name='rejoin')
    @check_valid_channel
    async def rejoin_command(self, ctx):
        await ctx.send('Rejoining the channel. brb ✌')
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await player.teardown()
        await asyncio.sleep(2)
        await player.connect(ctx)
        await ctx.send('Rejoined guild!, lets play now.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        """
        Local exception handling for Music cog.

        :param ctx: Passed by discord.
        :param exc: Exception
        :return: None / handles exception
        """

        if isinstance(exc, RestrictedCommandToMusicChannel):
            await ctx.send(f'This command is made for {self.music_channel.mention}')
        elif isinstance(exc, InvalidRemoveIndex):
            await ctx.send(f'The playlist is not that big 🙄, Invalid Index!')
        elif isinstance(exc, QueueIsEmpty):
            await ctx.send(f'Queue is empty')

    # Exception handling for Play command =============================================================================
    # Exception handling for next_command =============================================================================
    # Exception handling for previous_command =========================================================================
    # Exception handling for pause_command ============================================================================
    # Exception handling for shuffle_command ==========================================================================

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        """
        :param ctx: context passed by DC command
        :param exc: Exception raised (in this case custom exception is raised) in Player class's connect method
        :return: None
        """
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send('Already connected to a voice channel')
        elif isinstance(exc, NotVoiceChannel):
            await ctx.send('No suitable voice channel provided')

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("No songs to play as the queue is empty.")
        elif isinstance(exc, NotVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("There are no previous tracks in the queue.")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send('⏸   Player is already paused!')

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more tracks in the queue.")

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue could not be shuffled as it is currently empty.")

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty. Add some songs by ```.p <song name>``` ✌ 🥳")


def setup(bot):
    bot.add_cog(Music(bot))


