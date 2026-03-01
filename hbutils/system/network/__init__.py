"""
Network utility package aggregating common system-level networking helpers.

This package exposes a unified interface to several network-related utilities
implemented in its submodules. It re-exports public APIs from the following
modules for convenience:

* :mod:`hbutils.system.network.hosts` - Host file management and lookup helpers
* :mod:`hbutils.system.network.port` - Port availability and allocation tools
* :mod:`hbutils.system.network.telnet_` - Telnet-like connectivity checks
* :mod:`hbutils.system.network.url` - URL parsing and manipulation utilities

The main goal of this package is to provide a centralized access point for
network operations commonly used in system scripts, diagnostics, and tooling.

.. note::
   The package re-exports public symbols from its submodules. You may also
   import the submodules directly if you need module-scoped names.

Example::

    >>> import hbutils.system.network as network
    >>> network.__name__
    'hbutils.system.network'

"""
from .hosts import *
from .port import *
from .telnet_ import *
from .url import *
