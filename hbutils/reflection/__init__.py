"""
Reflection utility package for Python introspection and runtime manipulation.

This package aggregates a set of reflection-related utilities from multiple
submodules into a single import point. The public API is re-exported via
wildcard imports, allowing users to access functions and classes directly from
:mod:`hbutils.reflection`.

The package exposes functionality from these modules:

* :mod:`hbutils.reflection.clazz` - Class inspection and manipulation helpers
* :mod:`hbutils.reflection.context` - Context management utilities
* :mod:`hbutils.reflection.exception` - Exception handling helpers
* :mod:`hbutils.reflection.func` - Function inspection and invocation helpers
* :mod:`hbutils.reflection.imports` - Import-related utilities
* :mod:`hbutils.reflection.iter` - Iterator utilities
* :mod:`hbutils.reflection.module` - Module inspection utilities

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

.. note::
   This package module re-exports symbols from its submodules, so the exact
   set of available utilities depends on the implementations of those modules.
"""
from .clazz import *
from .context import *
from .exception import *
from .func import *
from .imports import *
from .iter import *
from .module import *
