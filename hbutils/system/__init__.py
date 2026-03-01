"""
System utilities package for hbutils.

This package provides a unified interface to a collection of system-level utilities,
organizing common functionality across filesystem, git, network, OS, and Python
environment operations. It re-exports public objects from the submodules so they
can be accessed directly under :mod:`hbutils.system`.

The package aggregates the following submodules:

* :mod:`hbutils.system.filesystem` - File and directory helpers, binary utilities, and temporary file handling
* :mod:`hbutils.system.git` - Git repository inspection and operations
* :mod:`hbutils.system.network` - Networking helpers including host/port utilities and URL handling
* :mod:`hbutils.system.os` - Operating system helpers such as executable discovery and OS type detection
* :mod:`hbutils.system.python` - Python runtime utilities and package/environment helpers

Example::

    >>> from hbutils.system import *
    >>> # Use utilities exposed by the submodules
    >>> # e.g., urlsplit from the network submodule (if exported there)
    >>> # split_url = urlsplit('https://example.com/path?q=1')

.. note::
   This package is a convenience re-exporter. Public objects are defined in
   the underlying submodules and imported into this namespace.

"""

from .filesystem import *
from .git import *
from .network import *
from .os import *
from .python import *
