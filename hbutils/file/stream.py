"""
Stream Utilities for Seekable File Objects.

This module provides helper utilities for managing the state of seekable file
streams, including preserving cursor position, obtaining stream size, and
checking end-of-file conditions. The helpers work for both text and binary
streams that implement the standard Python file API.

The module contains the following public utilities:

* :func:`keep_cursor` - Preserve the current cursor position within a context.
* :func:`getsize` - Retrieve the size of a stream in bytes or characters.
* :func:`is_eof` - Check whether the stream cursor is at the end-of-file.

.. note::
   All functions in this module require seekable file-like objects. Non-seekable
   streams will raise :class:`OSError`.

Example::

    >>> import io
    >>> from hbutils.file.stream import keep_cursor, getsize, is_eof
    >>>
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef') as f:
    ...     print(getsize(f))
    ...     with keep_cursor(f):
    ...         _ = f.read(2)
    ...     print(f.tell(), is_eof(f))
    4
    0 False
"""
import io
import os
from contextlib import contextmanager
from typing import Union, TextIO, BinaryIO, ContextManager

__all__ = [
    'keep_cursor', 'getsize', 'is_eof',
]


@contextmanager
def keep_cursor(file: Union[TextIO, BinaryIO]) -> ContextManager[None]:
    """
    Keep the cursor of the given file within a ``with``-block.

    This context manager saves the current cursor position of a file stream before
    entering the context and restores it when exiting, regardless of any operations
    performed within the context.

    :param file: File whose cursor needs to be preserved.
    :type file: Union[TextIO, BinaryIO]
    :return: A context manager that preserves the file cursor position.
    :rtype: ContextManager[None]
    :raises OSError: If the given file is not seekable.

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
        Only seekable streams can use :func:`keep_cursor`.
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
    Get the size of the given file stream.

    This function attempts to retrieve the file size by first trying to use
    :func:`os.stat` on the file descriptor. If that fails (e.g., for in-memory
    streams), it seeks to the end of the file to determine the size, then
    restores the original cursor position.

    :param file: File whose size needs to be accessed.
    :type file: Union[TextIO, BinaryIO]
    :return: File's size in bytes (for binary files) or characters (for text files).
    :rtype: int
    :raises OSError: If the given file is not seekable.

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
        Only seekable streams can use :func:`getsize`.
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
    Check if the file cursor is at the end of the file.

    This function determines whether the current cursor position is at the end of the
    file by comparing the current position (from :meth:`~io.IOBase.tell`) with the
    total file size (from :func:`getsize`).

    :param file: File to be checked.
    :type file: Union[TextIO, BinaryIO]
    :return: ``True`` if the cursor is at the end of file, ``False`` otherwise.
    :rtype: bool
    :raises OSError: If the given file is not seekable.

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
        Only seekable streams can use :func:`is_eof`.
    """
    return file.tell() == getsize(file)
