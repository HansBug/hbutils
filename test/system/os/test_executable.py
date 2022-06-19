import os
import unittest

import pytest

from hbutils.system import which, where
from hbutils.testing import OS


@pytest.mark.unittest
class TestSystemOSExecutable:
    @unittest.skipUnless(OS.linux or OS.macos, 'Linux and macOS only')
    def test_which_linux(self):
        bash_path = which('bash')

        assert os.path.exists(bash_path)
        assert os.path.isfile(bash_path)
        assert os.access(bash_path, os.R_OK)

        _, filename = os.path.split(bash_path)
        assert filename == 'bash'

        assert which('not_exist') is None

    @unittest.skipUnless(OS.windows, 'Windows only')
    def test_which_windows(self):
        cmd_path = which('cmd')
        assert os.path.exists(cmd_path)
        assert os.path.isfile(cmd_path)
        assert os.access(cmd_path, os.R_OK)

        _, filename = os.path.split(cmd_path)
        assert filename == 'cmd.exe'

        assert which('not_exist') is None

    @unittest.skipUnless(OS.linux or OS.macos, 'Linux and macOS only')
    def test_where_linux(self):
        bashes = where('bash')
        assert bashes
        for b in bashes:
            assert os.path.exists(b)
            assert os.path.isfile(b)
            assert os.access(b, os.R_OK)

            _, filename = os.path.split(b)
            assert filename == 'bash'

    @unittest.skipUnless(OS.windows, 'Windows only')
    def test_where_windows(self):
        cmds = where('cmd')
        assert cmds
        for c in cmds:
            assert os.path.exists(c)
            assert os.path.isfile(c)
            assert os.access(c, os.R_OK)

            _, filename = os.path.split(c)
            assert filename == 'cmd.exe'
