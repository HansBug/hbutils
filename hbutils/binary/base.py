import struct
from typing import BinaryIO


class CIOType:
    """
    Overview:
        Basic IO type.
        Used as base class of all the IO types.
    """

    def read(self, file: BinaryIO):
        """
        Read from binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :return: Reading result.

        .. warning::
            Need to be implemented.
        """
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        """
        Write object to binary IO object.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :param val: Object to write.

        .. warning::
            Need to be implemented.
        """
        raise NotImplementedError  # pragma: no cover


class CFixedType(CIOType):
    """
    Overview:
        Type with fixed size (such as ``int``, ``uint`` and ``float``).
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CFixedType`.

        :param size: Size of the type.
        """
        self.__size = size

    @property
    def size(self) -> int:
        """
        Size of the given type.
        """
        return self.__size

    def read(self, file: BinaryIO):
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        raise NotImplementedError  # pragma: no cover


class CRangedIntType(CFixedType):
    """
    Overview:
        Type with fixed size and range (such as ``int`` and ``uint``).
    """

    def __init__(self, size: int, minimum: int, maximum: int):
        """
        Constructor of :class:`CRangedIntType`.

        :param size: Size of the type.
        :param minimum: Min value of the type.
        :param maximum: Max value of the type.
        """
        CFixedType.__init__(self, size)
        self.__size = size
        self.__minimum = minimum
        self.__maximum = maximum

    @property
    def minimum(self) -> int:
        """
        Min value of the type.
        """
        return self.__minimum

    @property
    def maximum(self) -> int:
        """
        Max value of the type.
        """
        return self.__maximum

    def read(self, file: BinaryIO):
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        raise NotImplementedError  # pragma: no cover


class CMarkedType(CFixedType):
    """
    Overview:
        Type with struct mark, which can be directly read by ``struct`` module.
    """

    def __init__(self, mark: str, size: int):
        """
        Constructor of :class:`CMarkedType`.

        :param mark: Mark of the type.
        :param size: Size of the type.
        """
        CFixedType.__init__(self, size)
        self.__mark = mark

    @property
    def mark(self) -> str:
        """
        Mark of the type, will be used to read from binary data with ``struct`` module.
        """
        return self.__mark

    def read(self, file: BinaryIO):
        """
        Read from binary with ``struct`` module.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :return: Result value.
        """
        r, = struct.unpack(self.mark, file.read(self.size))
        return r

    def write(self, file: BinaryIO, val):
        """
        Write value to binary IO with ``struct`` module.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :param val: Writing value.
        """
        file.write(struct.pack(self.mark, float(val)))
