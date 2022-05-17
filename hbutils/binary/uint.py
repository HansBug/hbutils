import ctypes
from typing import Dict, BinaryIO, List

from .base import CRangedIntType

__all__ = [
    'CUnsignedIntType',
    'c_uint8', 'c_uint16', 'c_uint32', 'c_uint64',
    'c_ubyte', 'c_ushort', 'c_uint', 'c_ulong', 'c_ulonglong',
]


class CUnsignedIntType(CRangedIntType):
    """
    Overview:
        Unsigned int type.
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CUnsignedIntType`.

        :param size: Size of the type.
        """
        self.__size = size
        CRangedIntType.__init__(
            self, self.__size,
            0, (1 << (8 * self.__size)) - 1,
        )

    def read(self, file: BinaryIO) -> int:
        """
        Read unsigned int value.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :return: Unsigned int value.
        """
        result = 0
        for i, byte_ in enumerate(file.read(self.__size)):
            result |= byte_ << (8 * i)
        return result

    def write(self, file: BinaryIO, val: int):
        """
        Write unsigned int value to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :param val: Unsigned int value to write.
        """
        if not isinstance(val, int):
            raise TypeError(f'Int value expected, but {repr(val)} found.')
        elif not (self.minimum <= val <= self.maximum):
            raise ValueError(f'Signed int value within '
                             f'[{self.minimum}, {self.maximum}] expected, but {repr(val)} found.')

        _bytes = []
        for _ in range(self.__size):
            _bytes.append(val & 0xff)
            val >>= 8

        file.write(bytes(_bytes))


c_uint8 = CUnsignedIntType(ctypes.sizeof(ctypes.c_uint8))
"""
Overview:
    Reading and writing unsigned integer with 8-bits.
    
Examples::
    >>> import io
    >>> from hbutils.binary import c_uint8
    >>> 
    >>> with io.BytesIO(b'\xde\xad\xbe\xef') as file:
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
    b'\xde\xad\xbe\xef'
"""
c_uint16 = CUnsignedIntType(ctypes.sizeof(ctypes.c_uint16))
"""
Overview:
    Reading and writing unsigned integer with 16-bits.
    
Examples::
    >>> import io
    >>> from hbutils.binary import c_uint16
    >>> 
    >>> with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
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
    b'\xde\xad\xbe\xef\x124Vx'
"""
c_uint32 = CUnsignedIntType(ctypes.sizeof(ctypes.c_uint32))
"""
Overview:
    Reading and writing unsigned integer with 32-bits.
    
Examples::
    >>> import io
    >>> from hbutils.binary import c_uint32
    >>> 
    >>> with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
    ...     print(c_uint32.read(file))
    ...     print(c_uint32.read(file))
    4022250974
    2018915346
    >>> with io.BytesIO() as file:
    ...     c_uint32.write(file, 4022250974)
    ...     c_uint32.write(file, 2018915346)
    ...     print(file.getvalue())
    b'\xde\xad\xbe\xef\x124Vx'
"""
c_uint64 = CUnsignedIntType(ctypes.sizeof(ctypes.c_uint64))
"""
Overview:
    Reading and writing unsigned integer with 64-bits.
    
Examples::
    >>> import io
    >>> from hbutils.binary import c_uint64
    >>> 
    >>> with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
    ...     print(c_uint64.read(file))
    8671175388484775390
    >>> with io.BytesIO() as file:
    ...     c_uint64.write(file, 0x78563412efbeadde)
    ...     print(file.getvalue())
    b'\xde\xad\xbe\xef\x124Vx'
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


def _get_from_raw(tp) -> CUnsignedIntType:
    return _SIZE_TO_INT_TYPE[ctypes.sizeof(tp)]


c_ubyte = _get_from_raw(ctypes.c_ubyte)
"""
Alias for :data:`c_uint8`.
"""
c_ushort = _get_from_raw(ctypes.c_ushort)
"""
Alias for :data:`c_uint16`.
"""
c_uint = _get_from_raw(ctypes.c_uint)
"""
Alias for :data:`c_uint32` (in 64-bits OS).

.. note::
    Size of :data:`c_uint` is the same as that in C language, which mainly depends on CPU and OS.
"""
c_ulong = _get_from_raw(ctypes.c_ulong)
"""
Alias for :data:`c_uint64` (in 64-bits OS).

.. note::
    Size of :data:`c_ulong` is the same as that in C language, which mainly depends on CPU and OS.
"""
c_ulonglong = _get_from_raw(ctypes.c_ulonglong)
"""
Alias for :data:`c_uint64` (in 64-bits OS).

.. note::
    Size of :data:`c_ulonglong` is the same as that in C language, which mainly depends on CPU and OS.
"""
