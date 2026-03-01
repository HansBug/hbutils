"""
Utilities for converting and formatting memory size values.

This module provides helpers to normalize size representations into integer
byte counts and to format sizes into human-readable strings using binary
(NIST) or decimal (SI) prefixes. It builds on :mod:`bitmath` to parse and
format values while ensuring integer byte counts, issuing warnings when
floating-point rounding is required.

The module contains the following public components:

* :func:`size_to_bytes` - Convert size representations to integer bytes
* :func:`size_to_bytes_str` - Format sizes into a readable string
* :class:`SizeSystem` - Enumerated size systems for formatting

.. note::
   Floating-point byte values are rounded to the nearest integer with a
   warning when the rounding is non-negligible.

Example::

    >>> from hbutils.scale.size import size_to_bytes, size_to_bytes_str, SizeSystem
    >>> size_to_bytes('3.54 GB')
    3540000000
    >>> size_to_bytes_str('3.54 GB')
    '3.296881914138794 GiB'
    >>> size_to_bytes_str('3.54 GB', system='si')
    '3.54 GB'
    >>> SizeSystem.loads('nist')  # Enum lookup for formatting system
    <SizeSystem.NIST: 2>

"""
import warnings
from enum import IntEnum, unique
from typing import Union, Optional

from bitmath import Byte, NIST, SI
from bitmath import parse_string_unsafe as parse_bytes

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from ..model import int_enum_loads

__all__ = [
    'size_to_bytes', 'size_to_bytes_str'
]

_EPS = 1e-10


def _is_int(value: Union[int, float], stacklevel: int = 4) -> int:
    """
    Convert a value to an integer, with a warning if rounding occurs.

    :param value: The value to convert to an integer.
    :type value: Union[int, float]
    :param stacklevel: The stack level for the warning, defaults to ``4``.
    :type stacklevel: int
    :return: The integer representation of the value.
    :rtype: int
    :raises AssertionError: If the input is neither ``float`` nor ``int``.

    This function is used internally to ensure that byte values are always
    integers. If a float is provided, it is rounded to the nearest integer,
    and a warning is issued if the rounding causes a significant change in
    the value.
    """
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


def _base_size_to_bytes(size: Union[int, float, str, Byte], stacklevel: int = 4) -> int:
    """
    Convert various size representations to bytes.

    :param size: The size to convert, can be ``int``, ``float``, ``str``,
        or a :class:`bitmath.Byte` object.
    :type size: Union[int, float, str, Byte]
    :param stacklevel: The stack level for warnings, defaults to ``4``.
    :type stacklevel: int
    :return: The size in bytes as an integer.
    :rtype: int
    :raises TypeError: If the input type is not supported.
    :raises ValueError: If a string cannot be parsed by :func:`bitmath.parse_string_unsafe`.

    This function is used internally to handle different input types and
    convert them to bytes.
    """
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
    Convert any type of memory size representation to an integer value in bytes.

    :param size: Any type of size information.
    :type size: Union[int, float, str, Byte]
    :return: Size in bytes as an integer.
    :rtype: int
    :raises TypeError: If ``size`` is not an ``int``, ``float``, ``str``, or
        :class:`bitmath.Byte`.
    :raises ValueError: If a string cannot be parsed by :func:`bitmath.parse_string_unsafe`.

    This function can handle various input types:

    * Integers and floats are treated as byte values.
    * Strings are parsed as size representations (e.g., ``"23356 KB"``).
    * :class:`bitmath.Byte` objects are converted to their byte value.

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
    """
    Enumeration of size systems used for formatting.

    The enumeration is enhanced by :func:`hbutils.model.int_enum_loads`,
    providing a :meth:`loads` class method for convenient lookup by name or
    value.

    :cvar NIST: Uses binary prefixes (KiB, MiB, GiB, etc.).
    :cvar SI: Uses decimal prefixes (KB, MB, GB, etc.).

    Example::

        >>> SizeSystem.loads('nist') is SizeSystem.NIST
        True
        >>> SizeSystem.loads('si') is SizeSystem.SI
        True
        >>> SizeSystem.loads(2) is SizeSystem.NIST
        True
    """
    NIST = NIST
    SI = SI


def size_to_bytes_str(size: _SIZE_TYPING, precision: Optional[int] = None,
                      sigfigs: Optional[int] = None,
                      system: Literal['nist', 'si'] = 'nist') -> str:
    """
    Convert any type of memory size to a string value in the most appropriate unit.

    :param size: Any type of size information.
    :type size: Union[int, float, str, Byte]
    :param precision: Precision for float values. When ``None``, the
        default string representation from :mod:`bitmath` is used.
    :type precision: Optional[int]
    :param sigfigs: Number of significant figures to use. If specified,
        this overrides ``precision``.
    :type sigfigs: Optional[int]
    :param system: The unit system to use, either ``'nist'`` (binary) or
        ``'si'`` (decimal). Default is ``'nist'``.
    :type system: Literal['nist', 'si']
    :return: String formatted size value in the best unit.
    :rtype: str
    :raises ValueError: If an invalid system type is provided.
    :raises TypeError: If ``size`` is not an ``int``, ``float``, ``str``, or
        :class:`bitmath.Byte`.
    :raises ValueError: If a string cannot be parsed by :func:`bitmath.parse_string_unsafe`.

    This function provides a human-readable representation of size values.
    It automatically chooses the most appropriate unit (B, KB/KiB, MB/MiB,
    etc.) based on the size.

    The ``system`` parameter allows choosing between NIST (binary, e.g.,
    KiB) and SI (decimal, e.g., KB) units.

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
    try:
        system = SizeSystem.loads(system)
    except KeyError:
        raise ValueError(f'Invalid System Type - {system!r}.')
    if sigfigs is not None:
        format_str = f"{{value:.{sigfigs}g}} {{unit}}"
    elif precision is not None:
        format_str = f"{{value:.{precision}f}} {{unit}}"
    else:
        format_str = "{value} {unit}"
    return Byte(_base_size_to_bytes(size)).best_prefix(system.value).format(format_str)
