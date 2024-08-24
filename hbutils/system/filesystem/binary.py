"""
Overview:
    This module provides functions to check if a file is binary or text.
    It includes utility functions for reading file samples and analyzing their content.
"""

__all__ = [
    'is_binary_file', 'is_text_file',
]

_TEXT_CHARS = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})


def _is_binary_string(data: bytes) -> bool:
    """
    Check if the given bytes data contains non-text characters.

    :param data: The bytes data to check.
    :type data: bytes

    :return: True if the data contains non-text characters, False otherwise.
    :rtype: bool
    """
    return bool(data.translate(None, _TEXT_CHARS))


def _take_sample(filename, size=1024) -> bytes:
    """
    Read a sample of bytes from the given file.

    :param filename: The name of the file to read from.
    :type filename: str
    :param size: The number of bytes to read (default is 1024).
    :type size: int

    :return: A sample of bytes from the file.
    :rtype: bytes
    """
    with open(filename, 'rb') as f:
        return f.read(size)


def is_binary_file(filename) -> bool:
    """
    Check if the given file is a binary file.

    This function reads a sample of the file and analyzes its content
    to determine if it contains non-text characters.

    :param filename: The name of the file to check.
    :type filename: str

    :return: True if the file is binary, False if it's a text file.
    :rtype: bool

    Examples::
        >>> from hbutils.system import is_binary_file
        >>> is_binary_file('rar_template-simple.rar')
        True
        >>> is_binary_file('README.md')
        False

    .. note::
        Empty files are considered text files.
    """
    return _is_binary_string(_take_sample(filename))


def is_text_file(filename) -> bool:
    """
    Check if the given file is a text file.

    This function is the inverse of `is_binary_file`. It reads a sample
    of the file and analyzes its content to determine if it contains
    only text characters.

    :param filename: The name of the file to check.
    :type filename: str

    :return: True if the file is a text file, False if it's binary.
    :rtype: bool

    Examples::
        >>> from hbutils.system import is_text_file
        >>> is_text_file('rar_template-simple.rar')
        False
        >>> is_text_file('README.md')
        True

    .. note::
        Empty files are considered text files.
    """
    return not _is_binary_string(_take_sample(filename))
