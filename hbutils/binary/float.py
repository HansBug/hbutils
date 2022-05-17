import ctypes
from typing import BinaryIO, Dict, List, Union

from .base import CMarkedType

__all__ = [
    'CFloatType',
    'c_float16', 'c_float32', 'c_float64',
    'c_float', 'c_double',
]


class CFloatType(CMarkedType):
    """
    Overview:
        Float type, based on ``struct`` module.
    """

    def read(self, file: BinaryIO) -> float:
        return super().read(file)

    def write(self, file: BinaryIO, val: Union[int, float]):
        super().write(file, float(val))


c_float16 = CFloatType('e', 2)
"""
Overview:
    Reading and writing half-precision(16-bits) float.
"""
c_float32 = CFloatType('f', 4)
"""
Overview:
    Reading and writing single-precision(32-bits) float.

Examples::
    >>> import io
    >>> import math
    >>> from hbutils.binary import c_float32
    >>>
    >>> with io.BytesIO(b'\\x00\\x00\\x90\\x7f'
    ...                 b'\\x00\\x00\\x80\\x7f'
    ...                 b'\\x00\\xa0\\x3e\\xc1'
    ...                 b'\\x00\\x00\\x70\\x00') as file:
    ...     print(c_float32.read(file))
    ...     print(c_float32.read(file))
    ...     print(c_float32.read(file))
    ...     print(c_float32.read(file))
    nan
    inf
    -11.9140625
    1.0285575569695016e-38
    >>> with io.BytesIO() as file:
    ...     c_float32.write(file, math.nan)
    ...     c_float32.write(file, +math.inf)
    ...     c_float32.write(file, -11.9140625)
    ...     c_float32.write(file, 1.0285575569695016e-38)
    ...     print(file.getvalue())
    b'\\x00\\x00\\xc0\\x7f\\x00\\x00\\x80\\x7f\\x00\\xa0>\\xc1\\x00\\x00p\\x00'
"""
c_float64 = CFloatType('d', 8)
"""
Overview:
    Reading and writing double-precision(64-bits) float.

Examples::
    >>> import io
    >>> import math
    >>> from hbutils.binary import c_float64
    >>>
    >>> with io.BytesIO(b'\\x00\\x00\\x00\\x00\\x00\\x00\\xf8\\x7f'
    ...                 b'\\x00\\x00\\x00\\x00\\x00\\x00\\xf0\\x7f'
    ...                 b'\\x00\\x00\\x00\\x00\\x00\\xd4\\x27\\xc0'
    ...                 b'\\x00\\x00\\x00\\x00\\x00\\x00\\x0c8') as file:
    ...     print(c_float64.read(file))
    ...     print(c_float64.read(file))
    ...     print(c_float64.read(file))
    ...     print(c_float64.read(file))
    nan
    inf
    -11.9140625
    1.0285575569695016e-38
    >>> with io.BytesIO() as file:
    ...     c_float64.write(file, math.nan)
    ...     c_float64.write(file, +math.inf)
    ...     c_float64.write(file, -11.9140625)
    ...     c_float64.write(file, 1.0285575569695016e-38)
    ...     print(file.getvalue())
    b"\\x00\\x00\\x00\\x00\\x00\\x00\\xf8\\x7f\\x00\\x00\\x00\\x00\\x00\\x00\\xf0\\x7f\\x00\\x00\\x00\\x00\\x00\\xd4'\\xc0\\x00\\x00\\x00\\x00\\x00\\x00\\x0c8"
"""

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
"""
Alias for :data:`c_float32`.
"""
c_double = _get_from_raw(ctypes.c_double)
"""
Alias for :data:`c_float64`.
"""
