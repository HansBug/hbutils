"""
Overview:
    This module serves as the main entry point for the logging utilities package.
    It exports all functionality from the format module, which provides colored
    logging formatters and related utilities for enhanced console output.

    The module re-exports all public members from the format submodule, including
    the ColoredFormatter class and Colors class for ANSI color formatting.

Example::
    >>> import logging
    >>> from hbutils.logging import ColoredFormatter
    >>> 
    >>> logger = logging.getLogger()
    >>> logger.setLevel(logging.DEBUG)
    >>> console_handler = logging.StreamHandler()
    >>> console_handler.setFormatter(ColoredFormatter())
    >>> logger.addHandler(console_handler)
    >>> 
    >>> # Test single line message
    >>> logger.info("This is a single line message")
    >>> # Test multi-line message
    >>> logger.warning("This is a multi-line message:\\nLine 2 content\\nLine 3 content\\nLine 4 content")
"""

from .format import *
