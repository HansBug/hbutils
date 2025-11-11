"""
Overview:
    Design pattern module. Even in Python, design patterns are not emphasized like Java, \
    but some simple packages are often useful, such as singleton patterns.
    
    This module provides various design pattern implementations including:
    
    - Decorator pattern utilities
    - Final class/method decorators
    - Observer pattern implementation
    - Singleton pattern implementation

.. note::
    This module serves as the main entry point for the design pattern utilities,
    importing and exposing all public APIs from its submodules.

Examples::
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
