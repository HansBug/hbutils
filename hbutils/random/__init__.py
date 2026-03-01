"""
Random utilities package for generating binary data, sequences, strings, and
managing random state.

This package aggregates the random-related utilities from the following
modules:

* :mod:`hbutils.random.binary` - Binary data generators
* :mod:`hbutils.random.sequence` - Sequence generation and shuffling helpers
* :mod:`hbutils.random.state` - Random state management utilities
* :mod:`hbutils.random.string` - String generation utilities

The package serves as a central import point for random-related functionality
in the :mod:`hbutils` namespace.

Example::

    >>> from hbutils.random import random_bytes, random_shuffle, keep_global_state
    >>> # Generate random bytes
    >>> data = random_bytes(16)
    >>> # Shuffle a sequence
    >>> items = [1, 2, 3, 4, 5]
    >>> shuffled = random_shuffle(items)
    >>> # Manage random state
    >>> with keep_global_state():
    ...     # Random operations here will not affect global state
    ...     pass
"""
from .binary import *
from .sequence import *
from .state import *
from .string import *
