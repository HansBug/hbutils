import ctypes
from typing import Dict, BinaryIO, List

from .base import CRangedIntType
from .uint import CUnsignedIntType

__all__ = [
    'CSignedIntType',
    'c_int8', 'c_int16', 'c_int32', 'c_int64',
    'c_short', 'c_int', 'c_long', 'c_longlong',
]


class CSignedIntType(CRangedIntType):
    def __init__(self, byte_count: int):
        self.__byte_count = byte_count
        self._unit = CUnsignedIntType(byte_count)
        self.__half = 1 << (8 * self.__byte_count - 1)
        CRangedIntType.__init__(
            self, self.__byte_count,
            self._unit.minimum - self.__half,
            self._unit.maximum - self.__half
        )

    def read(self, file: BinaryIO) -> int:
        uval = self._unit.read(file)
        if uval < self.__half:
            return uval
        else:
            return uval - (self.__half << 1)

    def write(self, file: BinaryIO, val: int):
        if not isinstance(val, int):
            raise TypeError(f'Int value expected, but {repr(val)} found.')
        elif not (self.minimum <= val <= self.maximum):
            raise ValueError(f'Signed int value within '
                             f'[{self.minimum}, {self.maximum}] expected, but {repr(val)} found.')

        fval = val if val > 0 else val + (self.__half << 1)
        self._unit.write(file, fval)


c_int8 = CSignedIntType(1)
c_int16 = CSignedIntType(2)
c_int32 = CSignedIntType(4)
c_int64 = CSignedIntType(8)

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


c_short = _get_from_raw(ctypes.c_short)
c_int = _get_from_raw(ctypes.c_int)
c_long = _get_from_raw(ctypes.c_long)
c_longlong = _get_from_raw(ctypes.c_longlong)
