"""
This module provides utilities for retrieving system-related information, particularly Python version details.

The module uses the `platform` module to obtain Python version information and returns it in a structured
format using the `packaging.version.Version` class for easy version comparison and manipulation.
"""

import platform

from packaging.version import Version

__all__ = [
    'python_version',
]


def python_version() -> Version:
    """
    Get version of python.

    This function retrieves the current Python interpreter version and returns it as a
    `Version` object from the `packaging` library, which allows for easy version comparison
    and manipulation.

    :return: Version of python.
    :rtype: Version

    Examples::
        >>> from hbutils.system import python_version
        >>>
        >>> python_version()
        Version('3.8.1')  # for example
    """
    return Version(platform.python_version())
