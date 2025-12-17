"""
Overview:
    This module serves as the main entry point for the logging utilities package.
    It exports all functionality from the format and progress modules, which provide colored
    logging formatters and progress bar utilities for enhanced console output.

    The module re-exports all public members from the format submodule, including
    the ColoredFormatter class and Colors class for ANSI color formatting, as well
    as progress-related utilities from the progress submodule.

Example::
    >>> import logging
    >>> from hbutils.logging import ColoredFormatter
    >>> 
    >>> # Set up colored logging
    >>> logger = logging.getLogger()
    >>> logger.setLevel(logging.DEBUG)
    >>> console_handler = logging.StreamHandler()
    >>> console_handler.setFormatter(ColoredFormatter())
    >>> logger.addHandler(console_handler)
    >>> 
    >>> # Use the logger
    >>> logger.info("This is an info message")
    >>> logger.warning("This is a warning message")
    >>> logger.error("This is an error message")
"""

from .format import *
from .progress import *
