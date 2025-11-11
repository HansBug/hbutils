"""
This module provides C-style string types for binary I/O operations.

It includes support for null-terminated strings (like C strings) and fixed-size strings
(like C char arrays). Both types support automatic encoding detection and custom encoding.

Classes:
    - CStringType: Null-terminated string type (ends with \\x00)
    - CSizedStringType: Fixed-size string type with specified buffer length

Functions:
    - c_sized_str: Factory function to create CSizedStringType instances

Module-level instances:
    - c_str: Default CStringType instance for reading/writing null-terminated strings
"""

import io
from typing import BinaryIO, Optional

from .base import CIOType, CFixedType
from .buffer import c_buffer
from ..encoding import auto_decode

__all__ = [
    'CStringType',
    'c_str',
    'CSizedStringType',
    'c_sized_str',
]


def _auto_encode(s: str, encoding) -> bytes:
    """
    Encode a string to bytes using the specified encoding or UTF-8 as default.

    :param s: The string to encode.
    :type s: str
    :param encoding: The encoding to use, or None for UTF-8 default.
    :type encoding: Optional[str]
    :return: The encoded bytes.
    :rtype: bytes
    """
    return s.encode(encoding if encoding is not None else 'utf-8')


class CStringType(CIOType):
    """
    Simple null-terminated string type.

    This class represents C-style strings that end with a single ``\\x00`` byte,
    which is the standard string format in C language.
    """

    def __init__(self, encoding=None):
        """
        Constructor of :class:`CStringType`.

        :param encoding: Encoding type, default is ``None`` which means auto-detect the encodings.
        :type encoding: Optional[str]
        """
        self.__encoding = encoding

    @property
    def encoding(self) -> Optional[str]:
        """
        Get the encoding type used for string conversion.

        :return: The encoding type, or None for auto-detection.
        :rtype: Optional[str]
        """
        return self.__encoding

    def read(self, file: BinaryIO) -> str:
        """
        Read a null-terminated string value from binary file.

        Reads bytes from the file until a null byte (\\x00) is encountered,
        then decodes the bytes to a string using the specified or auto-detected encoding.

        :param file: Binary file object to read from, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: The decoded string value (without the null terminator).
        :rtype: str
        """
        b = bytearray()
        while True:
            bt = file.read(1)[0]
            if bt:
                b.append(bt)
            else:
                break

        return auto_decode(bytes(b), self.__encoding)

    def write(self, file: BinaryIO, val: str):
        """
        Write a null-terminated string value to binary IO object.

        Encodes the string using the specified or default encoding and appends
        a null byte (\\x00) at the end.

        :param file: Binary file object to write to, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: String value to write.
        :type val: str
        :raises TypeError: If val is not a string.
        """
        if not isinstance(val, str):
            raise TypeError(f'String value expected, but {repr(val)} found.')

        file.write(_auto_encode(val, self.__encoding) + b'\x00')


c_str = CStringType()
"""
Default instance for reading and writing null-terminated strings.

This instance provides convenient access to CStringType functionality with
default encoding (auto-detection).

Examples::

    >>> import io
    >>> from hbutils.binary import c_str
    >>> 
    >>> with io.BytesIO(
    ...         b'kdsfjldsjflkdsmgds\\x00'
    ...         b'\\xd0\\x94\\xd0\\xbe\\xd0\\xb1\\xd1\\x80\\xd1\\x8b\\xd0\\xb9 \\xd0'
    ...         b'\\xb2\\xd0\\xb5\\xd1\\x87\\xd0\\xb5\\xd1\\x80\\x00'
    ...         b'\\xa4\\xb3\\xa4\\xf3\\xa4\\xd0\\xa4\\xf3\\xa4\\xcf\\x00'
    ...         b'\\xcd\\xed\\xc9\\xcf\\xba\\xc3\\x00'
    ... ) as file:
    ...     print(c_str.read(file))
    ...     print(c_str.read(file))
    ...     print(c_str.read(file))
    ...     print(c_str.read(file))
    kdsfjldsjflkdsmgds
    Добрый вечер
    こんばんは
    晚上好
    >>> with io.BytesIO() as file:
    ...     c_str.write(file, "kdsfjld")
    ...     c_str.write(file, "Добрый")
    ...     print(file.getvalue())
    b'kdsfjld\\x00\\xd0\\x94\\xd0\\xbe\\xd0\\xb1\\xd1\\x80\\xd1\\x8b\\xd0\\xb9\\x00'
"""


class CSizedStringType(CFixedType):
    """
    Fixed-size string type.

    This class represents C-style fixed-size character arrays, defined like
    ``char s[size]`` in C language. The string occupies a fixed amount of space
    regardless of its actual content length.
    """

    def __init__(self, size: int, encoding=None):
        """
        Constructor of :class:`CSizedStringType`.

        :param size: Size of the string's buffer space in bytes.
        :type size: int
        :param encoding: Encoding type, default is ``None`` which means auto-detect the encodings.
        :type encoding: Optional[str]
        """
        CFixedType.__init__(self, size)
        self.__encoding = encoding
        self._buffer = c_buffer(size)

    @property
    def encoding(self) -> Optional[str]:
        """
        Get the encoding type used for string conversion.

        :return: The encoding type, or None for auto-detection.
        :rtype: Optional[str]
        """
        return self.__encoding

    def read(self, file: BinaryIO) -> str:
        """
        Read a fixed-size string value from binary file.

        Reads exactly the specified number of bytes from the file, then decodes
        them as a null-terminated string using the specified or auto-detected encoding.

        :param file: Binary file object to read from, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: The decoded string value (without padding or null terminator).
        :rtype: str
        """
        bytes_ = self._buffer.read(file)
        with io.BytesIO(bytes_ + b'\x00') as bf:
            return c_str.read(bf)

    def write(self, file: BinaryIO, val: str):
        """
        Write a fixed-size string value to binary IO object.

        Encodes the string and writes it to the file, padding with null bytes
        if necessary to fill the fixed size buffer.

        :param file: Binary file object to write to, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: String value to write.
        :type val: str
        :raises TypeError: If val is not a string.
        """
        if not isinstance(val, str):
            raise TypeError(f'String value expected, but {repr(val)} found.')

        self._buffer.write(file, _auto_encode(val, self.__encoding))


def c_sized_str(size: int) -> CSizedStringType:
    """
    Factory function to create a fixed-size string type.

    Creates a CSizedStringType instance that reads and writes strings occupying
    a fixed amount of space, similar to C char arrays.

    :param size: Size of the string's buffer space in bytes.
    :type size: int
    :return: A CSizedStringType instance with the specified size.
    :rtype: CSizedStringType

    Examples::

        >>> import io
        >>> from hbutils.binary import c_sized_str
        >>> 
        >>> with io.BytesIO(
        ...         b'kdsfjld\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'
        ...         b'\\xd0\\x94\\xd0\\xbe\\xd0\\xb1\\xd1\\x80\\xd1\\x8b\\xd0\\xb9\\x00\\x00\\x00'
        ... ) as file:
        ...     print(c_sized_str(15).read(file))
        ...     print(c_sized_str(15).read(file))
        kdsfjld
        Добрый
        >>> with io.BytesIO() as file:
        ...     c_sized_str(15).write(file, "kdsfjld")
        ...     c_sized_str(15).write(file, "Добрый")
        ...     print(file.getvalue())
        b'kdsfjld\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\xd0\\x94\\xd0\\xbe\\xd0\\xb1\\xd1\\x80\\xd1\\x8b\\xd0\\xb9\\x00\\x00\\x00'
    """
    return CSizedStringType(size)
