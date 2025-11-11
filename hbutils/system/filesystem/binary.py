"""
Overview:
    This module provides functions to check if a file is binary or text.
    It uses a heuristic approach by sampling the first portion of the file
    and checking for the presence of binary characters.
"""
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


def _take_sample(filename, size: int = 1024) -> bytes:
    """
    Read a sample of bytes from the beginning of a file.

    :param filename: The path to the file to sample.
    :type filename: str
    :param size: The number of bytes to read from the file. Defaults to 1024.
    :type size: int

    :return: The sampled bytes from the file.
    :rtype: bytes
    """
    with open(filename, 'rb') as f:
        return f.read(size)


def is_binary_file(filename) -> bool:
    """
    Check if the given file is a binary file.

    This function reads a sample from the beginning of the file and checks
    if it contains binary characters. Files are considered binary if they
    contain characters outside the standard text character set.

    :param filename: The path to the file to check.
    :type filename: str

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


def is_text_file(filename) -> bool:
    """
    Check if the given file is a text file.

    This function reads a sample from the beginning of the file and checks
    if it contains only text characters. Files are considered text if they
    do not contain binary characters.

    :param filename: The path to the file to check.
    :type filename: str

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
