"""
This module provides utilities for operating system operations, including executable detection and OS type identification.

The module exports functionality from two submodules:
- executable: Functions for detecting and working with executable files
- type: Functions for identifying operating system types

This serves as a convenience module that aggregates OS-related utilities into a single namespace.
"""

from .executable import *
from .type import *
