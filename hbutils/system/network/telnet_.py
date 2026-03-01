"""
Network connectivity helpers for port availability checks.

This module provides lightweight, telnet-like connectivity checks to determine
whether a TCP port is open and accepting connections. It also provides a polling
utility to wait for a port to become available within a specified timeout.

The module contains the following main components:

* :func:`telnet` - Check connectivity to a TCP host and port.
* :func:`wait_for_port_online` - Poll a host and port until it becomes available.

.. note::
   These utilities establish a TCP connection only. They do not perform any
   protocol-level handshake beyond the TCP connect operation.

Example::

    >>> from hbutils.system.network.telnet_ import telnet, wait_for_port_online
    >>> telnet('127.0.0.1', 8080, timeout=1.0)
    False
    >>> wait_for_port_online('127.0.0.1', 8080, timeout=5.0, interval=0.5)
"""

import socket
import time
from typing import Optional

__all__ = [
    'telnet', 'wait_for_port_online',
]


def telnet(host: str, port: int, timeout: float = 5.0) -> bool:
    """
    Attempt to connect to a TCP host and port.

    This function performs a TCP connection attempt, similar to a telnet check,
    and returns whether the connection was successfully established within the
    provided timeout.

    :param host: Host address to connect to, for example ``"127.0.0.1"``.
    :type host: str
    :param port: TCP port number to test, for example ``8080``.
    :type port: int
    :param timeout: Maximum timeout duration in seconds, defaults to ``5.0``.
    :type timeout: float
    :return: ``True`` if the port is online and responding, ``False`` otherwise.
    :rtype: bool
    :raises OSError: For unexpected socket errors not related to refusal or timeout.

    .. note::
       This function only checks for the ability to establish a TCP connection.
       It does not validate application-level protocols.

    Example::

        >>> telnet('127.0.0.1', 8080, timeout=3.0)
        True
        >>> telnet('127.0.0.1', 9999, timeout=1.0)
        False
    """
    try:
        sock = None
        try:
            sock = socket.create_connection((host, port), timeout)
            return True
        finally:
            if sock:
                sock.close()
    except (ConnectionRefusedError, socket.timeout):
        # ConnectionRefusedError is for Linux and macOS
        # socket.timeout is for Windows
        return False


def wait_for_port_online(host: str, port: int, timeout: Optional[float] = 5,
                         interval: float = 0.3) -> None:
    """
    Wait until a TCP port becomes available.

    This function repeatedly calls :func:`telnet` at a fixed interval until the
    target port is online or the timeout is reached.

    :param host: Host address to connect to, for example ``"127.0.0.1"``.
    :type host: str
    :param port: TCP port number to test, for example ``8080``.
    :type port: int
    :param timeout: Maximum timeout duration in seconds. ``None`` means wait
        indefinitely, defaults to ``5``.
    :type timeout: Optional[float]
    :param interval: Time interval between consecutive checks in seconds,
        defaults to ``0.3``.
    :type interval: float
    :return: ``None``. The function returns when the port is online.
    :rtype: None
    :raises TimeoutError: If the timeout is reached and the port is still offline.

    Example::

        >>> wait_for_port_online('127.0.0.1', 8080, timeout=10, interval=0.5)
        >>> wait_for_port_online('localhost', 3306, timeout=None)
    """
    _start_time = time.time()
    while True:
        if telnet(host, port, interval):
            return

        if timeout is not None and time.time() > _start_time + timeout:
            raise TimeoutError(f'Wait for {host}:{port} for {time.time() - _start_time:.3f}s, '
                               f'but still offline.')
