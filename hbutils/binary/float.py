import ctypes
from typing import BinaryIO, Dict, List, Union

from .base import CMarkedType

__all__ = [
    'CFloatType',
    'c_float16', 'c_float32', 'c_float64',
    'c_float', 'c_double',
]


class CFloatType(CMarkedType):
    def read(self, file: BinaryIO) -> float:
        return super().read(file)

    def write(self, file: BinaryIO, val: Union[int, float]):
        super().write(file, float(val))


c_float16 = CFloatType('e', 2)
c_float32 = CFloatType('f', 4)
c_float64 = CFloatType('d', 8)

_EXIST_TYPES: List[CFloatType] = [
    c_float16,
    c_float32,
    c_float64,
]
_SIZE_TO_FLOAT_TYPE: Dict[int, CFloatType] = {
    item.size: item
    for item in _EXIST_TYPES
}


def _get_from_raw(tp) -> CFloatType:
    return _SIZE_TO_FLOAT_TYPE[ctypes.sizeof(tp)]


c_float = _get_from_raw(ctypes.c_float)
c_double = _get_from_raw(ctypes.c_double)
