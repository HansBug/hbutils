"""
Concurrent programming utilities package.

This package exposes convenience imports that aggregate functionality from
the :mod:`hbutils.concurrent.parallel` and :mod:`hbutils.concurrent.readwrite`
modules. It is designed to provide a unified namespace for concurrency tools,
including bounded thread pool execution helpers and read-write lock utilities.

The package re-exports public members from the following modules:

* :mod:`hbutils.concurrent.parallel` - Thread pool executors and parallel helpers
* :mod:`hbutils.concurrent.readwrite` - Read-write locking utilities

.. note::
   This module only re-exports public symbols from its submodules. Refer to the
   respective module documentation for full details and usage patterns.

Example::

    >>> from hbutils.concurrent import BoundedThreadPoolExecutor
    >>> with BoundedThreadPoolExecutor(max_workers=2, max_pending=4) as executor:
    ...     future = executor.submit(lambda x: x + 1, 1)
    ...     future.result()
    2
"""

from .parallel import *
from .readwrite import *
