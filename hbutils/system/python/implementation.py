"""
This module provides utilities for detecting the Python implementation being used.

It defines an enumeration of common Python implementations (CPython, IronPython, Jython, PyPy)
and provides convenience functions to check which implementation is currently running.
The detection is based on the platform module's python_implementation() function and
results are cached for performance.

Example::
    >>> from hbutils.system.python.implementation import is_cpython, is_pypy
    >>> if is_cpython():
    ...     print("Running on CPython")
    >>> if is_pypy():
    ...     print("Running on PyPy")
"""

import platform
from enum import IntEnum, unique
from functools import lru_cache

from ...model import int_enum_loads

__all__ = [
    'is_cpython',
    'is_ironpython',
    'is_jython',
    'is_pypy',
]


@int_enum_loads(name_preprocess=str.upper)
@unique
class PythonImplementation(IntEnum):
    """
    Enumeration of Python implementations.
    
    This enum represents the different Python implementations that can be detected.
    The enum values are loaded from string names (case-insensitive) via the 
    int_enum_loads decorator.
    
    :cvar CPYTHON: The standard CPython implementation.
    :cvar IRONPYTHON: The IronPython implementation (.NET-based).
    :cvar JYTHON: The Jython implementation (JVM-based).
    :cvar PYPY: The PyPy implementation (JIT-compiled).
    """
    CPYTHON = 1
    IRONPYTHON = 2
    JYTHON = 3
    PYPY = 4


@lru_cache()
def _get_python_implementation() -> PythonImplementation:
    """
    Get the current Python implementation.
    
    This function detects the Python implementation using platform.python_implementation()
    and converts it to a PythonImplementation enum value. The result is cached for
    performance since the implementation cannot change during runtime.
    
    :return: The detected Python implementation.
    :rtype: PythonImplementation
    
    Example::
        >>> impl = _get_python_implementation()
        >>> print(impl)
        PythonImplementation.CPYTHON
    """
    return PythonImplementation.loads(platform.python_implementation())


def is_cpython() -> bool:
    """
    Check if the current Python implementation is CPython.
    
    Overview:
        Return ``True`` if current python is CPython, otherwise return ``False``.

    :return: Current python is CPython or not.
    :rtype: bool
    
    Example::
        >>> is_cpython()
        True  # When running on CPython
    """
    return _get_python_implementation() == PythonImplementation.CPYTHON


def is_ironpython() -> bool:
    """
    Check if the current Python implementation is IronPython.
    
    Overview:
        Return ``True`` if current python is IronPython, otherwise return ``False``.

    :return: Current python is IronPython or not.
    :rtype: bool
    
    Example::
        >>> is_ironpython()
        False  # When running on CPython
    """
    return _get_python_implementation() == PythonImplementation.IRONPYTHON


def is_jython() -> bool:
    """
    Check if the current Python implementation is Jython.
    
    Overview:
        Return ``True`` if current python is Jython, otherwise return ``False``.

    :return: Current python is Jython or not.
    :rtype: bool
    
    Example::
        >>> is_jython()
        False  # When running on CPython
    """
    return _get_python_implementation() == PythonImplementation.JYTHON


def is_pypy() -> bool:
    """
    Check if the current Python implementation is PyPy.
    
    Overview:
        Return ``True`` if current python is PyPy, otherwise return ``False``.

    :return: Current python is PyPy or not.
    :rtype: bool
    
    Example::
        >>> is_pypy()
        False  # When running on CPython
    """
    return _get_python_implementation() == PythonImplementation.PYPY
