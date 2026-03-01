"""
C-style string types for binary I/O operations.

This module provides implementations of C-style string handling for binary
streams, including null-terminated strings (``char *`` / ``char[]`` with a
terminator) and fixed-size buffers (``char s[size]``). The types are designed
to operate on binary file objects such as :class:`io.BytesIO` and other
:class:`typing.BinaryIO`-compatible streams.

The module contains the following public components:

* :class:`CStringType` - Null-terminated string type (terminated by ``\\x00``).
* :class:`CSizedStringType` - Fixed-size string type with a specified buffer size.
* :data:`c_str` - Default :class:`CStringType` instance for convenient use.
* :func:`c_sized_str` - Factory function for creating sized-string types.

Example::

    >>> import io
    >>> from hbutils.binary import c_str, c_sized_str
    >>>
    >>> with io.BytesIO(b'hello\\x00world\\x00') as file:
    ...     print(c_str.read(file))
    ...     print(c_str.read(file))
    hello
    world
    >>> with io.BytesIO() as file:
    ...     c_sized_str(8).write(file, "hi")
    ...     print(file.getvalue())
    b'hi\\x00\\x00\\x00\\x00\\x00\\x00'

.. note::
   The :class:`CSizedStringType` decoder currently uses automatic encoding
   detection during reads, regardless of the instance's ``encoding`` attribute.
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


def _auto_encode(s: str, encoding: Optional[str]) -> bytes:
    """
    Encode a string to bytes using the specified encoding or UTF-8 as default.

    :param s: The string to encode.
    :type s: str
    :param encoding: The encoding to use, or ``None`` for UTF-8 default.
    :type encoding: Optional[str]
    :return: The encoded bytes.
    :rtype: bytes
    """
    return s.encode(encoding if encoding is not None else 'utf-8')


class CStringType(CIOType):
    """
    Simple null-terminated string type.

    This class represents C-style strings that end with a single ``\\x00`` byte,
    which is the standard string format in the C language.

    :param encoding: Encoding type, default is ``None`` which enables
        auto-detection during decoding and UTF-8 during encoding.
    :type encoding: Optional[str]

    :ivar encoding: Encoding type configured for the instance.
    :vartype encoding: Optional[str]
    """

    def __init__(self, encoding: Optional[str] = None):
        """
        Constructor of :class:`CStringType`.

        :param encoding: Encoding type, default is ``None`` which means
            auto-detect the encodings.
        :type encoding: Optional[str]
        """
        self.__encoding = encoding

    @property
    def encoding(self) -> Optional[str]:
        """
        Get the encoding type used for string conversion.

        :return: The encoding type, or ``None`` for auto-detection.
        :rtype: Optional[str]
        """
        return self.__encoding

    def read(self, file: BinaryIO) -> str:
        """
        Read a null-terminated string value from a binary file.

        Reads bytes from the file until a null byte (``\\x00``) is encountered,
        then decodes the bytes to a string using the specified or auto-detected
        encoding.

        :param file: Binary file object to read from; ``io.BytesIO`` is supported.
        :type file: BinaryIO
        :return: The decoded string value (without the null terminator).
        :rtype: str
        :raises IndexError: If EOF is reached before a null terminator is found.
        """
        b = bytearray()
        while True:
            bt = file.read(1)[0]
            if bt:
                b.append(bt)
            else:
                break

        return auto_decode(bytes(b), self.__encoding)

    def write(self, file: BinaryIO, val: str) -> None:
        """
        Write a null-terminated string value to a binary IO object.

        Encodes the string using the specified or default encoding and appends
        a null byte (``\\x00``) at the end.

        :param file: Binary file object to write to; ``io.BytesIO`` is supported.
        :type file: BinaryIO
        :param val: String value to write.
        :type val: str
        :raises TypeError: If ``val`` is not a string.

        Example::

            >>> import io
            >>> from hbutils.binary import c_str
            >>> with io.BytesIO() as file:
            ...     c_str.write(file, "hello")
            ...     print(file.getvalue())
            b'hello\\x00'
        """
        if not isinstance(val, str):
            raise TypeError(f'String value expected, but {repr(val)} found.')

        file.write(_auto_encode(val, self.__encoding) + b'\x00')


c_str = CStringType()
"""
Default instance for reading and writing null-terminated strings.

This instance provides convenient access to :class:`CStringType` functionality
with the default encoding (auto-detection).

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
    ``char s[size]`` in the C language. The string occupies a fixed amount of
    space regardless of its actual content length.

    :param size: Size of the string's buffer space in bytes.
    :type size: int
    :param encoding: Encoding type, default is ``None`` which means
        auto-detect the encodings during decoding and UTF-8 during encoding.
    :type encoding: Optional[str]

    :ivar encoding: Encoding type configured for the instance.
    :vartype encoding: Optional[str]
    :ivar size: Size of the fixed buffer in bytes.
    :vartype size: int
    """

    def __init__(self, size: int, encoding: Optional[str] = None):
        """
        Constructor of :class:`CSizedStringType`.

        :param size: Size of the string's buffer space in bytes.
        :type size: int
        :param encoding: Encoding type, default is ``None`` which means
            auto-detect the encodings.
        :type encoding: Optional[str]
        """
        CFixedType.__init__(self, size)
        self.__encoding = encoding
        self._buffer = c_buffer(size)

    @property
    def encoding(self) -> Optional[str]:
        """
        Get the encoding type used for string conversion.

        :return: The encoding type, or ``None`` for auto-detection.
        :rtype: Optional[str]
        """
        return self.__encoding

    def read(self, file: BinaryIO) -> str:
        """
        Read a fixed-size string value from a binary file.

        Reads exactly the specified number of bytes from the file, then decodes
        them as a null-terminated string using auto-detected encoding. The
        current implementation uses :data:`c_str` internally, so any ``encoding``
        configured on this instance is not applied during reads.

        :param file: Binary file object to read from; ``io.BytesIO`` is supported.
        :type file: BinaryIO
        :return: The decoded string value (without padding or null terminator).
        :rtype: str
        """
        bytes_ = self._buffer.read(file)
        with io.BytesIO(bytes_ + b'\x00') as bf:
            return c_str.read(bf)

    def write(self, file: BinaryIO, val: str) -> None:
        """
        Write a fixed-size string value to a binary IO object.

        Encodes the string and writes it to the file, padding with null bytes
        if necessary to fill the fixed-size buffer.

        :param file: Binary file object to write to; ``io.BytesIO`` is supported.
        :type file: BinaryIO
        :param val: String value to write.
        :type val: str
        :raises TypeError: If ``val`` is not a string.
        """
        if not isinstance(val, str):
            raise TypeError(f'String value expected, but {repr(val)} found.')

        self._buffer.write(file, _auto_encode(val, self.__encoding))


def c_sized_str(size: int) -> CSizedStringType:
    """
    Factory function to create a fixed-size string type.

    Creates a :class:`CSizedStringType` instance that reads and writes strings
    occupying a fixed amount of space, similar to C ``char`` arrays.

    :param size: Size of the string's buffer space in bytes.
    :type size: int
    :return: A :class:`CSizedStringType` instance with the specified size.
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
