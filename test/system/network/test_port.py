import pytest

from hbutils.system import get_free_port, is_free_port
from .conftest import start_http_server


@pytest.mark.unittest
class TestSystemNetworkPort:
    def test_is_free_port(self):
        assert not is_free_port(80)  # do not put 80 inside start_http_server
        with start_http_server(35127), start_http_server(35128):
            assert is_free_port(35126)
            assert not is_free_port(35127)
            assert not is_free_port(35128)
            assert is_free_port(35129)

    def test_get_free_port_native(self):
        port = get_free_port(range(35127, 35227))
        assert port == 35127

        with pytest.warns(Warning):
            port = get_free_port()
            assert port > 0

        port = get_free_port(range(1, 2000))
        assert port >= 1024

    def test_get_free_port_inuse(self):
        with start_http_server(35127):
            port = get_free_port(range(35127, 35227))
            assert port == 35128

        with start_http_server(35127):
            port = get_free_port(range(35126, 35227))
            assert port == 35126

        with start_http_server(35127), start_http_server(35128):
            port = get_free_port(range(35127, 35227))
            assert port == 35129

        with start_http_server(35127), start_http_server(35128):
            with pytest.raises(OSError):
                _ = get_free_port([35127, 35128])

    def test_get_free_port_inuse_non_strict(self):
        with start_http_server(35127), start_http_server(35128):
            port = get_free_port([35127, 35128], strict=False)
            assert port > 0

        port = get_free_port(strict=False)
        assert port > 0
