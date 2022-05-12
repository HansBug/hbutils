import ctypes
from typing import BinaryIO

from .base import CFixedType

__all__ = [
    'CBoolType',
    'c_bool',
]


class CBoolType(CFixedType):
    def __init__(self, size: int):
        self.__size = size

    def _size(self) -> int:
        return self.__size

    def read(self, file: BinaryIO) -> bool:
        return any(file.read(self.__size))

    def write(self, file: BinaryIO, val: bool):
        file.write(b'\x00' * (self.__size - 1) + (b'\x01' if val else b'\x00'))


c_bool = CBoolType(ctypes.sizeof(ctypes.c_bool))
