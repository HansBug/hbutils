"""
Overview:
    Some useful utilities for decorator pattern and python decorators \
    for function or class.
"""
__all__ = ['decolize']

from functools import wraps, partial
from typing import Callable, Optional

from .singleton import SingletonMark

_NO_FUNC = SingletonMark('NO_FUNC_FOR_DECORATOR')


def decolize(deco: Callable[..., Callable]):
    """
    Overview:
        Decorator for decorator, make a decorator function with keyword-arguments \
        usable as the real python decorator.

    Arguments:
        - deco (:obj:`Callable[..., Callable]`): Decorator function to be decorated.

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
        >>> def _func_1(a, b, c):
        ...     return (a + b * 2) * c

        >>> @deco(a=2)  # used as parameterized decorator, same as deco(_func_2, a=2)
        >>> def _func_2(a, b, c):
        ...     return (a + b * 2) * c

        >>> _func_1(1, 2, 3)
        17  # ((1 + 2 * 2) * 3) * 1 + 2 == 17
        >>> _func_2(1, 2, 3)
        32  # ((1 + 2 * 2) * 3) * 2 + 2 == 32

    .. tip::

        This decorator can be useful when build a decorator with parameters.

    .. note::

        In the decorated decorator, **only keyword arguments are supported**. \
        So make sure the original decorator function's parameter (except ``func``) are \
        all keyword supported, and do not try to use positional arguments when use it to \
        decorator another function.

    """

    @wraps(deco)
    def _new_deco(func: Optional[Callable] = _NO_FUNC, **kwargs):
        if func is _NO_FUNC:  # used as parameterized decorator
            return partial(deco, **kwargs)
        else:  # functional use
            return deco(func, **kwargs)

    return _new_deco
