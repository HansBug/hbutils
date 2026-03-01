"""
Decorator utilities for flexible decorator usage.

This module provides a utility function that simplifies the creation of
decorators which can be used both with and without parameters. It focuses on
the common pattern where a decorator accepts optional keyword arguments and
wraps a target function accordingly.

The module contains the following main components:

* :func:`decolize` - A decorator for decorators that enables optional arguments.

Example::

    >>> from functools import wraps
    >>> from hbutils.design.decorator import decolize
    >>>
    >>> @decolize
    ... def deco(func, a=1, b=2):
    ...     @wraps(func)
    ...     def _new_func(*args, **kwargs):
    ...         return func(*args, **kwargs) * a + b
    ...     return _new_func
    >>>
    >>> @deco
    ... def f1(x):
    ...     return x
    >>>
    >>> @deco(a=2)
    ... def f2(x):
    ...     return x
    >>>
    >>> f1(3)
    5
    >>> f2(3)
    8

.. note::
   Only keyword arguments are supported for parameterized decorator usage.

"""

__all__ = ['decolize']

from functools import wraps, partial
from typing import Callable, Optional, Any

from .singleton import SingletonMark

_NO_FUNC = SingletonMark('NO_FUNC_FOR_DECORATOR')


def decolize(deco: Callable[..., Callable]) -> Callable:
    """
    Decorator for decorator, make a decorator function with keyword-arguments
    usable as the real python decorator.

    This utility allows decorators with parameters to be used both as simple decorators
    (without parentheses) and as parameterized decorators (with parentheses and arguments).

    :param deco: Decorator function to be decorated. The first parameter should be the
                 function to be decorated, followed by optional keyword arguments.
    :type deco: Callable[..., Callable]
    :return: A new decorator that can be used with or without parameters.
    :rtype: Callable

    .. tip::
        This decorator can be useful when building a decorator with parameters.

    .. note::
        In the decorated decorator, **only keyword arguments are supported**.
        So make sure the original decorator function's parameters (except ``func``) are
        all keyword supported, and do not try to use positional arguments when using it to
        decorate another function.

    Examples::

        >>> from functools import wraps
        >>> @decolize  # decorate the decorator
        ... def deco(func, a=1, b=2):
        ...     @wraps(func)
        ...     def _new_func(*args, **kwargs):
        ...         return func(*args, **kwargs) * a + b
        ...
        ...     return _new_func
        >>> @deco  # used as simple decorator, same as deco(_func_1)
        ... def _func_1(a, b, c):
        ...     return (a + b * 2) * c
        >>> @deco(a=2)  # used as parameterized decorator, same as deco(_func_2, a=2)
        ... def _func_2(a, b, c):
        ...     return (a + b * 2) * c
        >>> _func_1(1, 2, 3)
        17
        >>> _func_2(1, 2, 3)
        32
    """

    @wraps(deco)
    def _new_deco(func: Optional[Callable] = _NO_FUNC, **kwargs: Any) -> Callable:
        """
        Internal wrapper function that handles both parameterized and non-parameterized usage.

        :param func: The function to be decorated. If not provided (``_NO_FUNC``), returns a
                     partial function for parameterized decoration.
        :type func: Optional[Callable]
        :param kwargs: Keyword arguments to pass to the original decorator.
        :type kwargs: dict
        :return: Either a partial function (for parameterized use) or the decorated function.
        :rtype: Callable
        """
        if func is _NO_FUNC:  # used as parameterized decorator
            return partial(deco, **kwargs)
        else:  # functional use
            return deco(func, **kwargs)

    return _new_deco
