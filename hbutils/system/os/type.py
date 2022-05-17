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
    return _get_os_type() == OSType.LINUX


def is_windows() -> bool:
    return _get_os_type() == OSType.WINDOWS


def is_darwin() -> bool:
    return _get_os_type() == OSType.DARWIN


is_macos = is_darwin
