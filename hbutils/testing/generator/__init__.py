"""
Test case generation utilities for combinatorial and matrix-based testing.

This module exposes the public generator classes and functional helpers used to
create test cases for unit tests, parameterized testing, and combinatorial
coverage. It aggregates the most commonly used generators and utilities from
submodules into a single import location.

The module contains the following main components:

* :class:`BaseGenerator` - Abstract base class for generator implementations
* :class:`MatrixGenerator` - Cartesian product generator with include/exclude rules
* :class:`AETGGenerator` - AETG-based generator for pairwise/tuple coverage
* :func:`tmatrix` - Functional helper for generating a full matrix of cases

Example::

    >>> from hbutils.testing.generator import MatrixGenerator, AETGGenerator, tmatrix
    >>>
    >>> # Matrix-based generation with exclusions
    >>> gen = MatrixGenerator(
    ...     {'a': [1, 2], 'b': ['x', 'y']},
    ...     excludes=[{'a': 1, 'b': 'x'}]
    ... )
    >>> list(gen.cases())
    [{'a': 1, 'b': 'y'}, {'a': 2, 'b': 'x'}, {'a': 2, 'b': 'y'}]
    >>>
    >>> # AETG-based generation for pairwise coverage
    >>> aetg = AETGGenerator({'a': (1, 2), 'b': (3, 4), 'c': (5, 6)}, rnd=0)
    >>> next(aetg.cases())  # doctest: +ELLIPSIS
    {'a': 1, 'b': 3, 'c': 5}
    >>>
    >>> # Functional helper producing a matrix of tuple cases
    >>> tmatrix({'a': [1, 2], 'b': ['x', 'y']})
    [(1, 'x'), (1, 'y'), (2, 'x'), (2, 'y')]

.. note::
   Only public symbols listed in :data:`__all__` are intended for direct import
   from this module.

"""

from .aetg import AETGGenerator
from .base import BaseGenerator
from .func import *
from .func import __all__ as _func_all
from .matrix import MatrixGenerator

__all__ = [
    'BaseGenerator', 'MatrixGenerator', 'AETGGenerator',
    *_func_all,
]
