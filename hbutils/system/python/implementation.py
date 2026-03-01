"""
Python implementation detection utilities.

This module provides lightweight helpers to detect the active Python
implementation (such as CPython, PyPy, IronPython, or Jython). It exposes
an :class:`PythonImplementation` enumeration for normalized representation
and a set of convenience predicate functions for common checks. Detection
is based on :func:`platform.python_implementation` and the result is cached
for performance.

The module contains the following main components:

* :class:`PythonImplementation` - Enumeration of supported implementations
* :func:`is_cpython` - Predicate for CPython detection
* :func:`is_ironpython` - Predicate for IronPython detection
* :func:`is_jython` - Predicate for Jython detection
* :func:`is_pypy` - Predicate for PyPy detection

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
    :func:`hbutils.model.enum.int_enum_loads` decorator.

    :cvar CPYTHON: The standard CPython implementation.
    :cvar IRONPYTHON: The IronPython implementation (.NET-based).
    :cvar JYTHON: The Jython implementation (JVM-based).
    :cvar PYPY: The PyPy implementation (JIT-compiled).

    Example::

        >>> PythonImplementation.loads('cpython')
        <PythonImplementation.CPYTHON: 1>
        >>> PythonImplementation.loads('PyPy')
        <PythonImplementation.PYPY: 4>
    """
    CPYTHON = 1
    IRONPYTHON = 2
    JYTHON = 3
    PYPY = 4


@lru_cache()
def _get_python_implementation() -> PythonImplementation:
    """
    Get the current Python implementation.

    This function detects the Python implementation using
    :func:`platform.python_implementation` and converts it to a
    :class:`PythonImplementation` enum value. The result is cached for
    performance since the implementation cannot change during runtime.

    :return: The detected Python implementation.
    :rtype: PythonImplementation
    :raises KeyError: If the implementation name cannot be mapped to
        :class:`PythonImplementation`.
    :raises TypeError: If the returned implementation name is not a string.

    Example::

        >>> impl = _get_python_implementation()
        >>> print(impl)
        PythonImplementation.CPYTHON
    """
    return PythonImplementation.loads(platform.python_implementation())


def is_cpython() -> bool:
    """
    Check if the current Python implementation is CPython.

    :return: ``True`` if the current Python implementation is CPython,
        otherwise ``False``.
    :rtype: bool

    Example::

        >>> is_cpython()
        True  # When running on CPython
    """
    return _get_python_implementation() == PythonImplementation.CPYTHON


def is_ironpython() -> bool:
    """
    Check if the current Python implementation is IronPython.

    :return: ``True`` if the current Python implementation is IronPython,
        otherwise ``False``.
    :rtype: bool

    Example::

        >>> is_ironpython()
        False  # When running on CPython
    """
    return _get_python_implementation() == PythonImplementation.IRONPYTHON


def is_jython() -> bool:
    """
    Check if the current Python implementation is Jython.

    :return: ``True`` if the current Python implementation is Jython,
        otherwise ``False``.
    :rtype: bool

    Example::

        >>> is_jython()
        False  # When running on CPython
    """
    return _get_python_implementation() == PythonImplementation.JYTHON


def is_pypy() -> bool:
    """
    Check if the current Python implementation is PyPy.

    :return: ``True`` if the current Python implementation is PyPy,
        otherwise ``False``.
    :rtype: bool

    Example::

        >>> is_pypy()
        False  # When running on CPython
    """
    return _get_python_implementation() == PythonImplementation.PYPY
