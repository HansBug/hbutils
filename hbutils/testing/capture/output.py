"""
Overview:
    Capture for outputs.
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

from .._base import TemporaryDirectory


class OutputCaptureResult:
    """
    Overview:
        Result model of output capturing.
    """

    def __init__(self):
        """
        Constructor of :class:`OutputCaptureResult`.
        """
        self._stdout = None
        self._stderr = None
        self._lock = Lock()
        self._lock.acquire()

    def put_result(self, stdout: Optional[str], stderr: Optional[str]):
        """
        Put result inside this model.

        :param stdout: Stdout result.
        :param stderr: Stderr result.
        """
        self._stdout, self._stderr = stdout, stderr
        self._lock.release()

    @property
    def stdout(self) -> Optional[str]:
        """
        Stdout of the output result.

        .. note::
            Do not use this property when :func:`capture_output`'s with block is not quited, \
            or this property will be jammed due to the deadlock inside.
        """
        with self._lock:
            return self._stdout

    @property
    def stderr(self) -> Optional[str]:
        """
        Stderr of the output result.

        .. note::
            Do not use this property when :func:`capture_output`'s with block is not quited, \
            or this property will be jammed due to the deadlock inside.
        """
        with self._lock:
            return self._stderr


@contextmanager
def _capture_via_memory() -> ContextManager[OutputCaptureResult]:
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
    r = OutputCaptureResult()
    with TemporaryDirectory() as tdir:
        stdout_file = os.path.join(tdir, 'stdout')
        stderr_file = os.path.join(tdir, 'stderr')
        try:
            with open(stdout_file, 'w+') as f_stdout, open(stderr_file, 'w+') as f_stderr:
                with redirect_stdout(f_stdout), redirect_stderr(f_stderr):
                    yield r
        finally:
            r.put_result(
                pathlib.Path(stdout_file).read_text(),
                pathlib.Path(stderr_file).read_text(),
            )


@contextmanager
def capture_output(mem: bool = False) -> ContextManager[OutputCaptureResult]:
    """
    Overview:
        Capture all the output to ``sys.stdout`` and ``sys.stderr`` in this ``with`` block.

    :param mem: Use memory to put the result or not. Default is ``False`` \
        which means the output will be redirected to temporary files.

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
        When ``mem`` is set to ``True``, :class:`io.StringIO` is used, which do not have ``fileno`` \
            method. This may cause some problems in some cases (such as :func:`subprocess.run`).

    """
    mock_func = _capture_via_memory if mem else _capture_via_tempfile
    with mock_func() as co:
        yield co


@contextmanager
def disable_output() -> ContextManager[OutputCaptureResult]:
    """
    Overview:
        Disable all the output to ``sys.stdout`` and ``sys.stderr`` in this ``with`` block.

    Examples::
        >>> import sys
        >>> from hbutils.testing import disable_output
        >>>
        >>> with disable_output():  # no output will be shown
        ...     print('this is stdout')
        ...     print('this is stderr', file=sys.stderr)
    """
    with open(os.devnull, 'w') as sout:
        with redirect_stdout(sout), redirect_stderr(sout):
            yield
