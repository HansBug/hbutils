"""
Operating system detection utilities.

This module provides a small set of cross-platform helpers for detecting the
current operating system using :mod:`platform`. The detection is cached to
avoid repeated system calls, and the API exposes simple boolean functions for
common OS checks.

The module contains the following public functions:

* :func:`is_linux` - Check if the current OS is Linux
* :func:`is_windows` - Check if the current OS is Windows
* :func:`is_darwin` - Check if the current OS is Darwin/macOS
* :data:`is_macos` - Alias of :func:`is_darwin`

.. note::
   The module internally uses an :class:`enum.IntEnum` for OS identification,
   but only the helper functions are considered public API.

Example::

    >>> from hbutils.system.os.type import is_linux, is_windows, is_macos
    >>> is_linux()
    True
    >>> is_windows()
    False
    >>> is_macos()
    False
"""

import platform
from enum import IntEnum, unique
from functools import lru_cache
from typing import Callable

from ...model import int_enum_loads

__all__ = [
    'is_linux', 'is_windows', 'is_macos', 'is_darwin'
]


@int_enum_loads(name_preprocess=str.upper)
@unique
class OSType(IntEnum):
    """
    Enumeration of supported operating system types.

    This enum defines integer constants for different operating systems
    that can be detected by the :mod:`platform` module. The enum is decorated
    with :func:`hbutils.model.enum.int_enum_loads` to support loading from
    string names via the :meth:`loads` class method.

    :cvar LINUX: Linux operating system identifier.
    :cvar WINDOWS: Windows operating system identifier.
    :cvar DARWIN: Darwin/macOS operating system identifier.
    :cvar JAVA: Java platform identifier.
    """
    LINUX = 1
    WINDOWS = 2
    DARWIN = 3
    JAVA = 4


@lru_cache()
def _get_os_type() -> OSType:
    """
    Get the current operating system type with caching.

    This function detects the current operating system using
    :func:`platform.system` and converts it to an :class:`OSType` enum value.
    The result is cached using :func:`functools.lru_cache` to avoid repeated
    system calls.

    :return: The detected operating system type.
    :rtype: OSType
    :raises KeyError: If :func:`platform.system` returns a name that cannot be
        mapped to :class:`OSType`.

    Example::
        >>> _get_os_type()  # On a Linux system
        <OSType.LINUX: 1>
    """
    return OSType.loads(platform.system())


def is_linux() -> bool:
    """
    Check if the current operating system is Linux.

    Return ``True`` if the current operating system is Linux, otherwise return
    ``False``.

    :return: Whether the current OS is Linux.
    :rtype: bool

    Example::
        >>> is_linux()  # On a Linux system
        True
        >>> is_linux()  # On a Windows system
        False
    """
    return _get_os_type() == OSType.LINUX


def is_windows() -> bool:
    """
    Check if the current operating system is Windows.

    Return ``True`` if the current operating system is Windows, otherwise return
    ``False``.

    :return: Whether the current OS is Windows.
    :rtype: bool

    Example::
        >>> is_windows()  # On a Windows system
        True
        >>> is_windows()  # On a Linux system
        False
    """
    return _get_os_type() == OSType.WINDOWS


def is_darwin() -> bool:
    """
    Check if the current operating system is Darwin (macOS).

    Return ``True`` if the current operating system is Darwin, otherwise return
    ``False``.

    :return: Whether the current OS is Darwin.
    :rtype: bool

    .. note::
        Darwin is macOS.

    Example::
        >>> is_darwin()  # On a macOS system
        True
        >>> is_darwin()  # On a Linux system
        False
    """
    return _get_os_type() == OSType.DARWIN


is_macos: Callable[[], bool] = is_darwin
"""
Alias of :func:`is_darwin`.

This is a convenience alias for checking if the current operating system
is macOS. It provides a more intuitive name while maintaining the same
functionality as :func:`is_darwin`.
"""
