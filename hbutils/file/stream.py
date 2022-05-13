"""
Overview:
    Utilities for processing streams.
"""
import io
import os
from contextlib import contextmanager
from typing import Union, TextIO, BinaryIO, ContextManager

__all__ = [
    'keep_cursor', 'getsize', 'is_eof',
]


@contextmanager
def keep_cursor(file: Union[TextIO, BinaryIO]) -> ContextManager:
    """
    Overview:
        Keep the cursor of the given file within a with-block.

    :param file: File which cursor need to be kept.

    Examples::
        >>> import io
        >>> from hbutils.file import keep_cursor
        >>>
        >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef') as file:
        ...     with keep_cursor(file):
        ...         print(file.read(2))
        ...     with keep_cursor(file):  # still from 0
        ...         print(file.read())
        ...
        ...     _ = file.read(2)
        ...     with keep_cursor(file):  # now from 2
        ...         print(file.read(1))
        ...     with keep_cursor(file):  # still from 2
        ...         print(file.read())
        b'\\xde\\xad'
        b'\\xde\\xad\\xbe\\xef'
        b'\\xbe'
        b'\\xbe\\xef'

    .. note::
        Only seekable stream can use :func:`keep_cursor`.
    """
    if file.seekable():
        curpos = file.tell()
        try:
            yield
        finally:
            file.seek(curpos, io.SEEK_SET)
    else:
        raise OSError(f'Given file {repr(file)} is not seekable, '  # pragma: no cover
                      f'so its cursor position cannot be kept.')


def getsize(file: Union[TextIO, BinaryIO]) -> int:
    """
    Overview:
        Get the size of the given ``file`` stream.

    :param file: File which size need to access.
    :return: File's size.

    Examples::
        >>> import io
        >>> from hbutils.file import getsize
        >>>
        >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef') as file:
        ...     print(getsize(file))
        4
        >>> with open('README.md', 'r') as file:
        ...     print(getsize(file))
        2582

    .. note::
        Only seekable stream can use :func:`getsize`.
    """
    if file.seekable():
        try:
            return os.stat(file.fileno()).st_size
        except OSError:
            with keep_cursor(file):
                return file.seek(0, io.SEEK_END)
    else:
        raise OSError(f'Given file {repr(file)} is not seekable, '  # pragma: no cover
                      f'so its size is unavailable.')


def is_eof(file: Union[TextIO, BinaryIO]) -> bool:
    """
    Overview:
        Check if the file meets its end.

    :param file: File to be checked.
    :return: Is EOF(end of file) or not.

    Examples::
        >>> import io
        >>> from hbutils.file import is_eof
        >>>
        >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef') as file:
        ...     print(file.tell(), is_eof(file))
        ...     _ = file.read(2)
        ...     print(file.tell(), is_eof(file))
        ...     _ = file.read(2)
        ...     print(file.tell(), is_eof(file))
        0 False
        2 False
        4 True
        >>> with open('README.md', 'r') as file:
        ...     print(file.tell(), is_eof(file))
        ...     _ = file.read(100)
        ...     print(file.tell(), is_eof(file))
        ...     _ = file.read()
        ...     print(file.tell(), is_eof(file))
        0 False
        100 False
        2582 True

    .. note::
        Only seekable stream can use :func:`is_eof`.
    """
    return file.tell() == getsize(file)
