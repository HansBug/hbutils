from typing import Dict

from ..os import is_windows

__all__ = [
    'hostfile', 'get_hosts', 'get_localhost_ip',
]


def hostfile() -> str:
    """
    Overview:
        Get host file in this os.

    :return: Host file path in this os.

    .. note::
        This should be ``/etc/hosts`` on Linux and macOS, but ``c:\windows\system32\drivers\etc\hosts`` on Windows.

    """
    return r"c:\windows\system32\drivers\etc\hosts" if is_windows() else '/etc/hosts'


def get_hosts() -> Dict[str, str]:
    """
    Overview:
        Get hosts content in form of dictionary.

    :return: A dictionary of the hosts file.

    Examples::
        >>> from hbutils.system import get_hosts
        >>> get_hosts()
        {'hansbug-VirtualBox': '127.0.0.1', 'localhost': '127.0.0.1'}

    """
    resdict = {}
    with open(hostfile(), 'r') as hf:
        for line in hf:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            _content, *_ = line.split('#', maxsplit=1)
            ip_address, *hostnames = _content.strip().split()
            for host in hostnames:
                resdict[host.strip()] = ip_address.strip()

    return resdict


_LOCALHOST = 'localhost'
_DEFAULT_LOCALHOST = '127.0.0.1'


def get_localhost_ip() -> str:
    """
    Overview:
        Get ip address of localhost.
        It will be checked in hosts, and just return ``127.0.0.1`` is not found.

    :return: IP address of ``localhost``.

    Examples::
        >>> from hbutils.system import get_localhost_ip
        >>> get_localhost_ip()
        '127.0.0.1'

    """
    return get_hosts().get(_LOCALHOST, _DEFAULT_LOCALHOST)
