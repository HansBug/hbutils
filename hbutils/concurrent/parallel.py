"""
Parallel execution utilities with bounded thread pools and progress tracking.

This module provides tools for executing tasks in parallel while controlling the
number of pending tasks and optionally displaying progress information. It is
designed to prevent memory pressure that can arise from submitting too many
tasks at once by using a bounded queue mechanism implemented via a semaphore.

The module contains the following public components:

* :class:`BoundedThreadPoolExecutor` - A thread pool executor that limits the
  number of pending tasks using a semaphore.
* :func:`parallel_call` - High-level helper for parallel processing of an
  iterable with progress reporting and exception logging.

.. note::
   The progress display relies on :func:`hbutils.logging.tqdm`, which provides
   a tqdm-compatible interface and falls back to a lightweight progress bar if
   the real tqdm package is unavailable.

Example::

    >>> from hbutils.concurrent.parallel import parallel_call
    >>> def square(x):
    ...     return x * x
    >>> parallel_call(range(5), square, desc="Squaring")
    Squaring: 100%|██████████| 5/5 [00:00<00:00, ...it/s]

"""

import logging
import os
from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing import BoundedSemaphore
from typing import Any, Callable, Iterable, Optional

from ..logging import tqdm

__all__ = [
    'BoundedThreadPoolExecutor',
    'parallel_call',
]


class BoundedThreadPoolExecutor(ThreadPoolExecutor):
    """
    A :class:`~concurrent.futures.ThreadPoolExecutor` with bounded pending tasks.

    This executor extends :class:`~concurrent.futures.ThreadPoolExecutor` to
    limit the number of pending tasks in the queue. The limit is enforced by a
    semaphore that blocks submission when the maximum number of pending tasks
    is reached, providing backpressure to avoid unbounded memory growth.

    :param max_workers: Maximum number of worker threads. Defaults to ``None``.
    :type max_workers: Optional[int]
    :param max_pending: Maximum number of pending tasks. If ``None``, no limit
        is applied.
    :type max_pending: Optional[int]
    :param kwargs: Additional keyword arguments passed to
        :class:`~concurrent.futures.ThreadPoolExecutor`.
    :type kwargs: Any

    Example::

        >>> executor = BoundedThreadPoolExecutor(max_workers=4, max_pending=10)
        >>> future = executor.submit(lambda x: x * 2, 5)
        >>> future.result()
        10
    """

    def __init__(
        self,
        max_workers: Optional[int] = None,
        max_pending: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the bounded thread pool executor.

        :param max_workers: Maximum number of worker threads.
        :type max_workers: Optional[int]
        :param max_pending: Maximum number of pending tasks. If ``None``, no
            limit is applied.
        :type max_pending: Optional[int]
        :param kwargs: Additional keyword arguments for
            :class:`~concurrent.futures.ThreadPoolExecutor`.
        :type kwargs: Any
        """
        super().__init__(max_workers=max_workers, **kwargs)
        if max_pending is not None:
            self._semaphore: Optional[BoundedSemaphore] = BoundedSemaphore(max_pending)
        else:
            self._semaphore = None

    def submit(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
        """
        Submit a callable to be executed with the given arguments.

        This method acquires the semaphore before submitting the task to limit
        the number of pending tasks. If the pending task limit is reached,
        submission blocks until a slot becomes available. The semaphore is
        released after task completion in an internal wrapper.

        :param fn: The callable to execute.
        :type fn: Callable[..., Any]
        :param args: Positional arguments for the callable.
        :type args: Any
        :param kwargs: Keyword arguments for the callable.
        :type kwargs: Any
        :return: A future representing the pending execution.
        :rtype: concurrent.futures.Future
        :raises Exception: Re-raises any exception that occurs during submission.

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
        except Exception:
            if self._semaphore:
                self._semaphore.release()
            raise
        return future

    def _wrapper(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Execute the callable and release the semaphore.

        This internal wrapper ensures that the semaphore is released after task
        completion, regardless of success or failure.

        :param fn: The callable to execute.
        :type fn: Callable[..., Any]
        :param args: Positional arguments for the callable.
        :type args: Any
        :param kwargs: Keyword arguments for the callable.
        :type kwargs: Any
        :return: The result of the callable execution.
        :rtype: Any
        :raises Exception: Re-raises any exception from the callable.
        """
        try:
            return fn(*args, **kwargs)
        finally:
            if self._semaphore:
                self._semaphore.release()


def parallel_call(
    iterable: Iterable[Any],
    fn: Callable[[Any], Any],
    total: Optional[int] = None,
    desc: Optional[str] = None,
    max_workers: Optional[int] = None,
    max_pending: Optional[int] = None,
    disable_tqdm: bool = False,
) -> None:
    """
    Execute a callable in parallel for each item in an iterable with progress tracking.

    This function processes items in parallel using a bounded thread pool,
    displays a progress bar, and logs any exceptions that occur during
    processing before re-raising them.

    :param iterable: The iterable containing items to process.
    :type iterable: Iterable[Any]
    :param fn: The callable to execute for each item. It should accept a single
        argument.
    :type fn: Callable[[Any], Any]
    :param total: Total number of items. If ``None``, attempts to determine
        the length from the iterable.
    :type total: Optional[int]
    :param desc: Description for the progress bar. Defaults to a description
        that includes the function representation.
    :type desc: Optional[str]
    :param max_workers: Maximum number of worker threads. Defaults to
        ``min(os.cpu_count(), 16)``.
    :type max_workers: Optional[int]
    :param max_pending: Maximum number of pending tasks. If ``-1``, no limit is
        applied. Defaults to ``max_workers * 5``.
    :type max_pending: Optional[int]
    :param disable_tqdm: Whether to disable the progress bar.
    :type disable_tqdm: bool
    :return: This function does not return a value.
    :rtype: None
    :raises Exception: Re-raises exceptions from the worker callable after
        logging them.

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
            total = len(iterable)  # type: ignore[arg-type]
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

    def _fn(item: Any) -> Any:
        """
        Execute the callable for a single item and update progress.

        This wrapper logs any exceptions that occur during processing before
        re-raising them and always updates the progress bar.

        :param item: The item to process.
        :type item: Any
        :return: The result of ``fn(item)``.
        :rtype: Any
        :raises Exception: Re-raises any exception from ``fn`` after logging.
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
