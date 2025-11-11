"""
Python system utilities module.

This module provides utilities for working with Python implementation details,
package management, and version information. It aggregates functionality from
three main submodules:

- implementation: Python implementation detection and information
- package: Package management and introspection utilities
- version: Python version parsing and comparison utilities

All public functions and classes from these submodules are re-exported at the
module level for convenient access.

Example::
    >>> from hbutils.system.python import get_python_version
    >>> version = get_python_version()
    >>> print(version)
    3.8.10
"""

from .implementation import *
from .package import *
from .version import *
