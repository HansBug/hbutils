"""
Read-write lock utilities for coordinating concurrent access to shared resources.

This module provides a :class:`ReadWriteLock` implementation that allows
multiple concurrent readers or a single exclusive writer. It is useful for
scenarios where read operations are frequent and write operations are
occasional, improving overall throughput by permitting concurrent reads while
preserving consistency for writes.

The module contains the following main component:

* :class:`ReadWriteLock` - Reader-writer lock with convenience context managers

Example::

    >>> from hbutils.concurrent.readwrite import ReadWriteLock
    >>> lock = ReadWriteLock()
    >>> # Concurrent readers
    >>> with lock.read_lock():
    ...     # read shared state
    ...     pass
    >>> # Exclusive writer
    >>> with lock.write_lock():
    ...     # modify shared state
    ...     pass

.. note::
   The lock factory must return a lock object supporting ``acquire`` and
   ``release`` and acting as a context manager (e.g., :func:`threading.Lock`).

"""

import threading
from contextlib import contextmanager
from typing import Generator, Callable

__all__ = [
    'ReadWriteLock',
]


class ReadWriteLock:
    """
    A read-write lock implementation for controlling concurrent access to shared resources.

    This class implements a reader-writer lock that allows multiple concurrent readers
    or a single exclusive writer. The lock follows these exclusion rules:

    - Read-Read: Non-exclusive, multiple readers can access concurrently
    - Read-Write: Exclusive, write operations must wait for all read operations to complete
    - Write-Write: Exclusive, write operations execute serially
    - Write-Read: Exclusive, read operations must wait for write operations to complete

    The lock is designed to optimize scenarios with frequent read operations and occasional
    write operations, providing better performance through concurrent reads while maintaining
    data consistency during writes.

    :param lock_factory: Factory function to create lock objects, defaults to :func:`threading.Lock`
    :type lock_factory: Callable[[], threading.Lock]

    Example::

        >>> lock = ReadWriteLock()
        >>> lock.acquire_read()
        >>> try:
        ...     # perform read operations
        ...     pass
        ... finally:
        ...     lock.release_read()
    """

    def __init__(self, lock_factory: Callable[[], threading.Lock] = threading.Lock) -> None:
        """
        Initialize the ReadWriteLock.

        :param lock_factory: Factory function to create lock objects, defaults to :func:`threading.Lock`
        :type lock_factory: Callable[[], threading.Lock]
        """
        # Lock to protect the reader count
        self._read_ready = lock_factory()
        # Write lock to ensure write operations are mutually exclusive
        self._write_ready = lock_factory()
        # Current number of readers
        self._readers = 0

    def acquire_read(self) -> None:
        """
        Acquire a read lock.

        This method allows multiple threads to acquire read locks concurrently.
        The first reader will block any potential writers by acquiring the write lock.
        Subsequent readers can proceed without blocking as long as no writer is waiting.

        :return: None
        :rtype: None
        """
        with self._read_ready:
            self._readers += 1
            if self._readers == 1:
                # First reader needs to acquire write lock to prevent write operations
                self._write_ready.acquire()

    def release_read(self) -> None:
        """
        Release a read lock.

        This method decrements the reader count and releases the write lock
        when the last reader finishes, allowing pending write operations to proceed.

        :return: None
        :rtype: None
        :raises RuntimeError: If there are no active readers to release
        """
        with self._read_ready:
            if self._readers == 0:
                raise RuntimeError('Release unlocked reader lock.')
            self._readers -= 1
            if self._readers == 0:
                # Last reader releases write lock, allowing write operations
                self._write_ready.release()

    def acquire_write(self) -> None:
        """
        Acquire a write lock.

        This method provides exclusive access for write operations. It will block
        until all current readers have finished and no other writers are active.
        Once acquired, no new readers or writers can proceed until the write lock is released.

        :return: None
        :rtype: None
        """
        self._write_ready.acquire()

    def release_write(self) -> None:
        """
        Release a write lock.

        This method releases the exclusive write lock, allowing pending readers
        and writers to proceed according to the lock's scheduling policy.

        :return: None
        :rtype: None
        """
        self._write_ready.release()

    @contextmanager
    def read_lock(self) -> Generator[None, None, None]:
        """
        Context manager for read lock operations.

        This method provides a convenient way to acquire and automatically release
        a read lock using the ``with`` statement. The lock is guaranteed to be
        released even if an exception occurs within the context.

        :return: Generator for context management
        :rtype: Generator[None, None, None]

        Example::

            >>> rwlock = ReadWriteLock()
            >>> with rwlock.read_lock():
            ...     # Perform read operations
            ...     pass
        """
        self.acquire_read()
        try:
            yield
        finally:
            self.release_read()

    @contextmanager
    def write_lock(self) -> Generator[None, None, None]:
        """
        Context manager for write lock operations.

        This method provides a convenient way to acquire and automatically release
        a write lock using the ``with`` statement. The lock is guaranteed to be
        released even if an exception occurs within the context.

        :return: Generator for context management
        :rtype: Generator[None, None, None]

        Example::

            >>> rwlock = ReadWriteLock()
            >>> with rwlock.write_lock():
            ...     # Perform write operations
            ...     pass
        """
        self.acquire_write()
        try:
            yield
        finally:
            self.release_write()
