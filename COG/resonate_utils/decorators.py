import sys
from .custom_exceptions import *
import functools
from discord.ext import commands
from .resonate_settings import Configs
import asyncio

RESTRICTION = Configs.RESTRICT_CMDS_TO_MUSIC_CHANNEL


def export(fn):
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        name = fn.__name__
        all_ = mod.__all__
        if name not in all_:
            all_.append(name)
    else:
        mod.__all__ = [fn.__name__]
    return fn


def check_empty_queue(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self, *_ = args
        if self._Queue__queue:
            return func(*args, **kwargs)
        raise QueueIsEmpty

    return wrapper


def check_connected_to_channel(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self, *_ = args
        if not self.is_connected:
            return func(*args, **kwargs)
        raise AlreadyConnectedToChannel

    return wrapper


async def predicate(ctx):
    if RESTRICTION:
        if Configs.MUSIC_CMD_CHANNEL:
            if not ctx.channel.id == Configs.MUSIC_CMD_CHANNEL:
                raise RestrictedCommandToMusicChannel
            return True
        else:
            raise Exception('Commands restricted to music channel but music channel not specified.')
    return True


# A decorator to check Music commands are being called in music channel only.
check_valid_channel = commands.check(predicate)


def show_typing(interval=Configs.TYPING_INTERVAL):
    assert any([isinstance(interval, int), isinstance(interval, float)])

    def top_wrapper(fun):
        @functools.wraps(fun)
        async def wrapper(*args, **kwargs):
            if Configs.SHOW_TYPING:
                for ctx in args:
                    if isinstance(ctx, commands.context.Context):
                        async with ctx.typing():
                            await asyncio.sleep(interval)
            return await fun(*args, **kwargs)

        return wrapper

    return top_wrapper


__all__ = [
    "check_valid_channel",
    "check_empty_queue",
    "show_typing",
    "export"
]
