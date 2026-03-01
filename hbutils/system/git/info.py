"""
Git installation discovery and version inspection utilities.

This module provides public helpers to discover the Git executable and gather
version information for both Git and Git LFS. It normalizes the executable path
and caches lookup results to avoid repeated subprocess calls.

The module exposes the following public function:

* :func:`git_info` - Retrieve details about Git and Git LFS availability

.. note::
   Git LFS information is only available when Git itself is installed. When Git
   LFS is not installed, the ``lfs`` entry will be present with ``installed``
   set to ``False`` and no version details.

Example::

    >>> from hbutils.system.git import git_info
    >>> info = git_info()
    >>> if info['installed']:
    ...     print(f"Git version: {info['version']}")
    ...     if info['lfs']['installed']:
    ...         print(f"Git LFS version: {info['lfs']['version']}")

"""

import os.path
import re
import shutil
import subprocess
import warnings
from functools import lru_cache
from typing import Any, Dict, Optional

__all__ = [
    'git_info',
]


@lru_cache()
def _raw_check_git(git_path: Optional[str]) -> Dict[str, Any]:
    """
    Check Git installation and version information.

    This function checks if Git is installed at the given path, retrieves its
    version information, and checks for Git LFS installation and version. The
    function is cached using :func:`functools.lru_cache` to avoid redundant
    system calls for the same ``git_path``.

    :param git_path: Path to the Git executable.
    :type git_path: Optional[str]
    :return: A dictionary containing information about Git and Git LFS
        installations. When Git is not installed, ``installed`` is ``False`` and
        no version details are included. If Git is installed, a ``lfs`` field
        is added with Git LFS details.
    :rtype: dict
    :warns UserWarning: If Git version information cannot be parsed or if Git is
        found but version check fails. Also raised if Git LFS version information
        is unrecognizable.

    Example::
        >>> info = _raw_check_git('/usr/bin/git')
        >>> print(info['installed'])
        True
        >>> print(info['version'])
        '2.34.1'
    """
    git_info: Dict[str, Any] = {}
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
        git_lfs_info: Dict[str, Any] = {}
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


def git_info(git_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Get information about Git and Git LFS installations.

    This function attempts to locate the Git executable and retrieve information
    about the Git and Git LFS installations. It first tries to use the provided
    ``git_path``, then checks the system ``PATH``, and finally falls back to
    ``None`` if Git is not found.

    The function normalizes ``git_path`` to ensure consistent caching behavior
    across different path representations of the same executable.

    :param git_path: Optional path to the Git executable. If not provided, the
        function will attempt to find Git in the system ``PATH`` using
        :func:`shutil.which`.
    :type git_path: Optional[str]
    :return: A dictionary containing information about Git and Git LFS
        installations. When Git is not installed, ``installed`` is ``False`` and
        ``lfs`` information is not included. When Git is installed, ``lfs`` is
        present, with ``installed`` indicating whether Git LFS is available.
    :rtype: dict
    :warns UserWarning: If Git version information cannot be parsed or if Git
        LFS version information is unrecognizable.

    Example::
        >>> info = git_info()
        >>> print(info['installed'])  # Check if Git is installed
        True
        >>> print(info['version'])    # Get Git version
        '2.34.1'
        >>> print(info['lfs']['installed'])  # Check if Git LFS is installed
        True

    Example with custom git path::
        >>> info = git_info('/usr/local/bin/git')
        >>> if info['installed']:
        ...     print(f"Using Git at: {info['exec']}")
        Using Git at: /usr/local/bin/git

    The returned dictionary has the following structure when Git is installed:

    .. code-block:: python

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
