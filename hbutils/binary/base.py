from typing import BinaryIO


class CIOType:
    def read(self, file: BinaryIO):
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        raise NotImplementedError  # pragma: no cover


class CFixedType(CIOType):
    def _size(self) -> int:
        raise NotImplementedError  # pragma: no cover

    @property
    def size(self) -> int:
        return self._size()

    def read(self, file: BinaryIO):
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        raise NotImplementedError  # pragma: no cover


class CRangedIntType(CFixedType):
    def __init__(self, size: int, minimum: int, maximum: int):
        self.__size = size
        self.__minimum = minimum
        self.__maximum = maximum

    def _size(self) -> int:
        return self.__size

    @property
    def maximum(self) -> int:
        return self.__maximum

    @property
    def minimum(self) -> int:
        return self.__minimum

    def read(self, file: BinaryIO):
        raise NotImplementedError  # pragma: no cover

    def write(self, file: BinaryIO, val):
        raise NotImplementedError  # pragma: no cover
