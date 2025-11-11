"""
This module provides utility functions for checking Git and Git LFS installations and versions.

It includes functions to:
1. Check if Git is installed.
2. Get the Git version.
3. Check if Git LFS is installed.
4. Get the Git LFS version.

These functions utilize the git_info function from the system.git.info module and provide
a more convenient interface for common Git-related queries.
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

    :param git_path: Optional path to the Git executable. If not provided, the function
                     will attempt to find Git in the system PATH.
    :type git_path: Optional[str]

    :return: True if Git is installed, False otherwise.
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

    :param git_path: Optional path to the Git executable. If not provided, the function
                     will attempt to find Git in the system PATH.
    :type git_path: Optional[str]

    :return: A VersionInfo object representing the Git version, or None if Git is not installed
             or the version cannot be determined.
    :rtype: Optional[VersionInfo]

    .. note::
        This function may return None even if Git is installed, in cases where the
        'git --version' output is unrecognizable.

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

    :param git_path: Optional path to the Git executable. If not provided, the function
                     will attempt to find Git in the system PATH.
    :type git_path: Optional[str]

    :return: True if both Git and Git LFS are installed, False otherwise.
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

    :param git_path: Optional path to the Git executable. If not provided, the function
                     will attempt to find Git in the system PATH.
    :type git_path: Optional[str]

    :return: A VersionInfo object representing the Git LFS version, or None if Git LFS is not installed
             or the version cannot be determined.
    :rtype: Optional[VersionInfo]

    .. note::
        This function may return None even if Git LFS is installed, in cases where the
        'git lfs version' output is unrecognizable.

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
