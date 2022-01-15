import datetime
from typing import Union

from pytimeparse import parse as parse_duration


def time_to_duration(time_) -> Union[float, int]:
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


def time_to_delta_str(time_) -> str:
    return str(datetime.timedelta(seconds=time_to_duration(time_)))
