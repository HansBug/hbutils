import platform

from packaging.version import Version

__all__ = [
    'python_version',
]


def python_version() -> Version:
    """
    Overview:
        Get version of python.

    :return: Version of python.

    Examples::
        >>> from hbutils.system import python_version
        >>>
        >>> python_version()
        Version('3.8.1')  # for example
    """
    return Version(platform.python_version())
