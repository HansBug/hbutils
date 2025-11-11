"""
Overview:
    This module provides utilities for capturing and disabling standard output and error streams.
    It includes context managers for redirecting stdout/stderr to either memory buffers or temporary
    files, and for completely disabling output during code execution.
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
    Overview:
        Result model of output capturing. This class stores captured stdout and stderr
        content and provides thread-safe access to the results.
    """

    def __init__(self):
        """
        Constructor of :class:`OutputCaptureResult`.
        
        Initializes the result object with None values for stdout and stderr,
        and creates a lock that is initially acquired to prevent premature access.
        """
        self._stdout = None
        self._stderr = None
        self._lock = Lock()
        self._lock.acquire()

    def put_result(self, stdout: Optional[str], stderr: Optional[str]):
        """
        Put result inside this model.

        :param stdout: Stdout result content.
        :type stdout: Optional[str]
        :param stderr: Stderr result content.
        :type stderr: Optional[str]
        """
        self._stdout, self._stderr = stdout, stderr
        self._lock.release()

    @property
    def stdout(self) -> Optional[str]:
        """
        Stdout of the output result.

        :return: The captured stdout content.
        :rtype: Optional[str]

        .. note::
            Do not use this property when :func:`capture_output`'s with block is not exited,
            or this property will be blocked due to the deadlock inside.
        """
        with self._lock:
            return self._stdout

    @property
    def stderr(self) -> Optional[str]:
        """
        Stderr of the output result.

        :return: The captured stderr content.
        :rtype: Optional[str]

        .. note::
            Do not use this property when :func:`capture_output`'s with block is not exited,
            or this property will be blocked due to the deadlock inside.
        """
        with self._lock:
            return self._stderr


@contextmanager
def _capture_via_memory() -> ContextManager[OutputCaptureResult]:
    """
    Internal context manager that captures output using in-memory StringIO buffers.

    :return: A context manager yielding an OutputCaptureResult object.
    :rtype: ContextManager[OutputCaptureResult]
    
    .. note::
        This method uses StringIO which doesn't have a fileno() method, which may
        cause issues with some operations like subprocess.run.
    """
    r = OutputCaptureResult()
    with io.StringIO() as sout, io.StringIO() as serr:
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
    Internal context manager that captures output using temporary files.

    :return: A context manager yielding an OutputCaptureResult object.
    :rtype: ContextManager[OutputCaptureResult]
    
    .. note::
        This method uses actual files which have fileno() methods, making them
        compatible with operations like subprocess.run.
    """
    r = OutputCaptureResult()
    with TemporaryDirectory() as tdir:
        stdout_file = os.path.join(tdir, 'stdout')
        stderr_file = os.path.join(tdir, 'stderr')
        try:
            with open(stdout_file, 'w+', encoding='utf-8') as f_stdout, \
                    open(stderr_file, 'w+', encoding='utf-8') as f_stderr:
                with redirect_stdout(f_stdout), redirect_stderr(f_stderr):
                    yield r
        finally:
            r.put_result(
                pathlib.Path(stdout_file).read_text(encoding='utf-8'),
                pathlib.Path(stderr_file).read_text(encoding='utf-8'),
            )


@contextmanager
def capture_output(mem: bool = False) -> ContextManager[OutputCaptureResult]:
    """
    Overview:
        Capture all the output to ``sys.stdout`` and ``sys.stderr`` in this ``with`` block.

    :param mem: Use memory to put the result or not. Default is ``False``
        which means the output will be redirected to temporary files.
    :type mem: bool
    :return: A context manager yielding an OutputCaptureResult object containing captured output.
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
        When ``mem`` is set to ``True``, :class:`io.StringIO` is used, which does not have ``fileno``
        method. This may cause some problems in some cases (such as :func:`subprocess.run`).
        Use ``mem=False`` (default) for compatibility with subprocess operations.
    """
    mock_func = _capture_via_memory if mem else _capture_via_tempfile
    with mock_func() as co:
        yield co


@contextmanager
def disable_output(encoding: str = 'utf-8') -> ContextManager[None]:
    """
    Overview:
        Disable all the output to ``sys.stdout`` and ``sys.stderr`` in this ``with`` block.
        All output will be redirected to the system's null device (e.g., /dev/null on Unix).

    :param encoding: Encoding of null file, default is ``utf-8``.
    :type encoding: str
    :return: A context manager that suppresses all stdout and stderr output.
    :rtype: ContextManager[None]

    Examples::
        >>> import sys
        >>> from hbutils.testing import disable_output
        >>>
        >>> with disable_output():  # no output will be shown
        ...     print('this is stdout')
        ...     print('this is stderr', file=sys.stderr)
    """
    with open(os.devnull, 'w', encoding=encoding) as sout:
        with redirect_stdout(sout), redirect_stderr(sout):
            yield
