"""
This module provides boolean type handling for binary I/O operations in C-style format.

The module implements a CBoolType class that allows reading and writing boolean values
to binary streams using C language conventions. It provides a pre-configured c_bool
instance that matches the size of C's bool type on the current platform.
"""

import ctypes
from typing import BinaryIO

from .base import CFixedType

__all__ = [
    'CBoolType',
    'c_bool',
]


class CBoolType(CFixedType):
    """
    Boolean type for binary I/O operations.
    
    This class provides methods to read and write boolean values in binary format,
    compatible with C language boolean representation.
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CBoolType`.

        :param size: Size of boolean type in bytes.
        :type size: int
        """
        CFixedType.__init__(self, size)
        self.__size = size

    def read(self, file: BinaryIO) -> bool:
        """
        Read boolean value from binary file.

        :param file: Binary file object to read from, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        
        :return: Boolean value read from the file. Returns True if any byte is non-zero.
        :rtype: bool
        
        Example::
            >>> import io
            >>> from hbutils.binary import c_bool
            >>> with io.BytesIO(b'\\x01\\x00') as file:
            ...     print(c_bool.read(file))
            ...     print(c_bool.read(file))
            True
            False
        """
        return any(file.read(self.__size))

    def write(self, file: BinaryIO, val: bool):
        """
        Write boolean value to binary IO object.

        The boolean value is written as a sequence of bytes with the size specified
        during initialization. The value is represented as 0x01 for True and 0x00 for False,
        padded with leading zeros to match the required size.

        :param file: Binary file object to write to, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Boolean value to write.
        :type val: bool
        
        Example::
            >>> import io
            >>> from hbutils.binary import c_bool
            >>> with io.BytesIO() as file:
            ...     c_bool.write(file, True)
            ...     c_bool.write(file, False)
            ...     print(file.getvalue())
            b'\\x01\\x00'
        """
        file.write(b'\x00' * (self.__size - 1) + (b'\x01' if val else b'\x00'))


c_bool = CBoolType(ctypes.sizeof(ctypes.c_bool))
"""
Pre-configured boolean type instance for reading and writing bool values in C language format.

This instance is configured with the size of C's bool type on the current platform,
ensuring compatibility with C binary data structures.

:type: CBoolType

Examples::
    >>> import io
    >>> from hbutils.binary import c_bool
    >>> 
    >>> # Reading boolean values
    >>> with io.BytesIO(b'\\x01\\x00\\x01\\x00') as file:
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    True
    False
    True
    False
    
    >>> # Writing boolean values
    >>> with io.BytesIO() as file:
    ...     c_bool.write(file, True)
    ...     c_bool.write(file, False)
    ...     c_bool.write(file, True)
    ...     c_bool.write(file, False)
    ...     print(file.getvalue())
    ... 
    b'\\x01\\x00\\x01\\x00'
"""
