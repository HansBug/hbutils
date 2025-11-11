"""
Operating System Utilities Module.

This module provides utilities for operating system operations, including executable detection and OS type identification.

The module exports functionality from two submodules:

- executable: Functions for detecting and working with executable files in the system PATH
- type: Functions for identifying operating system types (Linux, Windows, macOS)

This serves as a convenience module that aggregates OS-related utilities into a single namespace,
allowing users to import all OS-related functionality from a single location.

Example::
    >>> from hbutils.system.os import is_windows, where
    >>> is_windows()
    False
    >>> where('python')
    ['/usr/bin/python', '/usr/local/bin/python']
"""

from .executable import *
from .type import *
