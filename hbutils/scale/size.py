"""
Overview:
    Useful utilities for memory size units, such as MB/KB/B.
"""
import warnings
from enum import IntEnum, unique
from typing import Union, Optional

from bitmath import Byte, NIST, SI
from bitmath import parse_string_unsafe as parse_bytes

from ..model import int_enum_loads

__all__ = [
    'size_to_bytes', 'size_to_bytes_str'
]

_EPS = 1e-10


def _is_int(value: Union[int, float], stacklevel: int = 4) -> int:
    if isinstance(value, float):
        _actual = int(round(value))
        _delta = abs(value - _actual)
        if _delta >= _EPS:
            warnings.warn(UserWarning(f'Float detected in variable in bytes ({repr(value)}), '
                                      f'rounded integer value ({repr(_actual)}) is used.'), stacklevel=stacklevel)
        return _actual
    elif isinstance(value, int):
        return value
    else:
        assert False, f"Should not reach here, {repr(type(value))} detected, " \
                      f"something may be wrong with {__name__}._is_int function."  # pragma: no cover


def _base_size_to_bytes(size, stacklevel: int = 4) -> int:
    if isinstance(size, (float, int)):
        return _is_int(size, stacklevel)
    elif isinstance(size, str):
        return _is_int(parse_bytes(size).bytes, stacklevel)
    elif isinstance(size, Byte):
        return _is_int(size.bytes, stacklevel)
    else:
        raise TypeError('{int}, {str} or {byte} expected but {actual} found.'.format(
            int=int.__name__,
            str=str.__name__,
            byte=Byte.__name__,
            actual=type(size).__name__,
        ))


_SIZE_TYPING = Union[int, float, str, Byte]


def size_to_bytes(size: _SIZE_TYPING) -> int:
    """
    Overview:
        Turn any types of memory size to integer value in bytes.

    Arguments:
        - size (:obj:`Union[int, float, str, Byte]`): Any types of size information.

    Returns:
        - bytes (:obj:`int`): Int formatted size in bytes.

    Examples::
        >>> from hbutils.scale import size_to_bytes
        >>> size_to_bytes(23344)
        23344
        >>> size_to_bytes('23356 KB')
        23356000
        >>> size_to_bytes('3.54 GB')
        3540000000
        >>> size_to_bytes('3.54 GiB')
        __main__:1: UserWarning: Float detected in variable in bytes (3801046056.96), rounded integer value (3801046057) is used.
        3801046057
    """
    return _base_size_to_bytes(size)


@int_enum_loads(name_preprocess=str.upper)
@unique
class SizeSystem(IntEnum):
    NIST = NIST
    SI = SI


def size_to_bytes_str(size: _SIZE_TYPING, precision: Optional[int] = None, system='nist') -> str:
    """
    Overview:
        Turn any types of memory size to string value in the best unit.

    :param size: Any types of size information.
    :param precision: Precsion for float values. Default is ``None`` which means just show the original float number.

    Returns:
        - bytes (:obj:`int`): String formatted size value in the best unit.

    Examples::
        >>> from hbutils.scale import size_to_bytes_str
        >>> size_to_bytes_str(23344)
        '22.796875 KiB'
        >>> size_to_bytes_str('23356 KB')
        '22.274017333984375 MiB'
        >>> size_to_bytes_str('3.54 GB')
        '3.296881914138794 GiB'
        >>> size_to_bytes_str('3.54 GiB')
        __main__:1: UserWarning: Float detected in variable in bytes (3801046056.96), rounded integer value (3801046057) is used.
        '3.540000000037253 GiB'
        >>> size_to_bytes_str('3.54 GB', precision=0)  # use precision
        '3 GiB'
        >>> size_to_bytes_str('3.54 GB', precision=3)
        '3.297 GiB'
        >>> size_to_bytes_str('3.54 GB', system='si')  # use GB/MB/KB instead of GiB/MiB/KiB
        '3.54 GB'
        >>> size_to_bytes_str('3.54 GB', precision=3, system='si')
        '3.540 GB'
    """
    system = SizeSystem.loads(system)
    if precision is None:
        format_str = "{value} {unit}"
    else:
        format_str = f"{{value:.{precision}f}} {{unit}}"
    return Byte(_base_size_to_bytes(size)).best_prefix(system.value).format(format_str)
