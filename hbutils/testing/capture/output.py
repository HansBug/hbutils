"""
Overview:
    Capture for outputs.
"""
import io
from contextlib import redirect_stdout, redirect_stderr, contextmanager
from threading import Lock
from typing import ContextManager


class OutputCaptureResult:
    def __init__(self):
        self._stdout = None
        self._stderr = None
        self._lock = Lock()
        self._lock.acquire()

    def put_result(self, stdout, stderr):
        self._stdout, self._stderr = stdout, stderr
        self._lock.release()

    @property
    def stdout(self):
        with self._lock:
            return self._stdout

    @property
    def stderr(self):
        with self._lock:
            return self._stderr


@contextmanager
def capture_output() -> ContextManager[OutputCaptureResult]:
    """
    Overview:
        Capture all the output to ``sys.stdout`` and ``sys.stderr`` in this ``with`` block.

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
