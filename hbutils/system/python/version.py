import platform

from packaging.version import Version
from pkg_resources import parse_version

__all__ = [
    'python_version',
]


def python_version() -> Version:
    return parse_version(platform.python_version())
