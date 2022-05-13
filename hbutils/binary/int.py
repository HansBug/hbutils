import ctypes
from typing import Dict, BinaryIO, List

from .base import CRangedIntType
from .uint import CUnsignedIntType

__all__ = [
    'CSignedIntType',
    'c_int8', 'c_int16', 'c_int32', 'c_int64',
    'c_byte', 'c_short', 'c_int', 'c_long', 'c_longlong',
]


class CSignedIntType(CRangedIntType):
    """
    Overview:
        Signed int type.
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CSignedIntType`.

        :param size: Size of the type.
        """
        self.__size = size
        self._unit = CUnsignedIntType(size)
        self.__half = 1 << (8 * self.__size - 1)
        CRangedIntType.__init__(
            self, self.__size,
            self._unit.minimum - self.__half,
            self._unit.maximum - self.__half
        )

    def read(self, file: BinaryIO) -> int:
        """
        Read signed int value.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :return: Signed int value.
        """
        uval = self._unit.read(file)
        if uval < self.__half:
            return uval
        else:
            return uval - (self.__half << 1)

    def write(self, file: BinaryIO, val: int):
        """
        Write signed int value to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :param val: Signed int value to write.
        """
        if not isinstance(val, int):
            raise TypeError(f'Int value expected, but {repr(val)} found.')
        elif not (self.minimum <= val <= self.maximum):
            raise ValueError(f'Signed int value within '
                             f'[{self.minimum}, {self.maximum}] expected, but {repr(val)} found.')

        fval = val if val >= 0 else val + (self.__half << 1)
        self._unit.write(file, fval)


c_int8 = CSignedIntType(ctypes.sizeof(ctypes.c_int8))
"""
Overview:
    Reading and writing signed integer with 8-bits.
    
Examples::
    >>> import io
    >>> from hbutils.binary import c_int8
    >>> 
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef') as file:
    ...     print(c_int8.read(file))
    ...     print(c_int8.read(file))
    ...     print(c_int8.read(file))
    ...     print(c_int8.read(file))
    -34
    -83
    -66
    -17
    >>> with io.BytesIO() as file:
    ...     c_int8.write(file, -34)
    ...     c_int8.write(file, -83)
    ...     c_int8.write(file, -66)
    ...     c_int8.write(file, -17)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef'
"""
c_int16 = CSignedIntType(ctypes.sizeof(ctypes.c_int16))
"""
Overview:
    Reading and writing signed integer with 16-bits.
    
Examples::
    >>> import io
    >>> from hbutils.binary import c_int16
    >>> 
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef\\x12\\x34\\x56\\xf7') as file:
    ...     print(c_int16.read(file))
    ...     print(c_int16.read(file))
    ...     print(c_int16.read(file))
    ...     print(c_int16.read(file))
    -21026
    -4162
    13330
    -2218
    >>> with io.BytesIO() as file:
    ...     c_int16.write(file, -21026)
    ...     c_int16.write(file, -4162)
    ...     c_int16.write(file, 13330)
    ...     c_int16.write(file, -2218)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef\\x124V\\xf7'
"""
c_int32 = CSignedIntType(ctypes.sizeof(ctypes.c_int32))
"""
Overview:
    Reading and writing signed integer with 32-bits.
    
Examples::
    >>> import io
    >>> from hbutils.binary import c_int32
    >>> 
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef\\x12\\x34\\x56\\xf7') as file:
    ...     print(c_int32.read(file))
    ...     print(c_int32.read(file))
    -272716322
    -145345518
    >>> with io.BytesIO() as file:
    ...     c_int32.write(file, -272716322)
    ...     c_int32.write(file, -145345518)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef\\x124V\\xf7'
"""
c_int64 = CSignedIntType(ctypes.sizeof(ctypes.c_int64))
"""
Overview:
    Reading and writing signed integer with 64-bits.
    
Examples::
    >>> import io
    >>> from hbutils.binary import c_int64
    >>> 
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef\\x12\\x34\\x56\\xf7') as file:
    ...     print(c_int64.read(file))
    -624254242407928354
    >>> with io.BytesIO() as file:
    ...     c_int64.write(file, -624254242407928354)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef\\x124V\\xf7'
"""

_EXIST_TYPES: List[CSignedIntType] = [
    c_int8,
    c_int16,
    c_int32,
    c_int64,
]
_SIZE_TO_INT_TYPE: Dict[int, CSignedIntType] = {
    item.size: item
    for item in _EXIST_TYPES
}


def _get_from_raw(tp) -> CSignedIntType:
    return _SIZE_TO_INT_TYPE[ctypes.sizeof(tp)]


c_byte = _get_from_raw(ctypes.c_byte)
"""
Alias for :data:`c_uint8`.
"""
c_short = _get_from_raw(ctypes.c_short)
"""
Alias for :data:`c_int16`.
"""
c_int = _get_from_raw(ctypes.c_int)
"""
Alias for :data:`c_int32` (in 64-bits OS).

.. note::
    Size of :data:`c_int` is the same as that in C language, which mainly depends on CPU and OS.
"""
c_long = _get_from_raw(ctypes.c_long)
"""
Alias for :data:`c_int64` (in 64-bits OS).

.. note::
    Size of :data:`c_long` is the same as that in C language, which mainly depends on CPU and OS.
"""
c_longlong = _get_from_raw(ctypes.c_longlong)
"""
Alias for :data:`c_int64` (in 64-bits OS).

.. note::
    Size of :data:`c_longlong` is the same as that in C language, which mainly depends on CPU and OS.
"""
