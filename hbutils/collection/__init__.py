"""
Overview:
    Collection module, include the basic utilities with collections like dict, list and tuple.
    
    This module provides a comprehensive set of utilities for working with various collection types
    in Python, including dictionaries, lists, tuples, and other sequence types. It includes functions
    for dimensional operations, functional programming patterns, data recovery, sequence manipulation,
    stacked operations, and structural transformations.
    
    The module is organized into several submodules:
    
    - dimension: Utilities for working with multi-dimensional data structures
    - functional: Functional programming utilities for collections
    - recover: Functions for recovering or reconstructing collection data
    - sequence: Sequence manipulation and processing utilities
    - stacked: Operations for stacked or nested collections
    - structural: Structural transformation and analysis utilities
    
    Example::
        >>> from hbutils.collection import unique, group_by
        >>> # Remove duplicates while preserving order
        >>> unique([1, 2, 2, 3, 1, 4])
        [1, 2, 3, 4]
        >>> # Group elements by criteria
        >>> group_by([1, 2, 3, 4, 5], lambda x: x % 2)
        {1: [1, 3, 5], 0: [2, 4]}
"""
from .dimension import *
from .functional import *
from .recover import *
from .sequence import *
from .stacked import *
from .structural import *
