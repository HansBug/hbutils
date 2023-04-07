"""
Overview:
    Useful utilities for time units, such as h/m/s.
"""
import datetime
from typing import Union

from pytimeparse import parse as parse_duration

__all__ = ['time_to_duration', 'time_to_delta_str']

_TIME_TYPING = Union[float, int, str]


def time_to_duration(time_: _TIME_TYPING) -> Union[float, int]:
    """
    Overview:
        Turn any types of time duration in time value in seconds.

    Arguments:
        - time\\_ (:obj:`Union[int, float, str]`): Any types of time duration.

    Returns:
        - bytes (:obj:`int`): Time duration value in seconds.

    Examples::
        >>> from hbutils.scale import time_to_duration
        >>> time_to_duration(23344)
        23344
        >>> time_to_duration(233.54)
        233.54
        >>> time_to_duration('1h343m67.4s')
        24247.4
        >>> time_to_duration('0:03:53.540000')
        233.54
    """
    if isinstance(time_, (float, int)):
        return time_
    elif isinstance(time_, str):
        return parse_duration(time_)
    else:
        raise TypeError('{float}, {int} or {str} expected but {actual} found.'.format(
            float=float.__name__,
            int=int.__name__,
            str=str.__name__,
            actual=type(time_).__name__,
        ))


def time_to_delta_str(time_: _TIME_TYPING) -> str:
    """
    Overview:
        Turn any types of time duration in time value in formatted string.

    Arguments:
        - time\\_ (:obj:`Union[int, float, str]`): Any types of time duration.

    Returns:
        - bytes (:obj:`int`): Time duration value in formatted string.

    Examples::
        >>> from hbutils.scale import time_to_delta_str
        >>> time_to_delta_str(23344)
        '6:29:04'
        >>> time_to_delta_str(233.54)
        '0:03:53.540000'
        >>> time_to_delta_str('1h343m67.4s')
        '6:44:07.400000'
    """
    return str(datetime.timedelta(seconds=time_to_duration(time_)))
