"""
Binary IO type definitions and helpers for fixed-size data structures.

This module defines a small hierarchy of IO types designed to read and write
binary data from file-like objects (e.g., :class:`io.BytesIO` or any
:class:`typing.BinaryIO`). The core abstractions help describe fixed-size
data structures, integer ranges, and types that can be directly packed
with the :mod:`struct` module.

The module contains the following main components:

* :class:`CIOType` - Base class defining the read/write interface
* :class:`CFixedType` - Fixed-size IO type with a known byte width
* :class:`CRangedIntType` - Fixed-size integer type with value constraints
* :class:`CMarkedType` - Fixed-size type using a struct format mark

Example::

    >>> import io
    >>> int_type = CMarkedType('i', 4)
    >>> buffer = io.BytesIO()
    >>> int_type.write(buffer, 5)
    >>> buffer.seek(0)
    0
    >>> int_type.read(buffer)
    5

.. note::
   All IO types operate on binary streams. Text streams are not supported.

"""

import struct
from typing import Any, BinaryIO


class CIOType:
    """
    Basic IO type.

    Used as base class of all the IO types. Provides the interface for reading from
    and writing to binary IO objects.
    """

    def read(self, file: BinaryIO) -> Any:
        """
        Read from binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Reading result.
        :rtype: Any

        .. warning::
            Need to be implemented in subclasses.

        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val: Any) -> None:
        """
        Write object to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Object to write.
        :type val: Any
        :return: ``None``.
        :rtype: None

        .. warning::
            Need to be implemented in subclasses.

        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover


class CFixedType(CIOType):
    """
    Type with fixed size.

    Represents types with a fixed size in bytes, such as ``int``, ``uint`` and ``float``.
    This class extends CIOType to add size information.
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CFixedType`.

        :param size: Size of the type in bytes.
        :type size: int
        """
        self.__size = size

    @property
    def size(self) -> int:
        """
        Size of the given type in bytes.

        :return: The size of the type.
        :rtype: int
        """
        return self.__size

    def read(self, file: BinaryIO) -> Any:
        """
        Read from binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Reading result.
        :rtype: Any

        .. warning::
            Need to be implemented in subclasses.

        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val: Any) -> None:
        """
        Write object to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Object to write.
        :type val: Any
        :return: ``None``.
        :rtype: None

        .. warning::
            Need to be implemented in subclasses.

        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover


class CRangedIntType(CFixedType):
    """
    Type with fixed size and value range.

    Represents integer types with fixed size and range constraints, such as ``int`` and ``uint``.
    This class extends CFixedType to add minimum and maximum value constraints.
    """

    def __init__(self, size: int, minimum: int, maximum: int):
        """
        Constructor of :class:`CRangedIntType`.

        :param size: Size of the type in bytes.
        :type size: int
        :param minimum: Minimum value of the type.
        :type minimum: int
        :param maximum: Maximum value of the type.
        :type maximum: int
        """
        CFixedType.__init__(self, size)
        self.__size = size
        self.__minimum = minimum
        self.__maximum = maximum

    @property
    def minimum(self) -> int:
        """
        Minimum value of the type.

        :return: The minimum value that can be represented by this type.
        :rtype: int
        """
        return self.__minimum

    @property
    def maximum(self) -> int:
        """
        Maximum value of the type.

        :return: The maximum value that can be represented by this type.
        :rtype: int
        """
        return self.__maximum

    def read(self, file: BinaryIO) -> Any:
        """
        Read from binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Reading result.
        :rtype: Any

        .. warning::
            Need to be implemented in subclasses.

        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val: Any) -> None:
        """
        Write object to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Object to write.
        :type val: Any
        :return: ``None``.
        :rtype: None

        .. warning::
            Need to be implemented in subclasses.

        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover


class CMarkedType(CFixedType):
    """
    Type with struct mark.

    Represents types that can be directly read and written using Python's ``struct`` module.
    The mark parameter corresponds to format characters used by struct (e.g., 'i' for int, 'f' for float).

    Example::
        >>> import io
        >>> float_type = CMarkedType('f', 4)
        >>> buffer = io.BytesIO()
        >>> float_type.write(buffer, 3.14)
        >>> buffer.seek(0)
        0
        >>> float_type.read(buffer)
        3.140000104904175
    """

    def __init__(self, mark: str, size: int):
        """
        Constructor of :class:`CMarkedType`.

        :param mark: Format character for the struct module (e.g., 'i', 'f', 'd').
        :type mark: str
        :param size: Size of the type in bytes.
        :type size: int
        """
        CFixedType.__init__(self, size)
        self.__mark = mark

    @property
    def mark(self) -> str:
        """
        Mark of the type.

        The format character that will be used to read from and write to binary data
        with the ``struct`` module.

        :return: The struct format character.
        :rtype: str
        """
        return self.__mark

    def read(self, file: BinaryIO) -> Any:
        """
        Read from binary with ``struct`` module.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Result value read from the binary file.
        :rtype: Any

        Example::
            >>> import io
            >>> buffer = io.BytesIO(b'\\x00\\x00\\x00\\x05')
            >>> int_type = CMarkedType('i', 4)
            >>> int_type.read(buffer)
            5
        """
        r, = struct.unpack(self.mark, file.read(self.size))
        return r

    def write(self, file: BinaryIO, val: Any) -> None:
        """
        Write value to binary IO with ``struct`` module.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Writing value. Will be converted to float before packing.
        :type val: Any
        :return: ``None``.
        :rtype: None

        Example::
            >>> import io
            >>> buffer = io.BytesIO()
            >>> float_type = CMarkedType('f', 4)
            >>> float_type.write(buffer, 3.14)
            >>> buffer.getvalue()
            b'\\xc3\\xf5H@'
        """
        file.write(struct.pack(self.mark, float(val)))
