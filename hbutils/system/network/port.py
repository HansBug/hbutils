"""
Network port availability and allocation utilities.

This module provides lightweight helpers to check whether a TCP port is
available on localhost and to allocate a free port within a given range.
For safety and common OS restrictions, only ports greater than or equal to
1024 are considered in range-based allocation.

The module contains the following public functions:

* :func:`is_free_port` - Check whether a specific port is available.
* :func:`get_free_port` - Find a free port within an optional iterable of ports.

.. note::
   Port allocation is performed on localhost (``127.0.0.1``) using TCP sockets.

Example::

    >>> from hbutils.system.network.port import is_free_port, get_free_port
    >>> is_free_port(8080)
    True
    >>> get_free_port(range(8000, 8100))
    8000

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
    Check if a port is currently not in use and can be allocated.

    This function attempts to connect to the given port on localhost. If the
    connection fails, the port is considered free.

    :param port: Port to be checked.
    :type port: int
    :return: ``True`` if the port is free; ``False`` if it is in use.
    :rtype: bool

    Example::

        >>> from hbutils.system.network.port import is_free_port
        >>> is_free_port(22)
        False
        >>> is_free_port(8080)
        True
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


def get_free_port(ports: Optional[Iterable[int]] = None, strict: bool = True) -> int:
    """
    Get an allocatable port inside the given ``ports`` range.

    This function searches for an available port within the specified iterable.
    For security reasons, only ports numbered 1024 and above are considered.
    When ``strict`` is ``True`` and no usable port is available, an
    :class:`OSError` is raised. When ``strict`` is ``False``, a free port will
    be allocated by the OS even if it is not in the provided range.

    If ``ports`` is ``None`` or contains no ports >= 1024 while ``strict`` is
    ``True``, strict mode is automatically disabled and a warning is emitted.

    :param ports: Iterable of candidate ports to select from. If ``None`` or empty,
        behavior depends on ``strict``.
    :type ports: Optional[Iterable[int]]
    :param strict: Strictly use the ports in ``ports``. If ``False``, ports not
        in ``ports`` may be used when no port in range is available.
    :type strict: bool
    :return: A usable port number.
    :rtype: int
    :raises OSError: Raised when no ports can be allocated in strict mode.

    .. note::
       Due to OS safety considerations, only ports >= 1024 are used.

    .. warning::
       If no usable ports are provided while ``strict`` is ``True``, a
       :func:`warnings.warn` call is triggered and strict mode is disabled.

    Example::

        >>> from hbutils.system.network.port import get_free_port
        >>> get_free_port(range(22, 1060))
        1024
        >>> get_free_port(range(1080, 2080, 10))  # assume that 1080 is in use
        1090
        >>> get_free_port(range(22, 80))
        OSError: No free port can be allocated with in range(22, 80).
        >>> get_free_port(range(22, 80), strict=False)
        44317
        >>> get_free_port()
        49152
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
