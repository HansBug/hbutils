"""
Binary and text file detection utilities.

This module provides a lightweight heuristic for determining whether a file
should be treated as binary or text. It samples the initial portion of a file
and checks for the presence of non-text byte values. The main public helpers
are :func:`is_binary_file` and :func:`is_text_file`.

The module contains the following main components:

* :func:`is_binary_file` - Determine whether a file is binary
* :func:`is_text_file` - Determine whether a file is text

.. note::
   Empty files are treated as text files by both public helpers.

Example::

    >>> from hbutils.system.filesystem.binary import is_binary_file, is_text_file
    >>> is_binary_file('README.md')
    False
    >>> is_text_file('README.md')
    True
"""
from typing import Union, AnyStr, Optional, Any, ByteString, IO, Iterable, Callable, Dict, List, Tuple, Set, Mapping, Sequence, MutableMapping, MutableSequence, MutableSet, cast, overload, TYPE_CHECKING
import os

__all__ = [
    'is_binary_file', 'is_text_file',
]

_TEXT_CHARS = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})


def _is_binary_string(data: bytes) -> bool:
    """
    Check if the given byte data contains binary characters.

    :param data: The byte data to check.
    :type data: bytes
    :return: True if the data contains binary characters, False otherwise.
    :rtype: bool
    """
    return bool(data.translate(None, _TEXT_CHARS))


def _take_sample(filename: Union[str, os.PathLike], size: int = 1024) -> bytes:
    """
    Read a sample of bytes from the beginning of a file.

    :param filename: The path to the file to sample.
    :type filename: str or os.PathLike
    :param size: The number of bytes to read from the file. Defaults to 1024.
    :type size: int
    :return: The sampled bytes from the file.
    :rtype: bytes
    """
    with open(filename, 'rb') as f:
        return f.read(size)


def is_binary_file(filename: Union[str, os.PathLike]) -> bool:
    """
    Check if the given file is a binary file.

    This function reads a sample from the beginning of the file and checks
    if it contains binary characters. Files are considered binary if they
    contain characters outside the standard text character set.

    :param filename: The path to the file to check.
    :type filename: str or os.PathLike
    :return: True if the file is binary, False otherwise.
    :rtype: bool

    Examples::

        >>> from hbutils.system import is_binary_file
        >>> is_binary_file('rar_template-simple.rar')
        True
        >>> is_binary_file('README.md')
        False

    .. note::
        Empty files will be treated as text files.
    """
    return _is_binary_string(_take_sample(filename))


def is_text_file(filename: Union[str, os.PathLike]) -> bool:
    """
    Check if the given file is a text file.

    This function reads a sample from the beginning of the file and checks
    if it contains only text characters. Files are considered text if they
    do not contain binary characters.

    :param filename: The path to the file to check.
    :type filename: str or os.PathLike
    :return: True if the file is text, False otherwise.
    :rtype: bool

    Examples::

        >>> from hbutils.system import is_text_file
        >>> is_text_file('rar_template-simple.rar')
        False
        >>> is_text_file('README.md')
        True

    .. note::
        Empty files will be treated as text files.
    """
    return not _is_binary_string(_take_sample(filename))
