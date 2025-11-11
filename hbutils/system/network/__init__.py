"""
Overview:
    This module provides useful tools for network operations, including:
    
    - Host management utilities
    - Port utilities for network connections
    - Telnet connection helpers
    - URL parsing and manipulation tools
    
    All utilities are imported and exposed at the package level for convenient access.

Main Components:

    - Host file management and localhost IP retrieval
    - Port availability checking and allocation
    - Telnet-like connectivity checks
    - URL parsing and splitting utilities

The module aggregates functionality from multiple submodules to provide a comprehensive
set of network-related utilities for common tasks such as checking port availability,
parsing URLs, managing host files, and testing network connectivity.
"""
from .hosts import *
from .port import *
from .telnet_ import *
from .url import *
