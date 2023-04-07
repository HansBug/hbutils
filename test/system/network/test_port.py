from unittest import skipUnless

import pytest

from hbutils.system import get_free_port, is_free_port
from hbutils.testing import OS


@pytest.mark.unittest
class TestSystemNetworkPort:
    def test_is_free_port(self):
        assert is_free_port(35126)
        assert not is_free_port(35127)
        assert not is_free_port(35128)
        assert is_free_port(35129)

    def test_get_free_port_native(self):
        port = get_free_port(range(35127, 35227))
        assert port == 35129

        with pytest.warns(Warning):
            port = get_free_port()
            assert port > 0

    @skipUnless(OS.linux, 'linux required')
    def test_get_free_port_native_linux(self):
        port = get_free_port(range(1, 2000))
        assert port >= 1024

    @skipUnless(OS.windows or OS.macos, 'windows or macos required')
    def test_get_free_port_native_non_linux(self):
        port = get_free_port(range(1, 2000))
        assert port >= 1

    def test_get_free_port_inuse(self):
        port = get_free_port(range(35127, 35227))
        assert port == 35129

        port = get_free_port(range(35126, 35227))
        assert port == 35126

        with pytest.raises(OSError):
            _ = get_free_port([35127, 35128])

    def test_get_free_port_inuse_non_strict(self):
        port = get_free_port([35127, 35128], strict=False)
        assert port > 0

        port = get_free_port(strict=False)
        assert port > 0
