"""
Overview:
    Functions to check if a file is binary or text.
"""
__all__ = [
    'is_binary_file', 'is_text_file',
]

_TEXT_CHARS = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})


def _is_binary_string(data: bytes) -> bool:
    return bool(data.translate(None, _TEXT_CHARS))


def _take_sample(filename, size=1024) -> bytes:
    with open(filename, 'rb') as f:
        return f.read(size)


def is_binary_file(filename) -> bool:
    """
    Overview:
        Check if the given file is binary file.

    :param filename: Filename.
    :return: Is binary file or not.

    Examples::
        >>> from hbutils.system import is_binary_file
        >>> is_binary_file('rar_template-simple.rar')
        True
        >>> is_binary_file('README.md')
        False

    .. note::
        Empty file will be seen as text file.
    """
    return _is_binary_string(_take_sample(filename))


def is_text_file(filename) -> bool:
    """
    Overview:
        Check if the given file is text file.

    :param filename: Filename.
    :return: Is text file or not.
    
    Examples::
        >>> from hbutils.system import is_text_file
        >>> is_text_file('rar_template-simple.rar')
        False
        >>> is_text_file('README.md')
        True

    .. note::
        Empty file will be seen as text file.
    """
    return not _is_binary_string(_take_sample(filename))
