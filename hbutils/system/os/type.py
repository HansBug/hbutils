"""
Operating System Detection Utilities Module.

This module provides utilities for detecting the current operating system type.
It defines an enumeration of supported OS types and functions to check if the
current system matches specific operating systems (Linux, Windows, macOS/Darwin).

The module uses caching to optimize repeated OS type checks and provides a
consistent interface for OS detection across the application.
"""

import platform
from enum import IntEnum, unique
from functools import lru_cache

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
    that can be detected by the platform module. The enum is decorated
    with int_enum_loads to support loading from string names.
    
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
    
    This function detects the current operating system using platform.system()
    and converts it to an OSType enum value. The result is cached using lru_cache
    to avoid repeated system calls.
    
    :return: The detected operating system type.
    :rtype: OSType
    
    Example::
        >>> _get_os_type()  # On a Linux system
        <OSType.LINUX: 1>
    """
    return OSType.loads(platform.system())


def is_linux() -> bool:
    """
    Check if the current operating system is Linux.
    
    Return ``True`` if current operating system is linux, otherwise return ``False``.

    :return: This OS is linux or not.
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
    
    Return ``True`` if current operating system is windows, otherwise return ``False``.

    :return: This OS is windows or not.
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
    
    Return ``True`` if current operating system is darwin, otherwise return ``False``.

    :return: This OS is darwin or not.
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


is_macos = is_darwin
"""
Alias of :func:`is_darwin`.

This is a convenience alias for checking if the current operating system
is macOS. It provides a more intuitive name while maintaining the same
functionality as is_darwin().
"""
