from discord.ext import commands


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NotVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class PlayerIsAlreadyPlaying(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class NotInQueue(commands.CommandError):
    pass


class InvalidRemoveIndex(commands.CommandError):
    pass


class RestrictedCommandToMusicChannel(commands.CheckFailure):
    pass


class StrideOutOfRange(Exception):
    pass


__all__ = [
    "AlreadyConnectedToChannel",
    "NotVoiceChannel",
    "QueueIsEmpty",
    "NoTracksFound",
    "PlayerIsAlreadyPlaying",
    "PlayerIsAlreadyPaused",
    "NoMoreTracks",
    "NoPreviousTracks",
    "InvalidRepeatMode",
    "NotInQueue",
    "InvalidRemoveIndex",
    "RestrictedCommandToMusicChannel",
    "StrideOutOfRange"
]
