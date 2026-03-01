"""
Native expression utilities for the :mod:`hbutils.expression` package.

This module aggregates and re-exports the public APIs from the native
expression submodules, providing a convenient entry point for users who want
to access the entire native expression toolkit in a single import.

The following public modules are re-exported:

* :mod:`hbutils.expression.native.base` - Base expression classes and utilities
* :mod:`hbutils.expression.native.feature` - Feature-related expression components
* :mod:`hbutils.expression.native.general` - General-purpose expression utilities

This design allows users to write expressive and compact imports while keeping
the internal organization modular.

Example::

    >>> from hbutils.expression.native import *
    >>> # You now have access to public classes and functions
    >>> # defined in base, feature, and general submodules.
"""

from .base import *
from .feature import *
from .general import *
