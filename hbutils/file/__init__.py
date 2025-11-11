"""
Overview:
    Utilities for processing single files.

    This module provides utilities for file processing operations. It serves as the main entry point
    for file-related functionality by importing and exposing utilities from the stream submodule.

    If you need to operate on filesystems (e.g., directory operations, path manipulations),
    see ``hbutils.system.filesystem`` instead.

Note:
    This module focuses on single file operations. For filesystem-level operations,
    refer to the filesystem utilities in ``hbutils.system.filesystem``.

Example::
    >>> from hbutils.file import *
    >>> # Use stream utilities for file operations
"""
from .stream import *
