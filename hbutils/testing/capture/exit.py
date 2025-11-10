"""
Overview:
    Capture for exitcode. This module provides utilities to capture system exit codes
    from calls to `sys.exit()` and `quit()` functions, allowing tests to verify exit
    behavior without actually terminating the process.
"""
from contextlib import contextmanager
from typing import ContextManager
from unittest.mock import patch

__all__ = [
    'capture_exit', 'ExitCaptureResult'
]

_DEFAULT_EXITCODE = 0


def _exitcode(status=None):
    """
    Normalize the exit status code.

    :param status: The exit status code, can be None or an integer.
    :type status: int or None
    :return: The normalized exit code, returns default if status is None.
    :rtype: int
    """
    return status if status is not None else _DEFAULT_EXITCODE


def _fake_exit(status=None):
    """
    Fake exit function that raises SystemExit instead of terminating the process.

    :param status: The exit status code.
    :type status: int or None
    :raises SystemExit: Always raises SystemExit with the given status.
    """
    raise SystemExit(status)


class ExitCaptureResult:
    """
    Overview:
        Model of exit capture result. This class stores the captured exit code
        from a context where system exits are intercepted.
    """

    def __init__(self, exitcode):
        """
        Constructor of :class:`ExitCaptureResult`.

        :param exitcode: Initial exitcode value.
        :type exitcode: int
        """
        self.__exitcode = exitcode

    @property
    def exitcode(self) -> int:
        """
        Get the captured exitcode value.

        :return: The exit code that was captured.
        :rtype: int

        .. note::
            Do not use this property when :func:`capture_exit` is not over, otherwise this result \
                is not guaranteed to be correct.
        """
        return self.__exitcode

    def put_result(self, exitcode: int):
        """
        Put result inside this model.

        :param exitcode: New exitcode value to store.
        :type exitcode: int
        """
        self.__exitcode = exitcode


@contextmanager
def capture_exit(default: int = 0) -> ContextManager[ExitCaptureResult]:
    """
    Overview:
        Capture for exitcode, :func:`quit` and :func:`sys.exit` can be captured.
        This context manager intercepts system exit calls and stores the exit code
        in an :class:`ExitCaptureResult` object instead of terminating the process.

    :param default: Default exitcode when no exit is called, default is ``0``.
    :type default: int
    :return: A context manager that yields an ExitCaptureResult object.
    :rtype: ContextManager[ExitCaptureResult]

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
    capture = ExitCaptureResult(default)
    try:
        with patch('sys.exit', _fake_exit):
            yield capture
    except SystemExit as err:
        capture.put_result(_exitcode(err.code))
