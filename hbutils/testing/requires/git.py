"""
Git availability and version query utilities for testing environments.

This module provides lightweight helpers built on top of
:func:`hbutils.system.git.info.git_info` to query Git and Git LFS installation
status as well as retrieve their versions. The functions are intentionally
minimal and designed for use in test requirements checks where a concise
boolean or version object is more convenient than the full metadata dictionary.

The module contains the following main components:

* :func:`is_git_installed` - Determine whether Git is available
* :func:`git_version` - Retrieve the Git version as a :class:`VersionInfo`
* :func:`is_git_lfs_installed` - Determine whether Git LFS is available
* :func:`git_lfs_version` - Retrieve the Git LFS version as a :class:`VersionInfo`

.. note::
   These helpers depend on :func:`hbutils.system.git.info.git_info` and therefore
   inherit its path resolution and caching behavior.

Example::

    >>> from hbutils.testing.requires.git import is_git_installed, git_version
    >>> if is_git_installed():
    ...     print(git_version())
    2.34.1

"""

from typing import Optional

from .version import VersionInfo
from ...system.git.info import git_info

__all__ = [
    'is_git_installed',
    'git_version',
    'is_git_lfs_installed',
    'git_lfs_version',
]


def is_git_installed(git_path: Optional[str] = None) -> bool:
    """
    Check if Git is installed.

    The function delegates to :func:`hbutils.system.git.info.git_info` and
    reports whether Git is available. When ``git_path`` is provided, it is used
    as the candidate Git executable path; otherwise, the system ``PATH`` is
    searched.

    :param git_path: Optional path to the Git executable. If not provided, the
        function will attempt to find Git in the system ``PATH``.
    :type git_path: Optional[str]
    :return: ``True`` if Git is installed, ``False`` otherwise.
    :rtype: bool

    Example::

        >>> is_git_installed()
        True
        >>> is_git_installed('/custom/path/to/git')
        True
    """
    return git_info(git_path=git_path)['installed']


def git_version(git_path: Optional[str] = None) -> Optional[VersionInfo]:
    """
    Get the Git version.

    This function returns a :class:`VersionInfo` instance for the parsed Git
    version when Git is installed and its version information can be parsed.
    If Git is not installed or the version string cannot be recognized, it
    returns ``None``.

    :param git_path: Optional path to the Git executable. If not provided, the
        function will attempt to find Git in the system ``PATH``.
    :type git_path: Optional[str]
    :return: Git version wrapped as :class:`VersionInfo`, or ``None`` if Git is
        not installed or the version cannot be determined.
    :rtype: Optional[VersionInfo]

    .. note::
        This function may return ``None`` even if Git is installed, in cases
        where the ``git --version`` output is unrecognizable.

    Example::

        >>> version = git_version()
        >>> if version:
        ...     print(f"Git version: {version}")
        ... else:
        ...     print("Git version could not be determined")
        Git version: 2.34.1
    """
    info = git_info(git_path=git_path)
    if info['installed'] and info['version']:
        return VersionInfo(info['version'])
    else:
        return None


def is_git_lfs_installed(git_path: Optional[str] = None) -> bool:
    """
    Check if Git LFS is installed.

    The function reports ``True`` only when both Git and Git LFS are installed.
    It uses :func:`hbutils.system.git.info.git_info` to obtain this information.

    :param git_path: Optional path to the Git executable. If not provided, the
        function will attempt to find Git in the system ``PATH``.
    :type git_path: Optional[str]
    :return: ``True`` if Git and Git LFS are installed, ``False`` otherwise.
    :rtype: bool

    Example::

        >>> is_git_lfs_installed()
        True
        >>> is_git_lfs_installed('/custom/path/to/git')
        False
    """
    info = git_info(git_path=git_path)
    return bool(info['installed'] and info['lfs']['installed'])


def git_lfs_version(git_path: Optional[str] = None) -> Optional[VersionInfo]:
    """
    Get the Git LFS version.

    This function returns a :class:`VersionInfo` instance for the parsed Git LFS
    version when Git LFS is installed and its version information can be parsed.
    If Git LFS is not installed or the version string cannot be recognized, it
    returns ``None``.

    :param git_path: Optional path to the Git executable. If not provided, the
        function will attempt to find Git in the system ``PATH``.
    :type git_path: Optional[str]
    :return: Git LFS version wrapped as :class:`VersionInfo`, or ``None`` if Git
        LFS is not installed or the version cannot be determined.
    :rtype: Optional[VersionInfo]

    .. note::
        This function may return ``None`` even if Git LFS is installed, in cases
        where the ``git lfs version`` output is unrecognizable.

    Example::

        >>> version = git_lfs_version()
        >>> if version:
        ...     print(f"Git LFS version: {version}")
        ... else:
        ...     print("Git LFS version could not be determined")
        Git LFS version: 3.2.0
    """
    info = git_info(git_path=git_path)
    if info['installed'] and info['lfs']['installed'] and info['lfs']['version']:
        return VersionInfo(info['lfs']['version'])
    else:
        return None
