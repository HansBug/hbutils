"""
Class and type reflection utilities.

This module provides helper functions for working with Python classes and types.
It includes utilities for creating class-wrapping decorators that preserve
metadata (similar to :func:`functools.wraps`) and for determining the most
specific common base class across multiple classes.

The module contains the following public components:

* :func:`class_wraps` - Create a class wrapper decorator that preserves metadata
* :func:`common_base` - Find the most specific common base class

Example::

    >>> from hbutils.reflection.clazz import class_wraps, common_base
    >>>
    >>> def cls_dec(clazz):
    ...     @class_wraps(clazz)
    ...     class _NewClazz(clazz):
    ...         pass
    ...     return _NewClazz
    ...
    >>> class Original:
    ...     '''Original class docstring'''
    ...     pass
    ...
    >>> @cls_dec
    ... class Wrapped(Original):
    ...     pass
    ...
    >>> Wrapped.__doc__
    'Original class docstring'
    >>> common_base(RuntimeError, ValueError, KeyError)
    <class 'Exception'>

"""
from functools import WRAPPER_ASSIGNMENTS as CLASS_WRAPPER_ASSIGNMENTS
from functools import update_wrapper, partial
from typing import Tuple, Callable

__all__ = [
    'class_wraps',
    'common_base',
]

CLASS_WRAPPER_UPDATES: Tuple[str, ...] = ()


def class_wraps(wrapped: type,
                assigned: Tuple[str, ...] = CLASS_WRAPPER_ASSIGNMENTS,
                updated: Tuple[str, ...] = CLASS_WRAPPER_UPDATES) -> Callable[[type], type]:
    """
    Create a wrapper decorator for classes.

    This function creates a decorator that can be used to wrap a class while
    preserving its metadata (similar to :func:`functools.wraps` but for classes).
    It updates the wrapper class with attributes from the wrapped class.

    :param wrapped: The class to be wrapped.
    :type wrapped: type
    :param assigned: Tuple of attribute names to be assigned from wrapped to wrapper.
                     Defaults to :data:`functools.WRAPPER_ASSIGNMENTS`.
    :type assigned: Tuple[str, ...]
    :param updated: Tuple of attribute names to be updated from wrapped to wrapper.
                    Defaults to an empty tuple (no updates).
    :type updated: Tuple[str, ...]
    :return: A callable decorator that updates a wrapper class with metadata.
    :rtype: Callable[[type], type]

    .. note::
       The returned decorator is a :class:`functools.partial` of
       :func:`functools.update_wrapper` and is intended to be used when defining
       a new class that wraps an existing class.

    Example::

        >>> def cls_dec(clazz):
        ...     @class_wraps(clazz)
        ...     class _NewClazz(clazz):
        ...         pass
        ...     return _NewClazz
        >>>
        >>> class Original:
        ...     '''Original class docstring'''
        ...     pass
        >>>
        >>> @cls_dec
        ... class Wrapped(Original):
        ...     pass
        >>>
        >>> Wrapped.__doc__
        'Original class docstring'
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)


def common_base(cls: type, *clss: type) -> type:
    """
    Get the most specific common base class for the given classes.

    This function finds the most specific common base class shared by all
    provided classes. Only the ``__base__`` attribute is considered during the
    search, which means it follows the direct inheritance chain rather than the
    full Method Resolution Order (MRO).

    :param cls: The first class to find a common base for.
    :type cls: type
    :param clss: Additional classes to find a common base for.
    :type clss: type
    :return: The most specific common base class shared by all input classes.
    :rtype: type
    :raises TypeError: If any provided argument is not a class.

    Example::

        >>> from hbutils.reflection import common_base
        >>> common_base(object)
        <class 'object'>
        >>> common_base(object, int, str)
        <class 'object'>
        >>> common_base(RuntimeError, ValueError, KeyError)
        <class 'Exception'>
        >>> common_base(int, float)
        <class 'object'>
        >>>
        >>> class A: pass
        >>> class B(A): pass
        >>> class C(A): pass
        >>> common_base(B, C)
        <class '__main__.A'>
    """
    current_cls = cls
    for new_cls in clss:
        while not issubclass(new_cls, current_cls):
            current_cls = current_cls.__base__

        if current_cls is object:
            break

    return current_cls
