"""
Utilities for isolating and mocking :mod:`logging` handlers in tests.

This module offers a context manager to temporarily replace the handler list of
a logger, allowing tests or debugging sessions to capture and redirect log
output in an isolated environment. When the context exits, the original logger
state is restored automatically, optionally closing any handlers installed
during isolation.

The module contains the following main component:

* :func:`isolated_logger` - Context manager for temporarily replacing a logger's
  handlers.

.. note::
   The isolated logger operates on the same logger instance and mutates its
   handler list in-place. Use it carefully when multiple threads may access
   the same logger.

Example::

    >>> import logging
    >>> from hbutils.testing.isolated.logging import isolated_logger
    >>> from logging import StreamHandler
    >>>
    >>> logging.error('before isolation')
    ERROR:root:before isolation
    >>> with isolated_logger(handlers=[StreamHandler()]) as lg:
    ...     lg.error('inside isolation')
    inside isolation
    >>> logging.error('after isolation')
    ERROR:root:after isolation

"""

import logging
from contextlib import contextmanager
from typing import Optional, Union, List, Iterator

from ...collection.recover import get_recovery_func

__all__ = [
    'isolated_logger',
]


@contextmanager
def isolated_logger(logger: Optional[Union[str, logging.Logger]] = None,
                    handlers: Optional[List[logging.Handler]] = None,
                    close_handlers: bool = True) -> Iterator[logging.Logger]:
    """
    Context manager for temporarily isolating and mocking loggers.

    This function allows you to temporarily replace a logger's handlers with
    custom ones and automatically restores the original handlers when exiting
    the context. This is particularly useful for testing or debugging
    scenarios where you need to capture or redirect log output.

    :param logger: Logger instance or logger name for isolation. If ``None``,
        the root logger is used.
    :type logger: Optional[Union[str, logging.Logger]]
    :param handlers: Initial handlers to use during isolation. If ``None``,
        an empty list is used.
    :type handlers: Optional[List[logging.Handler]]
    :param close_handlers: Whether to close handlers after exiting the context.
        Defaults to ``True``.
    :type close_handlers: bool
    :return: Iterator yielding the isolated logger instance.
    :rtype: Iterator[logging.Logger]

    .. note::
       The handler list is replaced in-place; existing handlers are restored
       after the context exits.

    .. warning::
       When ``close_handlers`` is ``True``, all handlers currently attached to
       the logger at context exit are closed.

    Examples::

        >>> import logging
        >>> from rich.logging import RichHandler  # a 3rd-party logger
        >>> from hbutils.testing.isolated.logging import isolated_logger
        >>>
        >>> logging.error('this is error')  # normal log
        ERROR:root:this is error
        >>> logging.error('this is error')
        ERROR:root:this is error
        >>>
        >>> with isolated_logger(handlers=[
        ...     RichHandler(),
        ...     logging.FileHandler('test_log.txt'),
        ... ]):
        ...     logging.error('this is error inside 1')
        ...     logging.error('this is error inside 2')
        [11/08/22 15:39:37] ERROR    this is error inside 1                    <stdin>:5
                            ERROR    this is error inside 2                    <stdin>:6
        >>>
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
