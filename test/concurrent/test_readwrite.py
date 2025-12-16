"""
This module provides comprehensive testing for the ReadWriteLock concurrent utility.

The module contains test cases that verify the behavior of ReadWriteLock in various
concurrent scenarios, including multiple readers, exclusive writers, and mixed
read-write operations. It includes helper classes and functions to simulate
realistic concurrent access patterns and verify proper synchronization behavior.
"""
import logging
import random
import threading
import time
from datetime import datetime

import pytest

from hbutils.concurrent import ReadWriteLock
from hbutils.reflection import progressive_for
from hbutils.testing import tmatrix


def log_message(message: str) -> None:
    """
    Log a message with timestamp and thread information.

    This function outputs a formatted log message that includes the current
    timestamp (with milliseconds) and the name of the current thread. This
    is useful for debugging and monitoring concurrent operations.

    :param message: The message to log.
    :type message: str
    """
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    thread_name = threading.current_thread().name
    logging.info(f"[{timestamp}] {thread_name}: {message}")


class SharedResource:
    """
    Simulate a shared resource with read-write lock protection.

    This class represents a shared data resource that can be safely accessed
    by multiple readers concurrently or by a single writer exclusively.
    It uses ReadWriteLock to ensure proper synchronization and data consistency.

    The class maintains an integer data value and provides thread-safe methods
    for reading and writing this value with simulated processing delays.
    """

    def __init__(self, read_time_cost: float = 0.5, write_time_cost: float = 0.8) -> None:
        """
        Initialize the shared resource.

        Creates a new SharedResource instance with initial data value of 0
        and a new ReadWriteLock for synchronization.
        """
        self.data = 0
        self.rw_lock = ReadWriteLock()
        self._read_time_cost = read_time_cost
        self._write_time_cost = write_time_cost
        self.operations = []

    def read_data(self, reader_id: int) -> int:
        """
        Read data from the shared resource.

        This method acquires a read lock, reads the current data value,
        simulates processing time, and then releases the lock. Multiple
        readers can execute this method concurrently.

        :param reader_id: Unique identifier for the reader thread.
        :type reader_id: int

        :return: The current data value at the time of reading.
        :rtype: int
        """
        with self.rw_lock.read_lock():
            start_time = time.time()
            log_message(f"Reader-{reader_id} starts reading")
            current_data = self.data
            # Simulate read processing time
            time.sleep(self._read_time_cost)
            log_message(f"Reader-{reader_id} finished reading, data value: {current_data}")
            end_time = time.time()
            self.operations.append((start_time, end_time, 'read'))
            return current_data

    def write_data(self, writer_id: int, new_value: int) -> None:
        """
        Write data to the shared resource.

        This method acquires an exclusive write lock, updates the data value,
        simulates processing time, and then releases the lock. Only one writer
        can execute this method at a time, and no readers can access the data
        during writing.

        :param writer_id: Unique identifier for the writer thread.
        :type writer_id: int
        :param new_value: The new value to write to the shared resource.
        :type new_value: int
        """
        with self.rw_lock.write_lock():
            start_time = time.time()
            log_message(f"Writer-{writer_id} starts writing")
            old_value = self.data
            # Simulate write processing time
            time.sleep(self._write_time_cost)
            self.data = new_value
            log_message(f"Writer-{writer_id} finished writing, {old_value} -> {new_value}")
            end_time = time.time()
            self.operations.append((start_time, end_time, 'write'))

    def assert_write_write_exclusive(self):
        for (t0s, t0e, t0t), (t1s, t1e, t1t) in progressive_for(self.operations, n=2):
            if t0t == 'write' and t1t == 'write':
                assert (t0e <= t1s) or (t1e <= t0s), \
                    f'Write-Write operation conflict - {(t0s, t0e, t0t)!r} vs {(t1s, t1e, t1t)!r}.'

    def assert_read_write_exclusive(self):
        for (t0s, t0e, t0t), (t1s, t1e, t1t) in progressive_for(self.operations, n=2):
            if (t0t == 'read' and t1t == 'write') or (t1t == 'read' and t0t == 'write'):
                assert (t0e <= t1s) or (t1e <= t0s), \
                    f'Read-Write operation conflict - {(t0s, t0e, t0t)!r} vs {(t1s, t1e, t1t)!r}.'


@pytest.mark.unittest
class TestConcurrentReadWriteLock:
    @pytest.mark.parametrize(*tmatrix({
        'read_time_cost': [0.5, 0.8, 1.0],
        'thread_count': [5, 10, 20],
    }))
    def test_read_concurrent(self, read_time_cost, thread_count):
        resource = SharedResource(read_time_cost=read_time_cost)
        resource.data = 100

        def concurrent_read(reader_id: int):
            start = time.time()
            resource.read_data(reader_id)
            duration = time.time() - start
            log_message(f"Reader-{reader_id} time cost: {duration:.2f}秒")

        threads = []
        overall_start = time.time()

        for i in range(thread_count):
            thread = threading.Thread(
                target=concurrent_read,
                args=(i + 1,),
                name=f"ConcurrentReader-{i + 1}"
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        overall_duration = time.time() - overall_start
        assert overall_duration == pytest.approx(read_time_cost, abs=0.05)
        resource.assert_write_write_exclusive()
        resource.assert_read_write_exclusive()

    @pytest.mark.parametrize(*tmatrix({
        'write_time_cost': [0.7, 1.0],
        'thread_count': [3, 5],
    }))
    def test_write_concurrent(self, write_time_cost, thread_count):
        resource = SharedResource(write_time_cost=write_time_cost)

        def exclusive_write(writer_id: int):
            start = time.time()
            resource.write_data(writer_id, writer_id * 100)
            duration = time.time() - start
            log_message(f"Writer-{writer_id} time cost: {duration:.2f}秒")

        threads = []
        overall_start = time.time()

        for i in range(thread_count):
            thread = threading.Thread(
                target=exclusive_write,
                args=(i + 1,),
                name=f"ExclusiveWriter-{i + 1}"
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        overall_duration = time.time() - overall_start
        assert overall_duration == pytest.approx(write_time_cost * thread_count, abs=0.1)
        resource.assert_write_write_exclusive()
        resource.assert_read_write_exclusive()

    def test_complex_case(self):
        resource = SharedResource()
        threads = []

        for i in range(3):
            thread = threading.Thread(
                target=resource.read_data,
                args=(i + 1,),
                name=f"Reader-{i + 1}"
            )
            threads.append(thread)

        for i in range(5):
            thread = threading.Thread(
                target=resource.write_data,
                args=(i + 1, (i + 1) * 10),
                name=f"Writer-{i + 1}"
            )
            threads.append(thread)

        for i in range(2):
            thread = threading.Thread(
                target=resource.read_data,
                args=(i + 4,),
                name=f"Reader-{i + 4}"
            )
            threads.append(thread)

        random.shuffle(threads)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        resource.assert_write_write_exclusive()
        resource.assert_read_write_exclusive()

    def test_invalid_read_release_case_1(self):
        lock = ReadWriteLock()
        with pytest.raises(RuntimeError):
            lock.release_read()

    def test_invalid_read_release_case_2(self):
        lock = ReadWriteLock()
        lock.acquire_read()
        lock.acquire_read()
        lock.release_read()
        lock.release_read()
        with pytest.raises(RuntimeError):
            lock.release_read()
