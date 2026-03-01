"""
Single-file processing utilities and stream helpers.

This module serves as the public entry point for file-related functionality in
:mod:`hbutils.file`. It re-exports utilities from the :mod:`hbutils.file.stream`
submodule, providing a convenient import surface for single-file operations.

If you need to operate on filesystems (e.g., directory operations, path
manipulations), see :mod:`hbutils.system.filesystem` instead.

The module focuses on operations that target a single file rather than
filesystem-level tasks.

.. note::
   This module focuses on single file operations. For filesystem-level
   operations, refer to the filesystem utilities in
   :mod:`hbutils.system.filesystem`.

Example::

    >>> from hbutils.file import *
    >>> # Use stream utilities for file operations
"""
from .stream import *
