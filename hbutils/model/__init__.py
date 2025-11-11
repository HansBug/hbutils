"""
Overview:
    Modeling module, includes useful utilities for building data models.
    
    This module provides various utilities for creating and managing data models,
    including class utilities, comparison operations, enum handling, raw data processing,
    and representation utilities.
    
    The module exports functionality from the following submodules:
    
    - clazz: Utilities for building class models with decorators for field access,
      visual representation, constructors, hash/equality operations, and property accessors
    - compare: Base interface for implementing comparable objects with comparison operations
    - enum: Utilities for working with Python enum classes, including AutoIntEnum and
      int_enum_loads decorator
    - raw: Support for wrapping and unwrapping raw values based on conditions
    - repr: Utilities for generating string representations of custom classes
    
    Example::
        >>> from hbutils.model import IComparable, AutoIntEnum, int_enum_loads
        >>> # Use IComparable for easy comparison implementation
        >>> # Use AutoIntEnum for auto-incrementing integer enums
        >>> # Use int_enum_loads for flexible enum parsing
"""
from .clazz import *
from .compare import *
from .enum import *
from .raw import *
from .repr import *
