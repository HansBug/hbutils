"""
Text comparison utilities for testing purposes.

This module serves as the public entry point for the text comparison
functionality in :mod:`hbutils.testing.compare`. It re-exports the public
API of the :mod:`hbutils.testing.compare.text` submodule, offering tools
for aligning and comparing text content in test assertions.

The module contains the following main components:

* :class:`TextAligner` - Text alignment and comparison utility for tests

Example::

    >>> from hbutils.testing.compare import TextAligner
    >>> aligner = TextAligner()
    >>> aligner.assert_equal("Hello", "Hello")
"""

from .text import *
