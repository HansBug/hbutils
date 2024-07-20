import os.path
import re
import shutil
import subprocess
import warnings
from functools import lru_cache
from typing import Optional


@lru_cache()
def _raw_check_git(git_path: str):
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
    git_path = git_path or shutil.which('git') or None
    if git_path:
        git_path = os.path.normcase(os.path.normpath(git_path))
    return _raw_check_git(git_path)
