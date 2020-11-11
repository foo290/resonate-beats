from .decorators import export


class StrideOutOfRange(Exception):
    pass


def validate_strides(stride, total_len):
    run = int(total_len / 10)
    jump_to = run * stride
    return jump_to


@export
def scale_to_10(length, stride):
    """
    This function scales track of any length from 0-9 scale for seek
    :param length: total length in milliseconds.
    :param stride: no. of stride we want to seek, For ex : stride = 1 means seek 45 seconds from current position.
    :return: milliseconds to seek for player (because seek function of player supports seek in ms.)
    """
    try:
        stride = int(stride)
        if stride in range(10):
            length = int(length)
            total_seconds = length
            res = validate_strides(stride, total_seconds)
            return int(res)
        else:
            return False, 404,  # out of range
    except ValueError:
        return False, 500,  # Not integer


@export
def true_duration_in_mins(length_in_ms):
    return length_in_ms // 60000


@export
def show_track_duration(duration_in_ms):
    formatted = f"{str(duration_in_ms // 60000).zfill(2)}:{str(duration_in_ms % 60).zfill(2)}"
    return formatted
