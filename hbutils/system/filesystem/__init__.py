"""
Filesystem utilities for hbutils.system.

This module serves as the public aggregation point for filesystem-related
utilities in the :mod:`hbutils.system` package. It re-exports the public
functions and classes from submodules that provide binary file inspection,
directory management, general file operations, and temporary file utilities.

The following main components are re-exported from submodules:

* :class:`TemporaryDirectory` - Temporary directory creation with resilient cleanup

.. note::
   This module only re-exports public symbols from its submodules and does not
   implement filesystem operations directly. Refer to the specific submodules
   for detailed behavior.

Example::

    >>> from hbutils.system.filesystem import TemporaryDirectory
    >>> with TemporaryDirectory() as tmpdir:
    ...     # Use tmpdir for temporary operations
    ...     pass
"""
from .binary import *
from .directory import *
from .file import *
from .tempfile import *
