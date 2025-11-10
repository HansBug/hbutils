"""
This module provides basic IO types for binary file operations.

It defines a hierarchy of classes for reading and writing binary data with different characteristics:
- CIOType: Base class for all IO types
- CFixedType: Types with fixed size (int, uint, float, etc.)
- CRangedIntType: Fixed-size types with value range constraints
- CMarkedType: Types that can be read/written using Python's struct module

These classes are designed to work with binary file objects and io.BytesIO instances.
"""

import struct
from typing import BinaryIO


class CIOType:
    """
    Basic IO type.
    
    Used as base class of all the IO types. Provides the interface for reading from
    and writing to binary IO objects.
    """

    def read(self, file: BinaryIO):
        """
        Read from binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Reading result.

        .. warning::
            Need to be implemented in subclasses.
        
        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        """
        Write object to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Object to write.

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

    def read(self, file: BinaryIO):
        """
        Read from binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Reading result.

        .. warning::
            Need to be implemented in subclasses.
        
        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        """
        Write object to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Object to write.

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

    def read(self, file: BinaryIO):
        """
        Read from binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Reading result.

        .. warning::
            Need to be implemented in subclasses.
        
        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        """
        Write object to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Object to write.

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

    def read(self, file: BinaryIO):
        """
        Read from binary with ``struct`` module.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Result value read from the binary file.
        
        Example::
            >>> import io
            >>> buffer = io.BytesIO(b'\\x00\\x00\\x00\\x05')
            >>> int_type = CMarkedType('i', 4)
            >>> int_type.read(buffer)
            5
        """
        r, = struct.unpack(self.mark, file.read(self.size))
        return r

    def write(self, file: BinaryIO, val):
        """
        Write value to binary IO with ``struct`` module.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Writing value. Will be converted to float before packing.
        
        Example::
            >>> import io
            >>> buffer = io.BytesIO()
            >>> float_type = CMarkedType('f', 4)
            >>> float_type.write(buffer, 3.14)
            >>> buffer.getvalue()
            b'\\xc3\\xf5H@'
        """
        file.write(struct.pack(self.mark, float(val)))
