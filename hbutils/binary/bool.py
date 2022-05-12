import ctypes
from typing import BinaryIO

from .base import CFixedType

__all__ = [
    'CBoolType',
    'c_bool',
]


class CBoolType(CFixedType):
    """
    Overview:
        Boolean type.
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CBoolType`.

        :param size: Size of boolean type.
        """
        CFixedType.__init__(self, size)
        self.__size = size

    def read(self, file: BinaryIO) -> bool:
        """
        Read boolean value.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :return: Boolean value.
        """
        return any(file.read(self.__size))

    def write(self, file: BinaryIO, val: bool):
        """
        Write boolean value to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :param val: Boolean value to write.
        """
        file.write(b'\x00' * (self.__size - 1) + (b'\x01' if val else b'\x00'))


c_bool = CBoolType(ctypes.sizeof(ctypes.c_bool))
"""
Overview:
    Reading and writing bool value like C language.

Examples::
    >>> import io
    >>> from hbutils.binary import c_bool
    >>> 
    >>> with io.BytesIO(b'\\x01\\x00\\x01\\x00') as file:
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    True
    False
    True
    False
    >>> with io.BytesIO() as file:
    ...     c_bool.write(file, True)
    ...     c_bool.write(file, False)
    ...     c_bool.write(file, True)
    ...     c_bool.write(file, False)
    ...     print(file.getvalue())
    ... 
    b'\\x01\\x00\\x01\\x00'
"""
