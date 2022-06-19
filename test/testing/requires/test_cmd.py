import unittest

import pytest

from hbutils.testing import cmdv, OS


@pytest.mark.unittest
class TestTestingRequiresCmd:
    @unittest.skipUnless(OS.linux or OS.macos, 'Linux and macOS only')
    def test_cmdv_linux(self):
        assert cmdv('bash')
        assert not cmdv('cmd')
        assert not cmdv('not_exist')
        assert cmdv('python') or cmdv('python3')

    @unittest.skipUnless(OS.windows, 'Windows only')
    def test_cmdv_windows(self):
        assert cmdv('cmd')
        assert not cmdv('not_exist')
        assert cmdv('python') or cmdv('python3')
