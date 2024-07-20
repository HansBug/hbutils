import shutil
from unittest import skipUnless

import pytest

from hbutils.testing import isolated_directory
from hbutils.testing.requires import is_git_installed, is_git_lfs_installed, git_version, git_lfs_version
from .conftest import _GIT_LFS, _GIT_RAW


@pytest.mark.unittest
class TestTestingRequiresGitNative:
    @skipUnless(shutil.which('git'), 'Git required.')
    def test_is_git_installed(self):
        assert is_git_installed()

    @skipUnless(not shutil.which('git'), 'No git required.')
    def test_is_git_installed_not_installed(self):
        assert not is_git_installed()

    def test_is_git_installed_negative(self):
        with isolated_directory():
            assert not is_git_installed('git')
            assert git_version('git') is None
            assert not is_git_lfs_installed('git')
            assert git_lfs_version('git') is None


@pytest.mark.unittest
class TestTestingRequiresGitLFS:
    @skipUnless(_GIT_LFS, 'Pre-compiled git_lfs required')
    def test_is_git_installed(self):
        assert is_git_installed(_GIT_LFS)

    @skipUnless(_GIT_LFS, 'Pre-compiled git_lfs required')
    def test_git_version(self):
        assert git_version(_GIT_LFS) == '2.30.0'

    @skipUnless(_GIT_LFS, 'Pre-compiled git_lfs required')
    def test_is_git_lfs_installed(self):
        assert is_git_lfs_installed(_GIT_LFS)

    @skipUnless(_GIT_LFS, 'Pre-compiled git_lfs required')
    def test_git_lfs_version(self):
        assert git_lfs_version(_GIT_LFS) == '2.13.3'


@pytest.mark.unittest
class TestTestingRequiresGitRAW:
    @skipUnless(_GIT_RAW, 'Pre-compiled git_raw required')
    def test_is_git_installed(self):
        assert is_git_installed(_GIT_RAW)

    @skipUnless(_GIT_RAW, 'Pre-compiled git_raw required')
    def test_git_version(self):
        assert git_version(_GIT_RAW) == '2.28.0'

    @skipUnless(_GIT_RAW, 'Pre-compiled git_raw required')
    def test_is_git_lfs_installed(self):
        assert not is_git_lfs_installed(_GIT_RAW)

    @skipUnless(_GIT_RAW, 'Pre-compiled git_raw required')
    def test_git_lfs_version(self):
        assert git_lfs_version(_GIT_RAW) is None
