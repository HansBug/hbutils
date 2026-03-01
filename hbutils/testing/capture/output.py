"""
Utilities for capturing, redirecting, and disabling standard output streams.

This module provides context managers that make it easy to capture or suppress
output written to ``sys.stdout`` and ``sys.stderr`` during a block of code.
It supports both in-memory capturing (via :class:`io.StringIO`) and file-based
capturing (via temporary files), as well as complete suppression by redirecting
output to the platform's null device.

The module exposes the following public components:

* :class:`OutputCaptureResult` - Thread-safe container for captured output
* :func:`capture_output` - Capture output within a ``with`` block
* :func:`disable_output` - Suppress output within a ``with`` block

Example::

    >>> import sys
    >>> from hbutils.testing.capture.output import capture_output, disable_output
    >>>
    >>> with capture_output() as result:
    ...     print("hello stdout")
    ...     print("hello stderr", file=sys.stderr)
    ...
    >>> result.stdout
    'hello stdout\\n'
    >>> result.stderr
    'hello stderr\\n'
    >>>
    >>> with disable_output():
    ...     print("this will not appear")

.. note::
   When capturing output in memory (``mem=True``), :class:`io.StringIO` is used.
   This object does not provide ``fileno()``, which may affect libraries that
   require a real file descriptor (e.g., :func:`subprocess.run`).

"""
import io
import os
import pathlib
from contextlib import redirect_stdout, redirect_stderr, contextmanager
from threading import Lock
from typing import ContextManager, Optional

__all__ = [
    'OutputCaptureResult',
    'capture_output', 'disable_output',
]

from ...system import TemporaryDirectory


class OutputCaptureResult:
    """
    Thread-safe container for captured stdout and stderr content.

    This class stores the captured output from :func:`capture_output` and allows
    safe access from multiple threads. Accessing :attr:`stdout` or :attr:`stderr`
    before the capture context has exited will block until the capture is done.

    Example::

        >>> import sys
        >>> from hbutils.testing.capture.output import capture_output
        >>> with capture_output() as result:
        ...     print("x")
        ...     print("y", file=sys.stderr)
        ...
        >>> result.stdout
        'x\\n'
        >>> result.stderr
        'y\\n'

    .. warning::
       Accessing :attr:`stdout` or :attr:`stderr` before the capture context is
       finished will block due to internal locking.
    """

    def __init__(self) -> None:
        """
        Initialize an empty capture result.

        The instance starts with ``None`` values for both stdout and stderr and
        uses an acquired lock to block access until results are set.
        """
        self._stdout = None
        self._stderr = None
        self._lock = Lock()
        self._lock.acquire()

    def put_result(self, stdout: Optional[str], stderr: Optional[str]) -> None:
        """
        Store the captured stdout and stderr results.

        :param stdout: Captured stdout content.
        :type stdout: Optional[str]
        :param stderr: Captured stderr content.
        :type stderr: Optional[str]
        """
        self._stdout, self._stderr = stdout, stderr
        self._lock.release()

    @property
    def stdout(self) -> Optional[str]:
        """
        Captured stdout content.

        :return: The captured stdout text, or ``None`` if capture failed.
        :rtype: Optional[str]

        .. note::
           Do not access this property before the :func:`capture_output`
           context has exited, or the call will block.
        """
        with self._lock:
            return self._stdout

    @property
    def stderr(self) -> Optional[str]:
        """
        Captured stderr content.

        :return: The captured stderr text, or ``None`` if capture failed.
        :rtype: Optional[str]

        .. note::
           Do not access this property before the :func:`capture_output`
           context has exited, or the call will block.
        """
        with self._lock:
            return self._stderr


@contextmanager
def _capture_via_memory() -> ContextManager[OutputCaptureResult]:
    """
    Capture output using in-memory buffers.

    This internal context manager redirects ``sys.stdout`` and ``sys.stderr``
    to :class:`io.StringIO` buffers, then stores their contents in an
    :class:`OutputCaptureResult` instance.

    :return: A context manager yielding an :class:`OutputCaptureResult` object.
    :rtype: ContextManager[OutputCaptureResult]

    .. note::
       :class:`io.StringIO` does not implement ``fileno()``, which may break
       compatibility with APIs that require a real file descriptor.
    """
    with io.StringIO() as sout, io.StringIO() as serr:
        r = OutputCaptureResult()
        try:
            with redirect_stdout(sout), redirect_stderr(serr):
                yield r
        finally:
            r.put_result(
                sout.getvalue(),
                serr.getvalue(),
            )


@contextmanager
def _capture_via_tempfile() -> ContextManager[OutputCaptureResult]:
    """
    Capture output using temporary files.

    This internal context manager redirects ``sys.stdout`` and ``sys.stderr``
    to temporary files, then reads their contents into an
    :class:`OutputCaptureResult` instance.

    :return: A context manager yielding an :class:`OutputCaptureResult` object.
    :rtype: ContextManager[OutputCaptureResult]

    .. note::
       Temporary files provide a ``fileno()``, which improves compatibility
       with operations like :func:`subprocess.run`.
    """
    with TemporaryDirectory() as tdir:
        stdout_file = os.path.join(tdir, 'stdout')
        stderr_file = os.path.join(tdir, 'stderr')
        with open(stdout_file, 'w+', encoding='utf-8') as f_stdout, \
                open(stderr_file, 'w+', encoding='utf-8') as f_stderr:
            r = OutputCaptureResult()
            try:
                with redirect_stdout(f_stdout), redirect_stderr(f_stderr):
                    yield r
            finally:
                if not f_stdout.closed:
                    f_stdout.close()
                if not f_stderr.closed:
                    f_stderr.close()
                try:
                    r.put_result(
                        pathlib.Path(stdout_file).read_text(encoding='utf-8'),
                        pathlib.Path(stderr_file).read_text(encoding='utf-8'),
                    )
                except:  # process for extreme cases to avoid lock stuck
                    r.put_result(None, None)
                    raise


@contextmanager
def capture_output(mem: bool = False) -> ContextManager[OutputCaptureResult]:
    """
    Capture output to ``sys.stdout`` and ``sys.stderr`` within a ``with`` block.

    When ``mem`` is ``False`` (default), output is captured to temporary files.
    When ``mem`` is ``True``, output is captured using in-memory
    :class:`io.StringIO` buffers.

    :param mem: Whether to capture output in memory, defaults to ``False``.
    :type mem: bool
    :return: A context manager yielding an :class:`OutputCaptureResult`.
    :rtype: ContextManager[OutputCaptureResult]

    Examples::
        >>> from hbutils.testing import capture_output
        >>> import sys
        >>>
        >>> with capture_output() as r:
        ...     print('this is stdout')
        ...     print('this is stderr', file=sys.stderr)
        ...
        >>> r.stdout
        'this is stdout\\n'
        >>> r.stderr
        'this is stderr\\n'

    .. note::
       When ``mem`` is set to ``True``, :class:`io.StringIO` is used, which does
       not provide ``fileno()``. Use ``mem=False`` for compatibility with
       subprocess-related operations.
    """
    mock_func = _capture_via_memory if mem else _capture_via_tempfile
    with mock_func() as co:
        yield co


@contextmanager
def disable_output(encoding: str = 'utf-8') -> ContextManager[None]:
    """
    Disable all output to ``sys.stdout`` and ``sys.stderr`` within a ``with`` block.

    All output during the block is redirected to the system's null device
    (e.g., ``/dev/null`` on Unix-like systems or ``NUL`` on Windows).

    :param encoding: Encoding used for the null device, defaults to ``'utf-8'``.
    :type encoding: str
    :return: A context manager that suppresses all output.
    :rtype: ContextManager[None]

    Examples::
        >>> import sys
        >>> from hbutils.testing import disable_output
        >>>
        >>> with disable_output():
        ...     print('this is stdout')
        ...     print('this is stderr', file=sys.stderr)
    """
    with open(os.devnull, 'w', encoding=encoding) as sout:
        with redirect_stdout(sout), redirect_stderr(sout):
            yield
