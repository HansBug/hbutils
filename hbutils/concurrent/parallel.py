"""
Module for parallel execution utilities with bounded thread pool and progress tracking.

This module provides a bounded thread pool executor that limits both the number of worker threads
and pending tasks, along with a convenient parallel_call function for processing iterables in parallel
with progress tracking.

The bounded executor prevents memory issues when submitting large numbers of tasks by controlling
the maximum number of pending tasks in the queue using a semaphore mechanism.
"""

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import BoundedSemaphore
from typing import Iterable, Callable, Any, Optional

from ..logging import tqdm

__all__ = [
    'BoundedThreadPoolExecutor',
    'parallel_call',
]


class BoundedThreadPoolExecutor(ThreadPoolExecutor):
    """
    A ThreadPoolExecutor with bounded pending tasks using a semaphore.
    
    This executor extends the standard ThreadPoolExecutor to limit the number of pending
    tasks in the queue, preventing memory issues when submitting a large number of tasks.
    The semaphore mechanism ensures that task submission blocks when the pending task limit
    is reached, providing backpressure to prevent unbounded memory growth.
    
    :param max_workers: Maximum number of worker threads. Defaults to None.
    :type max_workers: Optional[int]
    :param max_pending: Maximum number of pending tasks. If None, no limit is applied.
    :type max_pending: Optional[int]
    :param kwargs: Additional keyword arguments passed to ThreadPoolExecutor.
    
    Example::
        >>> executor = BoundedThreadPoolExecutor(max_workers=4, max_pending=10)
        >>> future = executor.submit(lambda x: x * 2, 5)
        >>> result = future.result()
        >>> print(result)
        10
    """

    def __init__(self, max_workers: Optional[int] = None, max_pending: Optional[int] = None, **kwargs):
        """
        Initialize the BoundedThreadPoolExecutor.
        
        :param max_workers: Maximum number of worker threads.
        :type max_workers: Optional[int]
        :param max_pending: Maximum number of pending tasks. If None, no limit is applied.
        :type max_pending: Optional[int]
        :param kwargs: Additional keyword arguments for ThreadPoolExecutor.
        """
        super().__init__(max_workers=max_workers, **kwargs)
        if max_pending is not None:
            self._semaphore = BoundedSemaphore(max_pending)
        else:
            self._semaphore = None

    def submit(self, fn, *args, **kwargs):
        """
        Submit a callable to be executed with the given arguments.
        
        Acquires the semaphore before submitting to limit pending tasks. If the semaphore
        is at its limit, this call will block until a slot becomes available. The semaphore
        is released in the wrapper function after task completion.
        
        :param fn: The callable to execute.
        :type fn: Callable
        :param args: Positional arguments for the callable.
        :param kwargs: Keyword arguments for the callable.
        :return: A Future representing the pending execution.
        :rtype: Future
        :raises: Re-raises any exception that occurs during submission.
        
        Example::
            >>> executor = BoundedThreadPoolExecutor(max_workers=2, max_pending=5)
            >>> future = executor.submit(print, "Hello, World!")
            >>> future.result()
            Hello, World!
        """
        if self._semaphore:
            self._semaphore.acquire()
        try:
            future = super().submit(self._wrapper, fn, *args, **kwargs)
        except:
            if self._semaphore:
                self._semaphore.release()
            raise
        return future

    def _wrapper(self, fn, *args, **kwargs):
        """
        Wrapper function that executes the callable and releases the semaphore.
        
        This internal wrapper ensures that the semaphore is always released after task
        completion, regardless of whether the task succeeds or fails. This is critical
        for maintaining the correct semaphore count and preventing deadlocks.
        
        :param fn: The callable to execute.
        :type fn: Callable
        :param args: Positional arguments for the callable.
        :param kwargs: Keyword arguments for the callable.
        :return: The result of the callable execution.
        :raises: Re-raises any exception from the callable.
        """
        try:
            return fn(*args, **kwargs)
        finally:
            if self._semaphore:
                self._semaphore.release()


def parallel_call(iterable: Iterable, fn: Callable[[Any], None], total: Optional[int] = None,
                  desc: Optional[str] = None, max_workers: Optional[int] = None, max_pending: Optional[int] = None,
                  disable_tqdm: bool = False):
    """
    Execute a callable in parallel for each item in an iterable with progress tracking.
    
    This function processes items from an iterable in parallel using a bounded thread pool,
    displaying a progress bar and logging any errors that occur during processing. It provides
    a convenient high-level interface for parallel processing with automatic progress tracking
    and error handling.
    
    :param iterable: The iterable containing items to process.
    :type iterable: Iterable
    :param fn: The callable to execute for each item. Should accept a single argument.
    :type fn: Callable[[Any], None]
    :param total: Total number of items. If None, attempts to determine from iterable length.
    :type total: Optional[int]
    :param desc: Description for the progress bar. Defaults to a description with the function name.
    :type desc: Optional[str]
    :param max_workers: Maximum number of worker threads. Defaults to min(cpu_count, 16).
    :type max_workers: Optional[int]
    :param max_pending: Maximum number of pending tasks. If -1, no limit is applied. 
                        Defaults to max_workers * 5.
    :type max_pending: Optional[int]
    :param disable_tqdm: Whether to disable the progress bar. Defaults to False.
    :type disable_tqdm: bool
    
    Example::
        >>> def process_item(item):
        ...     print(f"Processing {item}")
        >>> parallel_call([1, 2, 3, 4, 5], process_item, desc="Processing items")
        Processing items: 100%|██████████| 5/5 [00:00<00:00, 10.00it/s]
        Processing 1
        Processing 2
        Processing 3
        Processing 4
        Processing 5
    """
    if total is None:
        try:
            total = len(iterable)
        except (TypeError, AttributeError):
            total = None

    pg = tqdm(total=total, desc=desc or f'Process with {fn!r}', disable=disable_tqdm)
    if not max_workers:
        max_workers = min(os.cpu_count(), 16)
    if max_pending == -1:
        max_pending = None
    elif not max_pending:
        max_pending = max_workers * 5
    tp = BoundedThreadPoolExecutor(max_workers=max_workers, max_pending=max_pending)

    def _fn(item):
        """
        Internal wrapper function that executes the callable and updates progress.
        
        This wrapper ensures that the progress bar is updated after each item is processed,
        and logs any exceptions that occur during processing before re-raising them.
        
        :param item: The item to process.
        :return: The result of fn(item).
        :raises: Re-raises any exception from fn after logging.
        """
        try:
            return fn(item)
        except Exception as err:
            logging.exception(f'Error when processing {item!r} - {err!r}')
            raise
        finally:
            pg.update()

    for item in iterable:
        tp.submit(_fn, item)

    tp.shutdown(wait=True)
