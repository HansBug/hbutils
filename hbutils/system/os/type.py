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
    LINUX = 1
    WINDOWS = 2
    DARWIN = 3
    JAVA = 4


@lru_cache()
def _get_os_type() -> OSType:
    return OSType.loads(platform.system())


def is_linux() -> bool:
    """
    Overview:
        Return ``True`` if current operating system is linux, otherwise return ``False``.

    :return: This OS is linux or not.
    """
    return _get_os_type() == OSType.LINUX


def is_windows() -> bool:
    """
    Overview:
        Return ``True`` if current operating system is windows, otherwise return ``False``.

    :return: This OS is windows or not.
    """
    return _get_os_type() == OSType.WINDOWS


def is_darwin() -> bool:
    """
    Overview:
        Return ``True`` if current operating system is darwin, otherwise return ``False``.

    :return: This OS is darwin or not.

    .. note::
        Darwin is macos.
    """
    return _get_os_type() == OSType.DARWIN


is_macos = is_darwin
"""
Alias of :func:`is_darwin`.
"""
