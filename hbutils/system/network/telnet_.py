import socket
import time

__all__ = [
    'telnet', 'wait_for_port_online',
]

from typing import Optional


def telnet(host, port: int, timeout: float = 5.0) -> bool:
    """
    Overview:
        Perform a telnet operation on the given port and return ``True`` if a response is received
        within the timeout period, otherwise return ``False``.

    :param host: Host, e.g. ``127.0.0.1``.
    :param port: Port to test, e.g. ``32768``.
    :param timeout: Maximum timeout duration in seconds.
    :return: Port is on or not.

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


def wait_for_port_online(host, port: int, timeout: Optional[float] = 5, interval: float = 0.3):
    """
    Overview:
        Wait for the given interface to be in an online state.

    :param host: Host, e.g. ``127.0.0.1``.
    :param port: Port to test, e.g. ``32768``.
    :param timeout: Maximum timeout duration in seconds. ``None`` means wait it forever.
    :param interval: Timeout for every :func:`telnet` operation.
    :raises TimeoutError: Raise this when timeout is reached and the port is still offline.
    """
    _start_time = time.time()
    while True:
        if telnet(host, port, interval):
            return

        if timeout is not None and time.time() > _start_time + timeout:
            raise TimeoutError(f'Wait for {host}:{port} for {time.time() - _start_time:.3f}s, '
                               f'but still offline.')
