"""
System utilities module for hbutils.

This module provides a comprehensive collection of system-level utilities including:

- **filesystem**: File and directory operations, binary file handling, and temporary file management
- **git**: Git repository information and operations
- **network**: Network-related utilities including host management, port operations, telnet functionality, and URL handling
- **os**: Operating system utilities for executable management and OS type detection
- **python**: Python environment utilities including implementation detection, package management, and version handling

The module aggregates functionality from multiple submodules to provide a unified interface
for common system-level operations in Python applications.

Example::
    >>> from hbutils.system import *
    >>> # Use various system utilities
"""

from .filesystem import *
from .git import *
from .network import *
from .os import *
from .python import *
