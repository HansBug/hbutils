"""
Collection utilities for dictionary, list, tuple, and nested sequence operations.

This package module aggregates public utilities from several collection-focused
submodules, providing a single import location for common collection helpers.
It re-exports functions, classes, and constants from the following modules:

* :mod:`hbutils.collection.dimension` - Dimensional and shape-related utilities
* :mod:`hbutils.collection.functional` - Functional programming helpers
* :mod:`hbutils.collection.recover` - Collection recovery and reconstruction tools
* :mod:`hbutils.collection.sequence` - Sequence manipulation utilities
* :mod:`hbutils.collection.stacked` - Stacked or nested collection operations
* :mod:`hbutils.collection.structural` - Structural transformation helpers

.. note::
   This module is an aggregation layer only. Refer to the underlying submodules
   for detailed documentation of each function or class.

Example::

    >>> from hbutils.collection import unique, group_by
    >>> unique([1, 2, 2, 3, 1, 4])
    [1, 2, 3, 4]
    >>> group_by([1, 2, 3, 4, 5], lambda x: x % 2)
    {1: [1, 3, 5], 0: [2, 4]}

"""
from .dimension import *
from .functional import *
from .recover import *
from .sequence import *
from .stacked import *
from .structural import *
