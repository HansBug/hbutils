import unittest

import pytest
from easydict import EasyDict

from hbutils.testing import OS, disable_output
from ...testings import windows_mark, linux_mark, macos_mark


@pytest.mark.ignore
class _TestOS(unittest.TestCase):
    # noinspection PyPep8Naming
    def __init__(self, methodName: str, v):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.v = v

    @unittest.skipUnless(OS.linux, 'linux only.')
    def test_linux(self):
        self.v.is_linux = True

    @unittest.skipUnless(OS.windows, 'windows_only.')
    def test_windows(self):
        self.v.is_windows = True

    @unittest.skipUnless(OS.macos, 'macos_only.')
    def test_macos(self):
        self.v.is_macos = True


class TestTestingRequiresOS:
    @windows_mark
    def test_with_os_windows(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestOS('test_linux', d))
            runner.run(_TestOS('test_windows', d))
            runner.run(_TestOS('test_macos', d))

        assert d == {'is_windows': True}

    @linux_mark
    def test_with_os_linux(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestOS('test_linux', d))
            runner.run(_TestOS('test_windows', d))
            runner.run(_TestOS('test_macos', d))

        assert d == {'is_linux': True}

    @macos_mark
    def test_with_os_macos(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestOS('test_linux', d))
            runner.run(_TestOS('test_windows', d))
            runner.run(_TestOS('test_macos', d))

        assert d == {'is_macos': True}
