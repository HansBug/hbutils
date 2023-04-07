import socket
import warnings
from typing import Optional, Iterable

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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


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
