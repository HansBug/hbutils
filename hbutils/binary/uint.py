"""
Unsigned integer types for binary I/O operations.

This module defines a set of unsigned integer types with fixed sizes
(8, 16, 32, and 64 bits) and provides facilities to read and write these
values to binary streams using little-endian byte order. It also exposes
aliases that mirror common C unsigned integer types through :mod:`ctypes`.

The module contains the following main components:

* :class:`CUnsignedIntType` - Unsigned integer type with fixed size and range
* :data:`c_uint8`, :data:`c_uint16`, :data:`c_uint32`, :data:`c_uint64` - Fixed-size unsigned types
* :data:`c_ubyte`, :data:`c_ushort`, :data:`c_uint`, :data:`c_ulong`, :data:`c_ulonglong` - C aliases

.. note::
   All read/write operations are little-endian. Ensure the file-like object
   is opened in binary mode.

Example::

    >>> import io
    >>> from hbutils.binary import c_uint16
    >>> with io.BytesIO() as file:
    ...     c_uint16.write(file, 65535)
    ...     file.seek(0)
    ...     print(c_uint16.read(file))
    65535

"""

import ctypes
from typing import Dict, BinaryIO, List, Type

from .base import CRangedIntType

__all__ = [
    'CUnsignedIntType',
    'c_uint8', 'c_uint16', 'c_uint32', 'c_uint64',
    'c_ubyte', 'c_ushort', 'c_uint', 'c_ulong', 'c_ulonglong',
]


class CUnsignedIntType(CRangedIntType):
    """
    Unsigned integer type for binary I/O operations.

    This class provides functionality to read and write unsigned integers
    of various sizes to/from binary files using little-endian byte order.

    :param size: Size of the type in bytes.
    :type size: int

    :ivar size: Size of the type in bytes, inherited from :class:`CRangedIntType`.
    :vartype size: int
    :ivar minimum: Minimum representable value (always 0).
    :vartype minimum: int
    :ivar maximum: Maximum representable value for the given size.
    :vartype maximum: int
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CUnsignedIntType`.

        :param size: Size of the type in bytes.
        :type size: int
        """
        self.__size = size
        CRangedIntType.__init__(
            self, self.__size,
            0, (1 << (8 * self.__size)) - 1,
        )

    def read(self, file: BinaryIO) -> int:
        """
        Read unsigned int value from binary file.

        Reads bytes in little-endian order and converts them to an unsigned integer.

        :param file: Binary file object to read from. ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Unsigned int value read from the file.
        :rtype: int

        Example::

            >>> import io
            >>> from hbutils.binary import c_uint8
            >>> with io.BytesIO(b'\\xde\\xad') as file:
            ...     print(c_uint8.read(file))
            222
        """
        result = 0
        for i, byte_ in enumerate(file.read(self.__size)):
            result |= byte_ << (8 * i)
        return result

    def write(self, file: BinaryIO, val: int) -> None:
        """
        Write unsigned int value to binary IO object.

        Writes the integer value as bytes in little-endian order.

        :param file: Binary file object to write to. ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Unsigned int value to write.
        :type val: int
        :return: ``None``.
        :rtype: None
        :raises TypeError: If val is not an integer.
        :raises ValueError: If val is outside the valid range for this type.

        Example::

            >>> import io
            >>> from hbutils.binary import c_uint8
            >>> with io.BytesIO() as file:
            ...     c_uint8.write(file, 222)
            ...     print(file.getvalue())
            b'\\xde'
        """
        if not isinstance(val, int):
            raise TypeError(f'Int value expected, but {repr(val)} found.')
        elif not (self.minimum <= val <= self.maximum):
            raise ValueError(f'Unsigned int value within '
                             f'[{self.minimum}, {self.maximum}] expected, but {repr(val)} found.')

        _bytes = []
        for _ in range(self.__size):
            _bytes.append(val & 0xff)
            val >>= 8

        file.write(bytes(_bytes))


c_uint8 = CUnsignedIntType(ctypes.sizeof(ctypes.c_uint8))
"""
Reading and writing unsigned integer with 8-bits.

This type represents an unsigned 8-bit integer (range: 0 to 255).

Examples::

    >>> import io
    >>> from hbutils.binary import c_uint8
    >>> 
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef') as file:
    ...     print(c_uint8.read(file))
    ...     print(c_uint8.read(file))
    ...     print(c_uint8.read(file))
    ...     print(c_uint8.read(file))
    222
    173
    190
    239
    >>> with io.BytesIO() as file:
    ...     c_uint8.write(file, 222)
    ...     c_uint8.write(file, 173)
    ...     c_uint8.write(file, 190)
    ...     c_uint8.write(file, 239)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef'
"""
c_uint16 = CUnsignedIntType(ctypes.sizeof(ctypes.c_uint16))
"""
Reading and writing unsigned integer with 16-bits.

This type represents an unsigned 16-bit integer (range: 0 to 65535).

Examples::

    >>> import io
    >>> from hbutils.binary import c_uint16
    >>> 
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef\\x12\\x34\\x56\\x78') as file:
    ...     print(c_uint16.read(file))
    ...     print(c_uint16.read(file))
    ...     print(c_uint16.read(file))
    ...     print(c_uint16.read(file))
    44510
    61374
    13330
    30806
    >>> with io.BytesIO() as file:
    ...     c_uint16.write(file, 44510)
    ...     c_uint16.write(file, 61374)
    ...     c_uint16.write(file, 13330)
    ...     c_uint16.write(file, 30806)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef\\x124Vx'
"""
c_uint32 = CUnsignedIntType(ctypes.sizeof(ctypes.c_uint32))
"""
Reading and writing unsigned integer with 32-bits.

This type represents an unsigned 32-bit integer (range: 0 to 4294967295).

Examples::

    >>> import io
    >>> from hbutils.binary import c_uint32
    >>> 
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef\\x12\\x34\\x56\\x78') as file:
    ...     print(c_uint32.read(file))
    ...     print(c_uint32.read(file))
    4022250974
    2018915346
    >>> with io.BytesIO() as file:
    ...     c_uint32.write(file, 4022250974)
    ...     c_uint32.write(file, 2018915346)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef\\x124Vx'
"""
c_uint64 = CUnsignedIntType(ctypes.sizeof(ctypes.c_uint64))
"""
Reading and writing unsigned integer with 64-bits.

This type represents an unsigned 64-bit integer (range: 0 to 18446744073709551615).

Examples::

    >>> import io
    >>> from hbutils.binary import c_uint64
    >>> 
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef\\x12\\x34\\x56\\x78') as file:
    ...     print(c_uint64.read(file))
    8671175388484775390
    >>> with io.BytesIO() as file:
    ...     c_uint64.write(file, 0x78563412efbeadde)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef\\x124Vx'
"""

_EXIST_TYPES: List[CUnsignedIntType] = [
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
]
_SIZE_TO_INT_TYPE: Dict[int, CUnsignedIntType] = {
    item.size: item
    for item in _EXIST_TYPES
}


def _get_from_raw(tp: Type[ctypes._SimpleCData]) -> CUnsignedIntType:
    """
    Get the corresponding CUnsignedIntType for a ctypes type.

    :param tp: A ctypes unsigned integer type.
    :type tp: Type[ctypes._SimpleCData]
    :return: The corresponding :class:`CUnsignedIntType` instance.
    :rtype: CUnsignedIntType
    :raises KeyError: If the given ctypes type size is not supported.
    """
    return _SIZE_TO_INT_TYPE[ctypes.sizeof(tp)]


c_ubyte = _get_from_raw(ctypes.c_ubyte)
"""
Alias for :data:`c_uint8`.

Represents an unsigned byte (8-bit unsigned integer).
"""
c_ushort = _get_from_raw(ctypes.c_ushort)
"""
Alias for :data:`c_uint16`.

Represents an unsigned short integer (16-bit unsigned integer).
"""
c_uint = _get_from_raw(ctypes.c_uint)
"""
Alias for :data:`c_uint32` (in 64-bits OS).

Represents an unsigned int. The actual size depends on the platform.

.. note::
    Size of :data:`c_uint` is the same as that in C language, which mainly depends on CPU and OS.
"""
c_ulong = _get_from_raw(ctypes.c_ulong)
"""
Alias for :data:`c_uint64` (in 64-bits OS).

Represents an unsigned long integer. The actual size depends on the platform.

.. note::
    Size of :data:`c_ulong` is the same as that in C language, which mainly depends on CPU and OS.
"""
c_ulonglong = _get_from_raw(ctypes.c_ulonglong)
"""
Alias for :data:`c_uint64` (in 64-bits OS).

Represents an unsigned long long integer (64-bit unsigned integer).

.. note::
    Size of :data:`c_ulonglong` is the same as that in C language, which mainly depends on CPU and OS.
"""
