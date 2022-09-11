"""
Overview:
    Capture for exitcode.
"""
from contextlib import contextmanager
from typing import ContextManager
from unittest.mock import patch

__all__ = [
    'capture_exit',
]

_DEFAULT_EXITCODE = 0


def _exitcode(status=None):
    return status if status is not None else _DEFAULT_EXITCODE


def _fake_exit(status=None):
    raise SystemExit(status)


class _ExitCapture:
    def __init__(self, exitcode):
        self.exitcode = exitcode


@contextmanager
def capture_exit(default=0) -> ContextManager[_ExitCapture]:
    """
    Overview:
        Capture for exitcode, :func:`quit` and :func:`sys.exit` can be captured.

    :param default: Default exitcode, default is ``0``.

    Examples::
        >>> from hbutils.testing import capture_exit
        >>> with capture_exit() as ex:
        ...     pass
        >>> ex.exitcode
        0
        >>>
        >>> with capture_exit() as ex:
        ...     quit()
        >>> ex.exitcode
        0
        >>>
        >>> with capture_exit() as ex:
        ...     quit(0xf)
        >>> ex.exitcode
        15
        >>>
        >>> import sys
        >>> with capture_exit() as ex:
        ...     sys.exit(0xf)
        >>> ex.exitcode
        15
    """
    capture = _ExitCapture(default)
    try:
        with patch('sys.exit', _fake_exit):
            yield capture
    except SystemExit as err:
        capture.exitcode = _exitcode(err.code)
