"""
Fixed-size binary buffer utilities.

This module provides a binary I/O type for reading and writing fixed-size byte
buffers. The core abstraction is :class:`CBufferType`, which reads an exact
number of bytes from a binary stream and writes byte data padded with null bytes
(``\\x00``) when the input is shorter than the configured buffer size.

The module contains the following main components:

* :class:`CBufferType` - Fixed-size buffer reader/writer implementation
* :func:`c_buffer` - Convenience factory for :class:`CBufferType`

Example::

    >>> import io
    >>> from hbutils.binary.buffer import c_buffer
    >>>
    >>> # Reading example
    >>> with io.BytesIO(b'\\xde\\xad\\xbe\\xef\\x00\\x12\\x34\\x56\\x78\\x00') as file:
    ...     print(c_buffer(1).read(file))
    ...     print(c_buffer(2).read(file))
    ...     print(c_buffer(3).read(file))
    ...     print(c_buffer(4).read(file))
    b'\\xde'
    b'\\xad\\xbe'
    b'\\xef\\x00\\x12'
    b'4Vx\\x00'
    >>>
    >>> # Writing example
    >>> with io.BytesIO() as file:
    ...     c_buffer(1).write(file, b'\\xde')
    ...     c_buffer(2).write(file, b'\\xad\\xbe')
    ...     c_buffer(3).write(file, b'\\xef\\x00\\x12')
    ...     c_buffer(4).write(file, b'4Vx')  # length is 3, will be padded to 4
    ...     print(file.getvalue())
    b'\\xde\\xad\\xbe\\xef\\x00\\x124Vx\\x00'

.. note::
   The read operation returns exactly the number of bytes requested by the buffer
   size. If fewer bytes are available in the stream, the returned value may be
   shorter, depending on the underlying stream behavior.

"""

from typing import BinaryIO, Union

from .base import CIOType

__all__ = [
    'CBufferType',
    'c_buffer',
]


class CBufferType(CIOType):
    """
    A binary I/O type for handling fixed-size byte buffers.

    This class provides methods to read and write byte data with a predetermined
    size. When writing data shorter than the buffer size, it automatically pads
    the output with null bytes (``\\x00``) to the configured size.

    :param size: Size of the buffer in bytes.
    :type size: int

    :ivar __size: Internal buffer size in bytes.
    :vartype __size: int

    Example::

        >>> import io
        >>> buf = CBufferType(4)
        >>> with io.BytesIO(b'\\x01\\x02\\x03\\x04\\x05') as file:
        ...     buf.read(file)
        b'\\x01\\x02\\x03\\x04'
    """

    def __init__(self, size: int):
        """
        Constructor of :class:`CBufferType`.

        :param size: Size of the buffer in bytes.
        :type size: int
        """
        self.__size = size

    @property
    def size(self) -> int:
        """
        Get the size of the buffer.

        :return: Size of the buffer in bytes.
        :rtype: int
        """
        return self.__size

    def read(self, file: BinaryIO) -> bytes:
        """
        Read bytes value from a binary file.

        :param file: Binary file object to read from. ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :return: Bytes value read from the file with the specified buffer size.
        :rtype: bytes

        .. note::
           The returned value is exactly what the stream returns for ``read(size)``.
        """
        return file.read(self.__size)

    def write(self, file: BinaryIO, val: Union[bytearray, bytes]) -> None:
        """
        Write bytes value to binary IO object.

        If the length of the provided value is less than the buffer size,
        null bytes (``\\x00``) will be appended to reach the specified size.

        :param file: Binary file object to write to. ``io.BytesIO`` is supported as well.
        :type file: BinaryIO
        :param val: Bytes value to write. Must be of type :class:`bytearray` or :class:`bytes`.
        :type val: Union[bytearray, bytes]
        :return: ``None``.
        :rtype: None
        :raises TypeError: If ``val`` is not a :class:`bytearray` or :class:`bytes` object.
        :raises ValueError: If the length of ``val`` exceeds the buffer size.

        Example::

            >>> import io
            >>> buf = CBufferType(4)
            >>> with io.BytesIO() as file:
            ...     buf.write(file, b'\\x01\\x02')
            ...     file.getvalue()
            b'\\x01\\x02\\x00\\x00'
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
    Create a buffer type for reading and writing bytes with a given size.

    This function returns a :class:`CBufferType` object that can be used to read
    and write fixed-size byte buffers. When writing, if the data is shorter than
    the specified size, it will be padded with null bytes.

    :param size: Size of the buffer in bytes.
    :type size: int
    :return: A :class:`CBufferType` object configured with the specified size.
    :rtype: CBufferType

    Example::

        >>> import io
        >>> from hbutils.binary.buffer import c_buffer
        >>> with io.BytesIO() as file:
        ...     c_buffer(3).write(file, b'\\x10\\x20')
        ...     file.getvalue()
        b'\\x10\\x20\\x00'
    """
    return CBufferType(size)
