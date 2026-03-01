"""
Modeling utilities for data model construction and representation.

This package module provides a unified interface for a collection of model-related
utilities. It re-exports public symbols from several submodules that cover class
modeling helpers, comparison interfaces, enum utilities, raw value handling, and
representation helpers. Importing from :mod:`hbutils.model` allows consumers to
access these utilities in a single namespace.

The module re-exports the following submodules:

* :mod:`hbutils.model.clazz` - Class-building utilities and decorators
* :mod:`hbutils.model.compare` - Comparable interface and comparison helpers
* :mod:`hbutils.model.enum` - Enum-related helpers such as :class:`AutoIntEnum`
* :mod:`hbutils.model.raw` - Raw value wrapping and unwrapping helpers
* :mod:`hbutils.model.repr` - String representation utilities

Example::

    >>> from hbutils.model import AutoIntEnum, IComparable  # doctest: +SKIP
    >>> # Use AutoIntEnum for auto-incrementing enum values
    >>> # Use IComparable to simplify implementing comparison operations

.. note::
   This module only aggregates symbols from submodules. Refer to each submodule's
   documentation for detailed usage and API references.
"""
from .clazz import *
from .compare import *
from .enum import *
from .raw import *
from .repr import *
