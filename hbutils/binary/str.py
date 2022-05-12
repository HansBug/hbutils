from typing import BinaryIO, Optional

from .base import CIOType
from ..encoding import auto_decode

__all__ = [
    'CStringType',
    'c_str',
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
