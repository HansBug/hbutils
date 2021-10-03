"""
Overview:
    Useful functions to deal with exception or backtrace objects.
"""
import io
import traceback

__all__ = [
    'print_traceback',
    'str_traceback',
]


def print_traceback(err: BaseException, file=None):
    """
    Overview:
        Print full backtrace for exception object.
    Arguments:
        - err (:obj:`BaseException`): Exception object.
        - file: Output file, default is ``None`` which means stdout.

    Examples::
        See :func:`str_traceback` for actual print content.
    """
    traceback.print_exception(type(err), err, err.__traceback__, file=file)


def str_traceback(err: BaseException) -> str:
    """
    Overview:
        Get full backtrace for exception object.
    Arguments:
        - err (:obj:`BaseException`): Exception object.
    Returns:
        - backtrace (:obj:`str`): Full string backtrace.

    Examples:
        >>> try:
        >>>     raise RuntimeError('runtime error')
        >>> except RuntimeError as e:
        >>>     s = str_traceback(e)

        >>> s
        Traceback (most recent call last):
          File "<stdin>", line 2, in <module>
            raise RuntimeError('runtime error')
        RuntimeError: runtime error
    """
    with io.StringIO() as fs:
        print_traceback(err, file=fs)
        return fs.getvalue()
