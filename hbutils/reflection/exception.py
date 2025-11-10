"""
Overview:
    This module provides utility functions for handling exceptions and traceback objects.
    It includes functions to print and retrieve full backtrace information from exception objects,
    which is useful for debugging and error logging purposes.
"""
import io
import traceback

__all__ = [
    'print_traceback',
    'str_traceback',
]


def print_traceback(err: BaseException, file=None):
    """
    Print full backtrace for exception object.

    :param err: Exception object to print traceback for.
    :type err: BaseException
    :param file: Output file stream. If None, defaults to stdout.
    :type file: file-like object, optional

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
        See :func:`str_traceback` for getting traceback as a string instead of printing.
    """
    traceback.print_exception(type(err), err, err.__traceback__, file=file)


def str_traceback(err: BaseException) -> str:
    """
    Get full backtrace for exception object as a string.

    :param err: Exception object to extract traceback from.
    :type err: BaseException

    :return: Full string representation of the backtrace.
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
