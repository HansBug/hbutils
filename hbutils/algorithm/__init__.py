"""
Algorithm utilities and data structures.

This package module serves as the public entry point for the
:mod:`hbutils.algorithm` namespace. It re-exports commonly used algorithmic
helpers from submodules to provide a convenient import surface. The primary
utilities include:

* :func:`linear_map` - Create piecewise linear mapping functions.
* :func:`topoids` - Perform topological sorting on integer-indexed nodes.
* :func:`topo` - Perform topological sorting on arbitrary hashable objects.

The concrete implementations live in the :mod:`hbutils.algorithm.linear` and
:mod:`hbutils.algorithm.topological` submodules, and are imported into this
namespace for easy access.

Example::

    >>> from hbutils.algorithm import linear_map, topo
    >>> mapping = linear_map([(0, 0), (1, 10)])
    >>> mapping(0.5)
    5.0
    >>> order = topo({'a': ['b'], 'b': []})
    >>> order
    ['b', 'a']

.. note::
   This module only re-exports public APIs from its submodules. Refer to the
   respective submodule documentation for detailed parameter and return type
   descriptions.

"""

from .linear import *
from .topological import *
