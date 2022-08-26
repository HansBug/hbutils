import os.path
import pathlib
from unittest.mock import patch, MagicMock

import pytest

from hbutils.system import get_localhost_ip, get_hosts
from hbutils.testing import isolated_directory

HOST_FILE_EXAMPLE = """
# Kubernetes-managed hosts file.
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
fe00::0 ip6-mcastprefix
fe00::1 ip6-allnodes
fe00::2 ip6-allrouters
10.148.116.89   hansbug-dev-double-gpu-2

# Entries added by HostAliases.
1.2.3.4 example.com
"""


@pytest.fixture()
def fake_hostfile():
    with isolated_directory():
        pathlib.Path('hosts').write_text(HOST_FILE_EXAMPLE)
        hostfile_path = os.path.abspath('hosts')

        with patch('hbutils.system.network.hosts.hostfile', MagicMock(return_value=hostfile_path)):
            yield hostfile_path


@pytest.mark.unittest
class TestSystemNetworkHosts:
    def test_get_localhost_ip(self):
        assert get_localhost_ip() in {'127.0.0.1', '::1'}

    def test_try_fake_hosts(self, fake_hostfile):
        assert get_hosts() == {
            'localhost': '::1',
            'ip6-localhost': '::1',
            'ip6-loopback': '::1',
            'ip6-localnet': 'fe00::0',
            'ip6-mcastprefix': 'fe00::0',
            'ip6-allnodes': 'fe00::1',
            'ip6-allrouters': 'fe00::2',
            'hansbug-dev-double-gpu-2': '10.148.116.89',
            'example.com': '1.2.3.4'
        }
