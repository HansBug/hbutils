from typing import BinaryIO, Union

from .base import CIOType

__all__ = [
    'CBufferType',
    'c_buffer',
]


class CBufferType(CIOType):
    """
    Overview:
        Bytes type.
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CBufferType`.

        :param size: Size of the buffer.
        """
        self.__size = size

    @property
    def size(self):
        """
        Size of the buffer.
        """
        return self.__size

    def read(self, file: BinaryIO) -> bytes:
        """
        Read bytes value.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :return: Bytes value.
        """
        return file.read(self.__size)

    def write(self, file: BinaryIO, val: Union[bytearray, bytes]):
        """
        Write bytes value to binary IO object.
        If the length is not enough, ``\\\x00`` will be filled afterwards to reach the given ``size``.

        :param file: Binary file, ``io.BytesIO`` is supported as well.
        :param val: Bytes value to write.
        """
        if not isinstance(val, (bytearray, bytes)):
            raise TypeError(f'Bytearray or bytes expected, but {repr(val)}.')
        if not (0 <= len(val) <= self.__size):
            raise ValueError(f'Size is expected to be no more than {self.__size}, but actual length is {len(val)}.')

        fval = val[:self.__size]
        fval = fval + b'\x00' * (self.__size - len(fval))
        file.write(fval)


def c_buffer(size: int) -> CBufferType:
    """
    Overview:
        Reading and writing bytes with given size.

    :param size: Size of the buffer.
    :return: :class:`CBufferType` object.

    Examples::
        >>> import io
        >>> from hbutils.binary import c_buffer
        >>>
        >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef\\x00\\x12\\x34\\x56\\x78\\x00') as file:
        ...     print(c_buffer(1).read(file))
        ...     print(c_buffer(2).read(file))
        ...     print(c_buffer(3).read(file))
        ...     print(c_buffer(4).read(file))
        b'\\xde'
        b'\\xad\\xbe'
        b'\\xef\\x00\\x12'
        b'4Vx\\x00'
        >>> with io.BytesIO() as file:
        ...     c_buffer(1).write(file, b'\\xde')
        ...     c_buffer(2).write(file, b'\\xad\\xbe')
        ...     c_buffer(3).write(file, b'\\xef\\x00\\x12')
        ...     c_buffer(4).write(file, b'4Vx')  # length is 3
        ...     print(file.getvalue())
        b'\\xde\\xad\\xbe\\xef\\x00\\x124Vx\\x00'
    """
    return CBufferType(size)
