"""
This module provides a read-write lock implementation for controlling concurrent access to shared resources.

The ReadWriteLock class implements a reader-writer lock that allows multiple concurrent readers
or a single exclusive writer, following these rules:

- Read-Read: Non-exclusive, allows concurrent access
- Read-Write: Exclusive, write operations wait for all read operations to complete
- Write-Write: Exclusive, write operations execute serially
- Write-Read: Exclusive, read operations wait for write operations to complete

This is useful for scenarios where you have frequent read operations and occasional write operations,
allowing better performance through concurrent reads while maintaining data consistency.
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

    :param lock_factory: Factory function to create lock objects, defaults to threading.Lock
    :type lock_factory: Callable
    """

    def __init__(self, lock_factory: Callable = threading.Lock):
        """
        Initialize the ReadWriteLock.

        :param lock_factory: Factory function to create lock objects, defaults to threading.Lock
        :type lock_factory: Callable
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
        """
        self._write_ready.acquire()

    def release_write(self) -> None:
        """
        Release a write lock.

        This method releases the exclusive write lock, allowing pending readers
        and writers to proceed according to the lock's scheduling policy.
        """
        self._write_ready.release()

    @contextmanager
    def read_lock(self) -> Generator[None, None, None]:
        """
        Context manager for read lock operations.

        This method provides a convenient way to acquire and automatically release
        a read lock using the 'with' statement. The lock is guaranteed to be
        released even if an exception occurs within the context.

        :return: Generator for context management
        :rtype: Generator[None, None, None]

        Example:
            >>> rwlock = ReadWriteLock()
            >>> with rwlock.read_lock():
            ...     # Perform read operations
            ...     data = shared_resource.read()
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
        a write lock using the 'with' statement. The lock is guaranteed to be
        released even if an exception occurs within the context.

        :return: Generator for context management
        :rtype: Generator[None, None, None]

        Example:
            >>> rwlock = ReadWriteLock()
            >>> with rwlock.write_lock():
            ...     # Perform write operations
            ...     shared_resource.write(new_data)
        """
        self.acquire_write()
        try:
            yield
        finally:
            self.release_write()
