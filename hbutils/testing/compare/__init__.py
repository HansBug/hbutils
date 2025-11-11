"""
Text comparison utilities for testing purposes.

This module serves as the main entry point for text comparison functionality,
re-exporting all utilities from the text submodule. It provides tools for
comparing and validating text content in various formats and contexts,
particularly useful in unit testing scenarios.

The module includes the :class:`TextAligner` class and related utilities
for flexible text comparison, preprocessing, and alignment operations.

Example::
    >>> from hbutils.testing.compare import TextAligner
    >>> aligner = TextAligner()
    >>> # Use aligner for text comparison in tests
"""

from .text import *
