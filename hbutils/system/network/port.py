"""
This module provides utilities for checking and allocating free network ports.

The module contains functions to verify if a port is available and to find
an available port within a specified range. It ensures safe port allocation
by restricting usage to ports above 1024 for security reasons.
"""

import socket
import warnings
from typing import Optional, Iterable

__all__ = [
    'is_free_port',
    'get_free_port',
]


def is_free_port(port: int) -> bool:
    """
    Check if given ``port`` is currently not in use and able to be allocated.

    :param port: Port to be checked.
    :type port: int
    :return: True if the port is free, False if it is in use.
    :rtype: bool

    Examples::
        >>> from hbutils.system import is_free_port
        >>> is_free_port(22)
        False
        >>> is_free_port(80)
        False
        >>> is_free_port(8080)
        True
        >>> is_free_port(35022)
        True
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


def get_free_port(ports: Optional[Iterable[int]] = None, strict: bool = True) -> int:
    """
    Get allocatable port inside the given ``ports`` range.

    This function searches for an available port within the specified range.
    For security reasons, only ports numbered 1024 and above are considered.
    If strict mode is disabled and no port in the range is available, the
    system will allocate any available port.

    :param ports: Range of ports to select from. If None, behavior depends on strict parameter.
    :type ports: Optional[Iterable[int]]
    :param strict: Strictly use the ports in ``ports``. Default is ``True``. If ``False``, \
        ports not in ``ports`` may be used when no port in range is available.
    :type strict: bool
    :return: A usable port number.
    :rtype: int
    :raises OSError: Raised when no ports can be allocated in strict mode.

    Examples::
        >>> from hbutils.system import get_free_port
        >>> get_free_port(range(22, 1060))
        1024
        >>> get_free_port(range(1080, 2080, 10))  # assume that 1080 is in use
        1090
        >>> get_free_port(range(22, 80))
        OSError: No free port can be allocated with in range(22, 80).
        >>> get_free_port(range(22, 80), strict=False)
        44317

    .. note::
        Due to the safety consideration of OS, only ports over 1024 will be used.
    """
    _ports = [p for p in (ports or []) if p >= 1024]
    if not strict or not _ports:
        if not _ports and strict:
            warnings.warn('No usable ports provided, so strict mode will be disabled.', stacklevel=2)
            strict = False

    if _ports:
        for port in _ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if s.connect_ex(('localhost', port)) != 0:
                    return port

    if not strict:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', 0))
            _, port_ = s.getsockname()
            return port_
    else:
        raise OSError(f'No free port can be allocated with in {ports}.')
