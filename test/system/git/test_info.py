import os.path
import shutil
from unittest import skipUnless

import pytest

from hbutils.system.git.info import git_info
from hbutils.testing import isolated_directory
from .conftest import _GIT_LFS, _GIT_RAW


@pytest.mark.unittest
class TestSystemGitInfo:
    @skipUnless(shutil.which('git'), 'Git required.')
    def test_git_installed(self):
        assert git_info()['installed']

    @skipUnless(not shutil.which('git'), 'No git required.')
    def test_git_not_installed(self):
        assert not git_info()['installed']

    def test_git_not_installed_tmp(self):
        with isolated_directory():
            assert git_info('git') == {
                'exec': None,
                'installed': False,
            }


@pytest.mark.unittest
class TestSystemGitInfoLFS:
    @skipUnless(_GIT_LFS, 'Pre-compiled git_lfs required')
    def test_git_info(self):
        assert git_info(_GIT_LFS) == {
            'exec': os.path.normcase(os.path.normpath(_GIT_LFS)),
            'installed': True,
            'lfs': {
                'installed': True,
                'version': '2.13.3',
                'version_info': 'git-lfs/2.13.3 (GitHub; linux amd64; go 1.16.2)'},
            'version': '2.30.0',
            'version_info': 'git version 2.30.0'
        }


@pytest.mark.unittest
class TestSystemGitInfoLFS:
    @skipUnless(_GIT_RAW, 'Pre-compiled git_lfs required')
    def test_git_info(self):
        assert git_info(_GIT_RAW) == {
            'exec': os.path.normcase(os.path.normpath(_GIT_RAW)),
            'installed': True,
            'lfs': {'installed': False},
            'version': '2.28.0',
            'version_info': 'git version 2.28.0'
        }
