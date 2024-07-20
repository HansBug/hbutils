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
    return git_info(git_path=git_path)['installed']


def git_version(git_path: Optional[str] = None) -> Optional[VersionInfo]:
    # note that return value of this function is not guaranteed to be non-None when git is installed
    # when git --version output unrecognizable value, this func can also return None
    info = git_info(git_path=git_path)
    if info['installed'] and info['version']:
        return VersionInfo(info['version'])
    else:
        return None


def is_git_lfs_installed(git_path: Optional[str] = None) -> bool:
    info = git_info(git_path=git_path)
    return bool(info['installed'] and info['lfs']['installed'])


def git_lfs_version(git_path: Optional[str] = None) -> Optional[VersionInfo]:
    # note that return value of this function is not guaranteed to be non-None when git lfs is installed
    # when git lfs version output unrecognizable value, this func can also return None
    info = git_info(git_path=git_path)
    if info['installed'] and info['lfs']['installed'] and info['lfs']['version']:
        return VersionInfo(info['lfs']['version'])
    else:
        return None
