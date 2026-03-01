"""
Design pattern utilities for the :mod:`hbutils.design` package.

This package provides lightweight, Pythonic implementations of several classic
design patterns. It acts as a convenience entry point that re-exports all public
APIs from its submodules, allowing consumers to import from :mod:`hbutils.design`
directly.

The package includes the following public components:

* :class:`FinalMeta` - Metaclass that prevents class inheritance (final class)
* :class:`SingletonMeta` - Metaclass implementing the singleton pattern
* Decorator helpers from :mod:`hbutils.design.decorator`
* Observer pattern utilities from :mod:`hbutils.design.observer`

.. note::
   This module is an aggregation layer that imports and exposes public objects
   from its submodules. Refer to each submodule for detailed behavior and API
   specifics.

Example::

    >>> from hbutils.design import SingletonMeta
    >>> class MyClass(metaclass=SingletonMeta):
    ...     pass
    >>> instance1 = MyClass()
    >>> instance2 = MyClass()
    >>> instance1 is instance2
    True
"""
from .decorator import *
from .final import *
from .observer import *
from .singleton import *
