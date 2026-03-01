"""
Scale unit utilities for IT-oriented size and time conversions.

This package module consolidates scale-related utilities that handle common
units used in the IT domain. It provides convenient access to functions and
classes implemented in the :mod:`hbutils.scale.size` and :mod:`hbutils.scale.time`
submodules, re-exporting their public APIs for direct use.

The module primarily supports:

* **Size units** - Bytes, Kilobytes, Megabytes, Gigabytes, etc.
* **Time units** - Seconds, Minutes, Hours, Days, etc.

.. note::
   All public members from the :mod:`hbutils.scale.size` and
   :mod:`hbutils.scale.time` modules are imported into this namespace
   for easier access.

Example::

    >>> from hbutils.scale import size_to_bytes
    >>> size_to_bytes('1KB')
    1024

"""
from .size import *
from .time import *
