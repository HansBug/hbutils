"""
This module provides utilities for managing and querying host file information across different operating systems.

It includes functions to locate the host file path, parse host entries, and retrieve localhost IP address.
The module handles platform-specific differences between Windows and Unix-like systems.
"""

from typing import Dict

from ..os import is_windows

__all__ = [
    'hostfile', 'get_hosts', 'get_localhost_ip',
]


def hostfile() -> str:
    """
    Get host file path in this operating system.

    :return: Host file path in this os.
    :rtype: str

    .. note::
        This should be ``/etc/hosts`` on Linux and macOS, but ``c:\\windows\\system32\\drivers\\etc\\hosts`` on Windows.

    Examples::
        >>> from hbutils.system import hostfile
        >>> hostfile()  # On Linux/macOS
        '/etc/hosts'
        >>> hostfile()  # On Windows
        'c:\\windows\\system32\\drivers\\etc\\hosts'
    """
    return r"c:\windows\system32\drivers\etc\hosts" if is_windows() else '/etc/hosts'


def get_hosts() -> Dict[str, str]:
    """
    Get hosts content in form of dictionary.

    This function parses the system hosts file and returns a dictionary mapping
    hostnames to their corresponding IP addresses. Comments and empty lines are
    automatically ignored during parsing.

    :return: A dictionary of the hosts file where keys are hostnames and values are IP addresses.
    :rtype: Dict[str, str]

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
    Get IP address of localhost.

    This function retrieves the IP address associated with 'localhost' from the
    system hosts file. If 'localhost' is not found in the hosts file, it returns
    the default localhost IP address ``127.0.0.1``.

    :return: IP address of ``localhost``.
    :rtype: str

    Examples::
        >>> from hbutils.system import get_localhost_ip
        >>> get_localhost_ip()
        '127.0.0.1'
    """
    return get_hosts().get(_LOCALHOST, _DEFAULT_LOCALHOST)
