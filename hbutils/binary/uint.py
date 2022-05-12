import ctypes
from typing import Dict, BinaryIO, List

from .base import CRangedIntType

__all__ = [
    'CUnsignedIntType',
    'c_uint8', 'c_uint16', 'c_uint32', 'c_uint64',
    'c_byte', 'c_ushort', 'c_uint', 'c_ulong', 'c_ulonglong',
]


class CUnsignedIntType(CRangedIntType):
    _BYTE = 1 << 8

    def __init__(self, byte_count: int):
        self.__byte_count = byte_count
        CRangedIntType.__init__(
            self, self.__byte_count,
            0, (1 << (8 * self.__byte_count)) - 1,
        )

    def read(self, file: BinaryIO) -> int:
        result = 0
        for i, byte_ in enumerate(file.read(self.__byte_count)):
            result |= byte_ << (8 * i)
        return result

    def write(self, file: BinaryIO, val: int):
        if not isinstance(val, int):
            raise TypeError(f'Int value expected, but {repr(val)} found.')
        elif not (self.minimum <= val <= self.maximum):
            raise ValueError(f'Signed int value within '
                             f'[{self.minimum}, {self.maximum}] expected, but {repr(val)} found.')

        _bytes = []
        for _ in range(self.__byte_count):
            _bytes.append(val & (self._BYTE - 1))
            val >>= 8

        file.write(bytes(_bytes))


c_uint8 = CUnsignedIntType(1)
c_uint16 = CUnsignedIntType(2)
c_uint32 = CUnsignedIntType(4)
c_uint64 = CUnsignedIntType(8)

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


c_byte = _get_from_raw(ctypes.c_byte)
c_ushort = _get_from_raw(ctypes.c_ushort)
c_uint = _get_from_raw(ctypes.c_uint)
c_ulong = _get_from_raw(ctypes.c_ulong)
c_ulonglong = _get_from_raw(ctypes.c_ulonglong)
