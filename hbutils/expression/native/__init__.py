"""
This module provides native expression utilities for the hbutils library.

It aggregates and exports functionalities from three main submodules:

- base: Base expression classes and utilities
- feature: Feature-related expression components
- general: General-purpose expression utilities

This module serves as a convenient entry point to access all native expression
functionalities without needing to import from individual submodules.

Example::
    >>> from hbutils.expression.native import *
    >>> # Now you can use all exported classes and functions from base, feature, and general
"""

from .base import *
from .feature import *
from .general import *
