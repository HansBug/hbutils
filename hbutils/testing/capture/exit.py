"""
Exit code capture utilities for test environments.

This module provides context managers and result models for capturing exit codes
raised by :func:`sys.exit` or :func:`quit` without terminating the running
process. It is primarily intended for unit testing scenarios where code paths
that call system exit functions need to be verified safely.

The module contains the following main components:

* :class:`ExitCaptureResult` - Stores the captured exit code
* :func:`capture_exit` - Context manager that intercepts exit calls

.. note::
   The implementation patches :func:`sys.exit`. The built-in :func:`quit`
   delegates to :func:`sys.exit`, so it is captured by the same mechanism.

Example::

    >>> from hbutils.testing.capture.exit import capture_exit
    >>> with capture_exit() as result:
    ...     pass
    >>> result.exitcode
    0
    >>> with capture_exit() as result:
    ...     quit(3)
    >>> result.exitcode
    3
"""
from contextlib import contextmanager
from typing import ContextManager, Optional
from unittest.mock import patch

__all__ = [
    'capture_exit', 'ExitCaptureResult'
]

_DEFAULT_EXITCODE = 0


def _exitcode(status: Optional[int] = None) -> int:
    """
    Normalize the exit status code.

    :param status: Exit status code returned by :exc:`SystemExit` or ``None``.
    :type status: int or None
    :return: Normalized exit code, defaults to ``0`` when ``status`` is ``None``.
    :rtype: int
    """
    return status if status is not None else _DEFAULT_EXITCODE


def _fake_exit(status: Optional[int] = None) -> None:
    """
    Fake exit function that raises :exc:`SystemExit` instead of terminating.

    :param status: Exit status code passed to :func:`sys.exit`.
    :type status: int or None
    :raises SystemExit: Always raised with the provided ``status``.
    """
    raise SystemExit(status)


class ExitCaptureResult:
    """
    Model of exit capture result.

    This class stores the captured exit code from a context where exit calls
    are intercepted by :func:`capture_exit`.

    :param exitcode: Initial exit code to store.
    :type exitcode: int
    """

    def __init__(self, exitcode: int) -> None:
        """
        Initialize the result container.

        :param exitcode: Initial exit code to store.
        :type exitcode: int
        """
        self.__exitcode = exitcode

    @property
    def exitcode(self) -> int:
        """
        Get the captured exit code.

        :return: The exit code captured by :func:`capture_exit`.
        :rtype: int

        .. note::
           Do not access this property before :func:`capture_exit` finishes,
           otherwise the result may not be finalized.
        """
        return self.__exitcode

    def put_result(self, exitcode: int) -> None:
        """
        Store the captured exit code.

        :param exitcode: Exit code to store.
        :type exitcode: int
        """
        self.__exitcode = exitcode


@contextmanager
def capture_exit(default: int = 0) -> ContextManager[ExitCaptureResult]:
    """
    Capture system exit calls and store the resulting exit code.

    This context manager intercepts calls to :func:`sys.exit` (and therefore
    :func:`quit`) and stores the exit code in an :class:`ExitCaptureResult`
    instance instead of terminating the process.

    :param default: Default exit code when no exit is invoked, defaults to ``0``.
    :type default: int
    :return: Context manager yielding an :class:`ExitCaptureResult` instance.
    :rtype: ContextManager[ExitCaptureResult]

    Example::

        >>> from hbutils.testing.capture.exit import capture_exit
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
