"""
Overview:
    Useful utilities for time units, such as h/m/s.
    
    This module provides functions to convert various time duration formats into
    standardized representations. It supports numeric values (int, float) and
    string formats (e.g., '1h30m', '0:03:53.540000').
"""
import datetime
from typing import Union

from pytimeparse import parse as parse_duration

__all__ = ['time_to_duration', 'time_to_delta_str']

_TIME_TYPING = Union[float, int, str]


def time_to_duration(time_: _TIME_TYPING) -> Union[float, int]:
    """
    Turn any types of time duration into time value in seconds.

    :param time_: Any types of time duration, can be numeric (seconds) or string format.
    :type time_: Union[int, float, str]

    :return: Time duration value in seconds.
    :rtype: Union[float, int]
    
    :raises TypeError: If the input type is not int, float, or str.

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
    Turn any types of time duration into time value in formatted string.

    This function converts various time duration formats into a standardized
    string representation using the format 'H:MM:SS' or 'H:MM:SS.ffffff' for
    durations with fractional seconds.

    :param time_: Any types of time duration, can be numeric (seconds) or string format.
    :type time_: Union[int, float, str]

    :return: Time duration value in formatted string (e.g., '6:29:04' or '0:03:53.540000').
    :rtype: str
    
    :raises TypeError: If the input type is not int, float, or str (raised by time_to_duration).

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
