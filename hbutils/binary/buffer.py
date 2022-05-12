from typing import BinaryIO, Union

from .base import CIOType

__all__ = [
    'CBufferType',
    'c_buffer',
]


class CBufferType(CIOType):
    def __init__(self, size):
        self.__size = size

    @property
    def size(self):
        return self.__size

    def read(self, file: BinaryIO) -> bytes:
        return file.read(self.__size)

    def write(self, file: BinaryIO, val: Union[bytearray, bytes]):
        if not isinstance(val, (bytearray, bytes)):
            raise TypeError(f'Bytearray or bytes expected, but {repr(val)}.')
        if not (0 <= len(val) <= self.__size):
            raise ValueError(f'Size is expected to be no more than {self.__size}, but actual length is {len(val)}.')

        fval = val[:self.__size]
        fval = fval + b'\x00' * (self.__size - len(fval))
        file.write(fval)


def c_buffer(size: int) -> CBufferType:
    return CBufferType(size)
