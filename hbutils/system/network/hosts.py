"""
Host file utilities for cross-platform systems.

This module provides small utilities for locating and parsing the system
hosts file. It offers functions to resolve the hosts file path according to
the current operating system, parse host entries into a dictionary, and
retrieve the IP address of ``localhost``. The implementation supports
Windows and Unix-like platforms.

The module contains the following main components:

* :func:`hostfile` - Resolve the hosts file path for the current OS
* :func:`get_hosts` - Parse the hosts file into a hostname-to-IP mapping
* :func:`get_localhost_ip` - Retrieve the IP address associated with ``localhost``

Example::

    >>> from hbutils.system.network.hosts import hostfile, get_hosts, get_localhost_ip
    >>> hostfile()  # doctest: +SKIP
    '/etc/hosts'
    >>> hosts = get_hosts()  # doctest: +SKIP
    >>> hosts.get('localhost')  # doctest: +SKIP
    '127.0.0.1'
    >>> get_localhost_ip()  # doctest: +SKIP
    '127.0.0.1'

.. note::
   Parsing ignores empty lines and comments in the hosts file.
"""

from typing import Dict

from ..os import is_windows

__all__ = [
    'hostfile', 'get_hosts', 'get_localhost_ip',
]


def hostfile() -> str:
    """
    Get the hosts file path for the current operating system.

    :return: Hosts file path on this operating system.
    :rtype: str

    .. note::
       This should be ``/etc/hosts`` on Linux and macOS, and
       ``c:\\windows\\system32\\drivers\\etc\\hosts`` on Windows.

    Examples::
        >>> from hbutils.system.network.hosts import hostfile
        >>> hostfile()  # On Linux/macOS  # doctest: +SKIP
        '/etc/hosts'
        >>> hostfile()  # On Windows  # doctest: +SKIP
        'c:\\\\windows\\\\system32\\\\drivers\\\\etc\\\\hosts'
    """
    return r"c:\windows\system32\drivers\etc\hosts" if is_windows() else '/etc/hosts'


def get_hosts() -> Dict[str, str]:
    """
    Parse the system hosts file into a dictionary.

    This function reads the system hosts file line-by-line and constructs a
    mapping from each hostname to its associated IP address. Inline comments
    (starting with ``#``) and blank lines are ignored.

    :return: Dictionary mapping hostnames to their corresponding IP addresses.
    :rtype: Dict[str, str]

    Examples::
        >>> from hbutils.system.network.hosts import get_hosts
        >>> get_hosts()  # doctest: +SKIP
        {'hansbug-VirtualBox': '127.0.0.1', 'localhost': '127.0.0.1'}
    """
    resdict: Dict[str, str] = {}
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
    Get the IP address of ``localhost``.

    This function retrieves the IP address associated with ``localhost`` from
    the system hosts file. If ``localhost`` is not present, it returns the
    default value ``127.0.0.1``.

    :return: IP address of ``localhost``.
    :rtype: str

    Examples::
        >>> from hbutils.system.network.hosts import get_localhost_ip
        >>> get_localhost_ip()  # doctest: +SKIP
        '127.0.0.1'
    """
    return get_hosts().get(_LOCALHOST, _DEFAULT_LOCALHOST)
