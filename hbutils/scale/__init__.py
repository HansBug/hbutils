"""
Overview:
    Scale unit module, include some useful utilities for the units in IT area, such as memory unit (MB/KB/B) \
    and time unit (h/m/s).

This module provides utilities for handling and converting various scale units commonly used in IT:

- **Size units**: Bytes, Kilobytes, Megabytes, Gigabytes, etc.
- **Time units**: Seconds, Minutes, Hours, Days, etc.

The module exports all functions and classes from its submodules for convenient access.
"""
from .size import *
from .time import *
