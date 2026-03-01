"""
Binary floating-point type utilities for structured I/O.

This module provides floating-point type definitions for binary input/output
operations based on the :mod:`struct` module. It defines convenience classes and
instances for standard IEEE-754 floating-point sizes (16-bit, 32-bit, 64-bit),
along with aliases matching the conventional C type names.

The module exposes the following public components:

* :class:`CFloatType` - Float type wrapper with binary read/write helpers
* :data:`c_float16` - 16-bit (half precision) float type instance
* :data:`c_float32` - 32-bit (single precision) float type instance
* :data:`c_float64` - 64-bit (double precision) float type instance
* :data:`c_float` - Alias for :data:`c_float32`
* :data:`c_double` - Alias for :data:`c_float64`

Example::

    >>> import io
    >>> from hbutils.binary.float import c_float32
    >>>
    >>> buffer = io.BytesIO()
    >>> c_float32.write(buffer, 3.5)
    >>> buffer.seek(0)
    0
    >>> c_float32.read(buffer)
    3.5

.. note::
   These types are thin wrappers around :class:`hbutils.binary.base.CMarkedType`,
   which uses the :mod:`struct` module for binary packing and unpacking.

"""

import ctypes
from typing import Any, BinaryIO, Dict, List, Type, Union

from .base import CMarkedType

__all__ = [
    'CFloatType',
    'c_float16', 'c_float32', 'c_float64',
    'c_float', 'c_double',
]


class CFloatType(CMarkedType):
    """
    Float type class for binary I/O operations, based on the ``struct`` module.

    This class extends :class:`hbutils.binary.base.CMarkedType` to provide
    specialized handling for floating-point numbers in binary format. It
    enforces conversion to ``float`` when writing values.

    Example::

        >>> import io
        >>> from hbutils.binary.float import CFloatType
        >>>
        >>> float_type = CFloatType('f', 4)
        >>> buffer = io.BytesIO()
        >>> float_type.write(buffer, 1.25)
        >>> buffer.seek(0)
        0
        >>> float_type.read(buffer)
        1.25
    """

    def read(self, file: BinaryIO) -> float:
        """
        Read a floating-point value from a binary file.

        :param file: The binary file to read from.
        :type file: BinaryIO
        :return: The floating-point value read from the file.
        :rtype: float
        """
        return super().read(file)

    def write(self, file: BinaryIO, val: Union[int, float]) -> None:
        """
        Write a floating-point value to a binary file.

        :param file: The binary file to write to.
        :type file: BinaryIO
        :param val: The numeric value to write (will be converted to float).
        :type val: Union[int, float]
        :return: ``None``.
        :rtype: None
        """
        super().write(file, float(val))


c_float16 = CFloatType('e', 2)
"""
Reading and writing half-precision (16-bit) floating-point numbers.

This type uses 2 bytes to represent floating-point values with reduced precision.

Example::

    >>> import io
    >>> from hbutils.binary.float import c_float16
    >>>
    >>> buffer = io.BytesIO()
    >>> c_float16.write(buffer, 1.5)
    >>> buffer.seek(0)
    0
    >>> c_float16.read(buffer)
    1.5
"""

c_float32 = CFloatType('f', 4)
"""
Reading and writing single-precision (32-bit) floating-point numbers.

This type uses 4 bytes to represent floating-point values.

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
Reading and writing double-precision (64-bit) floating-point numbers.

This type uses 8 bytes to represent floating-point values with higher precision.

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
"""List of all available floating-point types."""

_SIZE_TO_FLOAT_TYPE: Dict[int, CFloatType] = {
    item.size: item
    for item in _EXIST_TYPES
}
"""Mapping from byte size to corresponding CFloatType instance."""


def _get_from_raw(tp: Type[ctypes._SimpleCData]) -> CFloatType:
    """
    Get the corresponding :class:`CFloatType` from a ``ctypes`` float type.

    :param tp: A ctypes float type (e.g., :class:`ctypes.c_float`,
               :class:`ctypes.c_double`).
    :type tp: Type[ctypes._SimpleCData]
    :return: The corresponding :class:`CFloatType` instance.
    :rtype: CFloatType
    """
    return _SIZE_TO_FLOAT_TYPE[ctypes.sizeof(tp)]


c_float = _get_from_raw(ctypes.c_float)
"""
Alias for :data:`c_float32`.

This provides a convenient name matching the C language's ``float`` type.
"""

c_double = _get_from_raw(ctypes.c_double)
"""
Alias for :data:`c_float64`.

This provides a convenient name matching the C language's ``double`` type.
"""
