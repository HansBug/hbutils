"""
This module provides network utility functions for checking port availability and waiting for ports to come online.

It includes functions to perform telnet-like connectivity checks and wait for network services to become available.
"""

import socket
import time

__all__ = [
    'telnet', 'wait_for_port_online',
]

from typing import Optional


def telnet(host: str, port: int, timeout: float = 5.0) -> bool:
    """
    Perform a telnet operation on the given port and return ``True`` if a response is received
    within the timeout period, otherwise return ``False``.

    :param host: Host address to connect to, e.g. ``127.0.0.1``.
    :type host: str
    :param port: Port number to test, e.g. ``32768``.
    :type port: int
    :param timeout: Maximum timeout duration in seconds, defaults to 5.0.
    :type timeout: float
    :return: ``True`` if port is online and responding, ``False`` otherwise.
    :rtype: bool

    Example::
        >>> telnet('127.0.0.1', 8080, timeout=3.0)  # Check if port 8080 is available
        True
        >>> telnet('127.0.0.1', 9999, timeout=1.0)  # Check unavailable port
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


def wait_for_port_online(host: str, port: int, timeout: Optional[float] = 5, interval: float = 0.3):
    """
    Wait for the given interface to be in an online state.

    This function continuously checks if a port is available by performing telnet operations
    at regular intervals until the port comes online or the timeout is reached.

    :param host: Host address to connect to, e.g. ``127.0.0.1``.
    :type host: str
    :param port: Port number to test, e.g. ``32768``.
    :type port: int
    :param timeout: Maximum timeout duration in seconds. ``None`` means wait forever, defaults to 5.
    :type timeout: Optional[float]
    :param interval: Time interval between consecutive telnet checks in seconds, defaults to 0.3.
    :type interval: float
    :raises TimeoutError: Raised when timeout is reached and the port is still offline.

    Example::
        >>> wait_for_port_online('127.0.0.1', 8080, timeout=10, interval=0.5)  # Wait up to 10 seconds
        >>> wait_for_port_online('localhost', 3306, timeout=None)  # Wait indefinitely
    """
    _start_time = time.time()
    while True:
        if telnet(host, port, interval):
            return

        if timeout is not None and time.time() > _start_time + timeout:
            raise TimeoutError(f'Wait for {host}:{port} for {time.time() - _start_time:.3f}s, '
                               f'but still offline.')
