"""
Overview:
    Algorithm module, including the generic implementation of some useful algorithms and data structures.
    
    This module provides various algorithmic utilities including:

    - Linear algorithms and data structures (piecewise linear mapping functions)
    - Topological sorting and related algorithms

    The module serves as a central import point for algorithm-related functionality,
    exposing implementations from submodules for convenient access.

    Exported Functions:
        - :func:`linear_map`: Creates piecewise linear mapping functions
        - :func:`topoids`: Performs topological sort on integer-indexed nodes
        - :func:`topo`: Performs topological sort on arbitrary objects
"""
from .linear import *
from .topological import *
