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
    Overview:
        Mock loggers in `logging` module.

    :param logger: Logger or logger's name for isolation.
    :param handlers: Initial handlers for isolation.
    :param close_handlers: Close handler's after complete.

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
