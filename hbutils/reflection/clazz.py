"""
Overview:
    Useful functions for processing python classes and types.
    
This module provides utility functions for working with Python classes and types,
including class wrapping decorators and common base class detection.
"""
from functools import WRAPPER_ASSIGNMENTS as CLASS_WRAPPER_ASSIGNMENTS
from functools import update_wrapper, partial
from typing import Tuple

__all__ = [
    'class_wraps',
    'common_base',
]

CLASS_WRAPPER_UPDATES = ()


def class_wraps(wrapped: type,
                assigned: Tuple[str] = CLASS_WRAPPER_ASSIGNMENTS,
                updated: Tuple[str] = CLASS_WRAPPER_UPDATES):
    """
    Wrapper decorator for class.
    
    This function creates a decorator that can be used to wrap a class while preserving
    its metadata (similar to functools.wraps but for classes). It updates the wrapper
    class with attributes from the wrapped class.

    :param wrapped: The class to be wrapped.
    :type wrapped: type
    :param assigned: Tuple of attribute names to be assigned from wrapped to wrapper.
                     Defaults to CLASS_WRAPPER_ASSIGNMENTS (same as functools.WRAPPER_ASSIGNMENTS).
    :type assigned: Tuple[str]
    :param updated: Tuple of attribute names to be updated from wrapped to wrapper.
                    Defaults to CLASS_WRAPPER_UPDATES (empty tuple).
    :type updated: Tuple[str]
    
    :return: A partial function that can be used as a decorator.
    :rtype: functools.partial
    
    Examples::
        >>> def cls_dec(clazz):
        ...     @class_wraps(clazz)
        ...     class _NewClazz(clazz):
        ...         pass
        ...
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
    Get common base class of the given classes.
    
    This function finds the most specific common base class shared by all provided classes.
    Only the ``__base__`` attribute is considered during the search, which means it follows
    the direct inheritance chain rather than the full MRO (Method Resolution Order).

    :param cls: The first class to find common base for.
    :type cls: type
    :param clss: Additional classes to find common base for.
    :type clss: type
    
    :return: The most specific common base class shared by all input classes.
    :rtype: type
    
    Examples::
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
