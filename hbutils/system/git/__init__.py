"""
This module provides functionality for checking and retrieving information about Git and Git LFS installations.

It includes functions to:

1. Check if Git is installed and get its version information.
2. Check if Git LFS is installed and get its version information.
3. Cache the results of these checks for improved performance.

The module uses subprocess to run Git commands and parse their output, providing detailed information about
the Git and Git LFS installations on the system.
"""

from .info import *
