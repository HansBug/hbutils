"""
This module provides utilities for isolating and mocking loggers in the `logging` module.

It allows temporary replacement of logger handlers for testing or debugging purposes,
with automatic restoration of the original logger state after use.
"""

import logging
from contextlib import contextmanager
from typing import Optional, Union, List

from ...collection.recover import get_recovery_func

__all__ = [
    'isolated_logger',
]


@contextmanager
def isolated_logger(logger: Optional[Union[str, logging.Logger]] = None,
                    handlers: Optional[List[logging.Handler]] = None,
                    close_handlers: bool = True):
    """
    Context manager for temporarily isolating and mocking loggers in the `logging` module.

    This function allows you to temporarily replace a logger's handlers with custom ones,
    and automatically restores the original handlers when exiting the context. This is
    particularly useful for testing or debugging scenarios where you need to capture or
    redirect log output.

    :param logger: Logger instance or logger name for isolation. If None, uses the root logger.
    :type logger: Optional[Union[str, logging.Logger]]
    :param handlers: Initial handlers to use during isolation. If None, uses an empty list.
    :type handlers: Optional[List[logging.Handler]]
    :param close_handlers: Whether to close handlers after exiting the context. Defaults to True.
    :type close_handlers: bool

    :yield: The isolated logger instance.
    :rtype: logging.Logger

    Examples::
        >>> import logging
        >>> from rich.logging import RichHandler  # a 3rd-party logger
        >>> from hbutils.testing import isolated_logger
        >>>
        >>> logging.error('this is error')  # normal log
        ERROR:root:this is error
        >>> logging.error('this is error')
        ERROR:root:this is error

        >>> with isolated_logger(handlers=[  # replaced with custom handlers
        ...     RichHandler(),
        ...     logging.FileHandler('test_log.txt'),
        ... ]):
        ...     logging.error('this is error inside 1')
        ...     logging.error('this is error inside 2')
        [11/08/22 15:39:37] ERROR    this is error inside 1                    <stdin>:5
                            ERROR    this is error inside 2                    <stdin>:6

        >>> logging.error('this is error')  # change back to normal log
        ERROR:root:this is error
        >>> logging.error('this is error')
        ERROR:root:this is error

    """
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)
    handlers = list(handlers or [])

    rf = get_recovery_func(logger)
    try:
        logger.handlers[:] = handlers[:]
        yield logger
    finally:
        if close_handlers:
            for handler in logger.handlers:
                handler.close()
        rf()
