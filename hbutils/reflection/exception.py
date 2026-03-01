"""
Exception and traceback utilities for debugging and error reporting.

This module provides lightweight helpers for printing and capturing full
exception tracebacks. It is designed to simplify error logging and diagnostics
by exposing two public utilities:

* :func:`print_traceback` - Print a full traceback for a given exception.
* :func:`str_traceback` - Capture a full traceback as a string.

Example::

    >>> from hbutils.reflection.exception import print_traceback, str_traceback
    >>> try:
    ...     raise RuntimeError("runtime error")
    ... except RuntimeError as e:
    ...     print_traceback(e)
    ...     text = str_traceback(e)
    ...     assert "RuntimeError" in text

"""
import io
import traceback
from typing import Optional, TextIO

__all__ = [
    'print_traceback',
    'str_traceback',
]


def print_traceback(err: BaseException, file: Optional[TextIO] = None) -> None:
    """
    Print the full traceback for an exception object.

    This function delegates to :func:`traceback.print_exception` and prints
    the complete traceback of the provided exception, including chained
    exceptions if present.

    :param err: Exception object to print a traceback for.
    :type err: BaseException
    :param file: Output file-like object. If ``None``, defaults to standard output.
    :type file: typing.TextIO or None, optional
    :return: This function does not return a value.
    :rtype: None

    Example::

        >>> try:
        ...     raise RuntimeError('runtime error')
        ... except RuntimeError as e:
        ...     print_traceback(e)
        Traceback (most recent call last):
          File "<stdin>", line 2, in <module>
            raise RuntimeError('runtime error')
        RuntimeError: runtime error

    .. note::
       See :func:`str_traceback` for capturing the traceback as a string.
    """
    traceback.print_exception(type(err), err, err.__traceback__, file=file)


def str_traceback(err: BaseException) -> str:
    """
    Get the full traceback for an exception object as a string.

    This function captures the output of :func:`print_traceback` into an
    in-memory buffer and returns it as a string.

    :param err: Exception object to extract traceback from.
    :type err: BaseException
    :return: Full string representation of the traceback.
    :rtype: str

    Example::

        >>> try:
        ...     raise RuntimeError('runtime error')
        ... except RuntimeError as e:
        ...     s = str_traceback(e)
        ...     print(s)
        Traceback (most recent call last):
          File "<stdin>", line 2, in <module>
            raise RuntimeError('runtime error')
        RuntimeError: runtime error
    """
    with io.StringIO() as fs:
        print_traceback(err, file=fs)
        return fs.getvalue()
