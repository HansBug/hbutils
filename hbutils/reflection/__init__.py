"""
Overview:
    Reflection module, include some useful utilities for the python language.
    
    This module provides a collection of reflection utilities for Python, including:
    
    - Class inspection and manipulation utilities (from :mod:`hbutils.reflection.clazz`)
    - Context management utilities (from :mod:`hbutils.reflection.context`)
    - Exception handling utilities (from :mod:`hbutils.reflection.exception`)
    - Function inspection and manipulation utilities (from :mod:`hbutils.reflection.func`)
    - Import utilities (from :mod:`hbutils.reflection.imports`)
    - Iterator utilities (from :mod:`hbutils.reflection.iter`)
    - Module inspection utilities (from :mod:`hbutils.reflection.module`)
    
    All utilities are exposed at the package level through wildcard imports from their
    respective submodules, providing a convenient single import point for reflection operations.
    
    Example::
        >>> from hbutils.reflection import context, dynamic_call, mount_pythonpath
        >>> # Use context management
        >>> with context().vars(debug=True):
        ...     print(context().get('debug'))
        True
        >>> # Use dynamic function calling
        >>> def func(a, b=2):
        ...     return a + b
        >>> dynamic_call(func, {'a': 1, 'b': 3, 'c': 4})  # 'c' is ignored
        4
"""
from .clazz import *
from .context import *
from .exception import *
from .func import *
from .imports import *
from .iter import *
from .module import *
