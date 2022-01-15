"""
Overview:
    Scale unit module, include some useful utilities for the units in IT area, such as memory unit (MB/KB/B) \
    and time unit (h/m/s).
"""
from .size import size_to_bytes, size_to_bytes_str
from .time import time_to_duration, time_to_delta_str
