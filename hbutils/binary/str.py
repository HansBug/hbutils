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
    return s.encode(encoding if encoding is not None else 'utf-8')


class CStringType(CIOType):
    """
    Overview:
        Simple string type.

        It should end with a single ``\\x00``, which is quite common in C language.
    """

    def __init__(self, encoding=None):
        """
        Constructor of :class:`CStringType`.

        :param encoding: Encoding type, default is ``None`` which means auto-detect the encodings.
        """
        self.__encoding = encoding

    @property
    def encoding(self) -> Optional[str]:
        """
        Encoding type.
        """
        return self.__encoding

    def read(self, file: BinaryIO) -> str:
        """
        Read simple string value.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :return: String value.
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
        Write simple string value to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :param val: String to write.
        """
        if not isinstance(val, str):
            raise TypeError(f'String value expected, but {repr(val)} found.')

        file.write(_auto_encode(val, self.__encoding) + b'\x00')


c_str = CStringType()
"""
Overview:
    Reading and writing simple string, ends with a single ``\\x00``.

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
    Overview:
        Sized string type.

        It should have a fixed size, which is defined like ``char s[size]`` in C language.
    """

    def __init__(self, size: int, encoding=None):
        """
        Constructor of :class:`CStringType`.

        :param size: Size of the string's space.
        :param encoding: Encoding type, default is ``None`` which means auto-detect the encodings.
        """
        CFixedType.__init__(self, size)
        self.__encoding = encoding
        self._buffer = c_buffer(size)

    @property
    def encoding(self) -> Optional[str]:
        """
        Encoding type.
        """
        return self.__encoding

    def read(self, file: BinaryIO) -> str:
        """
        Read sized string value.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :return: String value.
        """
        bytes_ = self._buffer.read(file)
        with io.BytesIO(bytes_ + b'\x00') as bf:
            return c_str.read(bf)

    def write(self, file: BinaryIO, val: str):
        """
        Write sized string value to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :param val: String to write.
        """
        if not isinstance(val, str):
            raise TypeError(f'String value expected, but {repr(val)} found.')

        self._buffer.write(file, _auto_encode(val, self.__encoding))


def c_sized_str(size: int) -> CSizedStringType:
    """
    Overview:
        Reading and writing sized string, which occupy a fixed space..

    :param size: Size of the string's space.

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
