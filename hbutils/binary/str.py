import io
from typing import BinaryIO, Optional

from .base import CIOType
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
    def __init__(self, encoding=None):
        self.__encoding = encoding

    @property
    def encoding(self) -> Optional[str]:
        return self.__encoding

    def read(self, file: BinaryIO) -> str:
        b = bytearray()
        while True:
            bt = file.read(1)[0]
            if bt:
                b.append(bt)
            else:
                break

        return auto_decode(bytes(b), self.__encoding)

    def write(self, file: BinaryIO, val: str):
        if not isinstance(val, str):
            raise TypeError(f'String value expected, but {repr(val)} found.')

        file.write(_auto_encode(val, self.__encoding) + b'\x00')


c_str = CStringType()


class CSizedStringType(CIOType):
    def __init__(self, size: int, encoding=None):
        self.__size = size
        self.__encoding = encoding
        self._buffer = c_buffer(size)

    @property
    def encoding(self) -> Optional[str]:
        return self.__encoding

    @property
    def size(self) -> int:
        return self.__size

    def read(self, file: BinaryIO) -> str:
        bytes_ = self._buffer.read(file)
        with io.BytesIO(bytes_ + b'\x00') as bf:
            return c_str.read(bf)

    def write(self, file: BinaryIO, val: str):
        if not isinstance(val, str):
            raise TypeError(f'String value expected, but {repr(val)} found.')

        self._buffer.write(file, _auto_encode(val, self.__encoding))


def c_sized_str(size: int) -> CSizedStringType:
    return CSizedStringType(size)
