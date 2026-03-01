"""
Boolean type handling for binary I/O operations using C-style conventions.

This module provides utilities for reading and writing boolean values in binary
streams following the C language representation of ``bool``. The core
functionality is implemented by :class:`CBoolType`, which reads and writes
fixed-size boolean values. A pre-configured :data:`c_bool` instance is provided
to match the platform's native C ``bool`` size, ensuring compatibility with C
binary data structures.

The module contains the following public components:

* :class:`CBoolType` - Fixed-size boolean type for binary I/O.
* :data:`c_bool` - Pre-configured boolean type instance based on C ``bool`` size.

Example::

    >>> import io
    >>> from hbutils.binary import c_bool
    >>> with io.BytesIO() as file:
    ...     c_bool.write(file, True)
    ...     c_bool.write(file, False)
    ...     file.getvalue()
    b'\\x01\\x00'

.. note::
   The boolean value is encoded with ``0x01`` for ``True`` and ``0x00`` for ``False``,
   padded with leading zeros to match the configured size.

"""

import ctypes
from typing import BinaryIO

from .base import CFixedType

__all__ = [
    'CBoolType',
    'c_bool',
]


class CBoolType(CFixedType):
    """
    Boolean type for binary I/O operations.

    This class provides methods to read and write boolean values in binary format,
    compatible with C language boolean representation.

    :param size: Size of boolean type in bytes.
    :type size: int

    Example::

        >>> import io
        >>> from hbutils.binary import CBoolType
        >>> c_bool_1 = CBoolType(1)
        >>> with io.BytesIO(b'\\x01\\x00') as file:
        ...     c_bool_1.read(file), c_bool_1.read(file)
        (True, False)
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CBoolType`.

        :param size: Size of boolean type in bytes.
        :type size: int
        """
        CFixedType.__init__(self, size)
        self.__size = size

    def read(self, file: BinaryIO) -> bool:
        """
        Read boolean value from binary file.

        The method reads exactly ``size`` bytes and returns ``True`` if any of
        the bytes is non-zero; otherwise, it returns ``False``.

        :param file: Binary file object to read from, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Boolean value read from the file.
        :rtype: bool

        Example::

            >>> import io
            >>> from hbutils.binary import c_bool
            >>> with io.BytesIO(b'\\x01\\x00') as file:
            ...     print(c_bool.read(file))
            ...     print(c_bool.read(file))
            True
            False
        """
        return any(file.read(self.__size))

    def write(self, file: BinaryIO, val: bool) -> None:
        """
        Write boolean value to binary IO object.

        The boolean value is written as a sequence of bytes with the size specified
        during initialization. The value is represented as ``0x01`` for ``True`` and
        ``0x00`` for ``False``, padded with leading zeros to match the required size.

        :param file: Binary file object to write to, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Boolean value to write.
        :type val: bool
        :return: ``None``.
        :rtype: None

        Example::

            >>> import io
            >>> from hbutils.binary import c_bool
            >>> with io.BytesIO() as file:
            ...     c_bool.write(file, True)
            ...     c_bool.write(file, False)
            ...     print(file.getvalue())
            b'\\x01\\x00'
        """
        file.write(b'\x00' * (self.__size - 1) + (b'\x01' if val else b'\x00'))


c_bool = CBoolType(ctypes.sizeof(ctypes.c_bool))
"""
Pre-configured boolean type instance for reading and writing bool values in C language format.

This instance is configured with the size of C's bool type on the current platform,
ensuring compatibility with C binary data structures.

:type: CBoolType

Examples::

    >>> import io
    >>> from hbutils.binary import c_bool
    >>> 
    >>> # Reading boolean values
    >>> with io.BytesIO(b'\\x01\\x00\\x01\\x00') as file:
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    ...     print(c_bool.read(file))
    True
    False
    True
    False

    >>> # Writing boolean values
    >>> with io.BytesIO() as file:
    ...     c_bool.write(file, True)
    ...     c_bool.write(file, False)
    ...     c_bool.write(file, True)
    ...     c_bool.write(file, False)
    ...     print(file.getvalue())
    ... 
    b'\\x01\\x00\\x01\\x00'
"""
