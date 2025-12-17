"""
Module for concurrent programming utilities.

This module provides utilities for concurrent and parallel execution, including:

- Bounded thread pool executor with task queue limits
- Parallel execution with progress tracking
- Read-write lock implementation for shared resource access control

The module combines functionality from parallel and readwrite submodules to provide
a comprehensive set of tools for managing concurrent operations in Python applications.
"""

from .parallel import *
from .readwrite import *
