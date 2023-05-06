import pytest

from hbutils.system import telnet, wait_for_port_online


@pytest.mark.unittest
class TestSystemNetworkTelnet:
    def test_telnet(self):
        assert telnet('127.0.0.1', 35127)
        assert telnet('127.0.0.1', 35128)
        assert not telnet('127.0.0.1', 35129, timeout=1.0)

    def test_wait_for_port_online(self):
        wait_for_port_online('127.0.0.1', 35127)
        wait_for_port_online('127.0.0.1', 35128)

        with pytest.raises(TimeoutError):
            wait_for_port_online('127.0.0.1', 35129, timeout=2.0, interval=0.1)
