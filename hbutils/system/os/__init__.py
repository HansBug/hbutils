"""
Operating system utilities aggregated under :mod:`hbutils.system.os`.

This module provides a convenient namespace for OS-related helpers by
re-exporting public interfaces from two submodules:

* :mod:`hbutils.system.os.executable` - Executable detection utilities
* :mod:`hbutils.system.os.type` - Operating system type detection helpers

The module itself does not implement functionality directly. Instead, it
collects and re-exports the public symbols from the submodules above, so
consumers can import OS-related utilities from a single location.

Example::

    >>> from hbutils.system.os import is_windows, where
    >>> is_windows()
    False
    >>> where('python')
    ['/usr/bin/python', '/usr/local/bin/python']

.. note::
   The list of publicly available functions and classes depends on the
   exports defined in :mod:`hbutils.system.os.executable` and
   :mod:`hbutils.system.os.type`. Refer to those modules for detailed
   API documentation.

"""

from .executable import *
from .type import *
