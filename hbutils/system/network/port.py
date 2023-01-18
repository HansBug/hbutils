import errno
import socket
import warnings
from typing import Optional, Iterable

from .hosts import get_localhost_ip

__all__ = [
    'is_free_port',
    'get_free_port',
]


def is_free_port(port: int) -> bool:
    """
    Overview:
        Check if given ``port`` is currently not in use and able to be allocated.

    :param port: Port to be checked.
    :return: In use or not.

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
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            s.bind((get_localhost_ip(), port))
        except PermissionError:
            return False
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                return False
            else:
                raise  # pragma: no cover
        else:
            return True

    finally:
        if s is not None:
            s.close()


def get_free_port(ports: Optional[Iterable[int]] = None, strict: bool = True) -> int:
    """
    Overview:
        Get allocatable port inside the given ``port``.

    :param ports: Range of ports to select.
    :param strict: Strictly use the ports in ``ports``. Default is ``False``, otherwise the ports \
        not in ``ports`` will probably be used.
    :param: A usable port.
    :raise OSError: Raise ``OSError`` when no ports can be allocated.

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
    """
    _ports = list(ports or [])
    if not strict or not _ports:
        if not _ports and strict:
            warnings.warn('No ports provided, so strict mode will be disabled.', stacklevel=2)
        _ports.append(0)

    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        for port in _ports:
            try:
                s.bind((get_localhost_ip(), port))
            except PermissionError:
                pass
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    pass
                else:
                    raise  # pragma: no cover
            else:
                _, port_ = s.getsockname()
                return port_

        raise OSError(f'No free port can be allocated with in {ports}.')
    finally:
        if s is not None:
            s.close()
