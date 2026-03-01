"""
Expression utilities for the :mod:`hbutils.expression` package.

This module serves as the public entry point for the expression system and
re-exports all public symbols from :mod:`hbutils.expression.native`. It provides
a unified namespace for working with expression objects, including feature-based
operator handling and general expression construction utilities.

The module primarily exposes the following public capabilities via the native
submodule:

* Base expression classes and interfaces
* Feature-based expression handling (e.g., arithmetic, logical, bitwise)
* General expression utilities and helpers

.. note::
   All public symbols are imported from :mod:`hbutils.expression.native`. Refer
   to the native module for detailed API documentation.

Example::

    >>> from hbutils.expression import *
    >>> # Use expression utilities provided by the native module

"""

from .native import *
