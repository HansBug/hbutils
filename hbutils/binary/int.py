"""
This module provides signed integer types for binary I/O operations.

It implements various signed integer types (8-bit, 16-bit, 32-bit, 64-bit) that can be used
to read from and write to binary files or streams. The module also provides platform-dependent
type aliases that match C language integer types.

The main class is :class:`CSignedIntType`, which handles the conversion between binary data
and signed integer values. It supports reading and writing signed integers of different sizes
while handling two's complement representation.

Example::
    >>> import io
    >>> from hbutils.binary import c_int32
    >>> 
    >>> # Reading signed integers
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef') as file:
    ...     value = c_int32.read(file)
    ...     print(value)
    -272716322
    
    >>> # Writing signed integers
    >>> with io.BytesIO() as file:
    ...     c_int32.write(file, -272716322)
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef'
"""
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
    Signed integer type for binary I/O operations.
    
    This class provides functionality to read and write signed integers of a specific size
    to and from binary streams. It handles two's complement representation internally by
    using an unsigned integer type for the actual I/O operations.
    
    :param size: Size of the integer type in bytes.
    :type size: int
    
    Example::
        >>> import io
        >>> from hbutils.binary import CSignedIntType
        >>> 
        >>> # Create a 2-byte signed integer type
        >>> int16_type = CSignedIntType(2)
        >>> 
        >>> # Read a signed integer
        >>> with io.BytesIO(b'\\xde\\xad') as file:
        ...     value = int16_type.read(file)
        ...     print(value)
        -21026
        
        >>> # Write a signed integer
        >>> with io.BytesIO() as file:
        ...     int16_type.write(file, -21026)
        ...     print(file.getvalue())
        b'\\xde\\xad'
    """

    def __init__(self, size: int):
        """
        Initialize a signed integer type with the specified size.

        :param size: Size of the integer type in bytes.
        :type size: int
        
        The constructor sets up the internal unsigned integer type for I/O operations
        and calculates the valid range for signed integers of this size.
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
        Read a signed integer value from a binary stream.

        :param file: Binary file or stream to read from. ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: The signed integer value read from the stream.
        :rtype: int
        
        This method reads the unsigned representation and converts it to a signed integer
        using two's complement representation.
        
        Example::
            >>> import io
            >>> from hbutils.binary import c_int16
            >>> 
            >>> with io.BytesIO(b'\\xde\\xad') as file:
            ...     value = c_int16.read(file)
            ...     print(value)
            -21026
        """
        uval = self._unit.read(file)
        if uval < self.__half:
            return uval
        else:
            return uval - (self.__half << 1)

    def write(self, file: BinaryIO, val: int):
        """
        Write a signed integer value to a binary stream.

        :param file: Binary file or stream to write to. ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Signed integer value to write.
        :type val: int
        :raises TypeError: If the value is not an integer.
        :raises ValueError: If the value is outside the valid range for this integer type.
        
        This method converts the signed integer to its unsigned two's complement representation
        before writing to the stream.
        
        Example::
            >>> import io
            >>> from hbutils.binary import c_int16
            >>> 
            >>> with io.BytesIO() as file:
            ...     c_int16.write(file, -21026)
            ...     print(file.getvalue())
            b'\\xde\\xad'
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
Reading and writing signed integer with 8-bits.

This type represents a signed 8-bit integer with a range of -128 to 127.
    
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
Reading and writing signed integer with 16-bits.

This type represents a signed 16-bit integer with a range of -32768 to 32767.
    
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
Reading and writing signed integer with 32-bits.

This type represents a signed 32-bit integer with a range of -2147483648 to 2147483647.
    
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
Reading and writing signed integer with 64-bits.

This type represents a signed 64-bit integer with a range of -9223372036854775808 to 9223372036854775807.
    
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
    """
    Get the corresponding CSignedIntType instance for a ctypes integer type.
    
    :param tp: A ctypes integer type (e.g., ctypes.c_int, ctypes.c_long).
    :return: The corresponding CSignedIntType instance.
    :rtype: CSignedIntType
    
    This internal function maps ctypes integer types to their corresponding
    CSignedIntType instances based on size.
    """
    return _SIZE_TO_INT_TYPE[ctypes.sizeof(tp)]


c_byte = _get_from_raw(ctypes.c_byte)
"""
Alias for :data:`c_int8`.

This type represents a signed byte, equivalent to a signed 8-bit integer.
"""
c_short = _get_from_raw(ctypes.c_short)
"""
Alias for :data:`c_int16`.

This type represents a short integer, equivalent to a signed 16-bit integer.
"""
c_int = _get_from_raw(ctypes.c_int)
"""
Alias for :data:`c_int32` (in 64-bit OS).

.. note::
    Size of :data:`c_int` is the same as that in C language, which mainly depends on CPU and OS.
    On most modern 64-bit systems, this is a 32-bit signed integer.
"""
c_long = _get_from_raw(ctypes.c_long)
"""
Alias for :data:`c_int64` (in 64-bit OS).

.. note::
    Size of :data:`c_long` is the same as that in C language, which mainly depends on CPU and OS.
    On 64-bit Unix-like systems, this is typically a 64-bit signed integer.
    On Windows, it may be 32-bit even on 64-bit systems.
"""
c_longlong = _get_from_raw(ctypes.c_longlong)
"""
Alias for :data:`c_int64` (in 64-bit OS).

.. note::
    Size of :data:`c_longlong` is the same as that in C language, which mainly depends on CPU and OS.
    This is typically a 64-bit signed integer on all modern platforms.
"""
