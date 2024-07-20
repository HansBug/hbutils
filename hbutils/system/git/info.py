import os.path
import re
import shutil
import subprocess
import warnings
from functools import lru_cache
from typing import Optional

__all__ = [
    'git_info',
]


@lru_cache()
def _raw_check_git(git_path: str):
    """
    Check Git installation and version information.

    This function checks if Git is installed at the given path, retrieves its version information,
    and also checks for Git LFS installation and version.

    :param git_path: Path to the Git executable.
    :type git_path: str

    :return: A dictionary containing information about Git and Git LFS installations.
    :rtype: dict

    """
    git_info = {}
    if git_path and os.path.exists(git_path):
        git_info['exec'] = git_path
        git_info['installed'] = True
        try:
            git_version = subprocess.check_output([git_path, "--version"], universal_newlines=True).strip()
            git_info['version_info'] = git_version
            matching = re.fullmatch(r'^git\s*version\s*(?P<version>[\s\S]+?)\s*$', git_version)
            if matching:
                git_info['version'] = matching.group('version')
            else:
                warnings.warn(f'Git installed but unrecognizable git version info: {git_version!r}')
                git_info['version'] = None
        except subprocess.CalledProcessError as err:
            warnings.warn(f'Git found but unable to check git version, exitcode {err.returncode}.')
            git_info["version"] = None
    else:
        git_info['installed'] = False
        git_info['exec'] = None

    if git_info["installed"]:
        git_lfs_info = {}
        git_info['lfs'] = git_lfs_info
        try:
            lfs_version = subprocess.check_output([git_path, "lfs", "version"], universal_newlines=True).strip()
            git_lfs_info["installed"] = True
            git_lfs_info['version_info'] = lfs_version
            matching = re.fullmatch(r'^git-lfs/(?P<version>[\s\S]+?)\s+[\s\S]+$', lfs_version)
            if matching:
                git_lfs_info["version"] = matching.group('version')
            else:
                warnings.warn(f'Git lfs installed but unrecognizable git lfs version info: {lfs_version!r}')
                git_lfs_info['version'] = None
        except subprocess.CalledProcessError:
            git_lfs_info['installed'] = False

    return git_info


def git_info(git_path: Optional[str] = None):
    """
    Get information about Git and Git LFS installations.

    This function attempts to locate the Git executable and retrieve information about
    the Git and Git LFS installations. It first tries to use the provided git_path,
    then checks the system PATH, and finally falls back to None if Git is not found.

    :param git_path: Optional path to the Git executable. If not provided, the function
                     will attempt to find Git in the system PATH.
    :type git_path: Optional[str]

    :return: A dictionary containing information about Git and Git LFS installations.
    :rtype: dict

    :raises subprocess.CalledProcessError: If there's an error running Git commands.
    :warns UserWarning: If Git version information cannot be parsed or if Git LFS version unrecognizable.

    :usage:
        >>> info = git_info()
        >>> print(info['installed'])  # Check if Git is installed
        >>> print(info['version'])    # Get Git version
        >>> print(info['lfs']['installed'])  # Check if Git LFS is installed

    The returned dictionary has the following structure:

    .. code-block:: python
        :linenos:

        {
            'exec': str,          # Path to Git executable
            'installed': bool,    # Whether Git is installed
            'version_info': str,  # Full version string from 'git --version'
            'version': str,       # Parsed Git version
            'lfs': {              # Information about Git LFS
                'installed': bool,    # Whether Git LFS is installed
                'version_info': str,  # Full version string from 'git lfs version'
                'version': str        # Parsed Git LFS version
            }
        }

    """
    git_path = git_path or shutil.which('git') or None
    if git_path:
        git_path = os.path.normcase(os.path.normpath(git_path))
    return _raw_check_git(git_path)
