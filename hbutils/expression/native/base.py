"""
This module provides a flexible expression system for creating and composing callable functions.

The module allows users to build complex expressions from simple components, supporting both
direct callable functions and Expression objects. It provides utilities to convert various
types into callable objects and compose them into more complex expressions.

Key Features:
    - Convert any object (Expression, callable, or constant) into a callable function
    - Build complex expressions by composing simpler ones
    - Cache expression function lookups for performance
    - Support for custom expression subclasses with operator overloading

Main Components:
    - :func:`efunc`: Convert any object to a callable function
    - :class:`Expression`: Base class for building custom expression types
"""

from functools import lru_cache
from typing import Callable, Any, Optional

__all__ = [
    'efunc',
    'Expression',
]


@lru_cache()
def _raw_expr_func() -> Callable:
    """
    Get the cached _expr method from Expression class.
    
    This function uses lru_cache to avoid repeated attribute lookups,
    improving performance when converting values to expressions.
    
    :return: The _expr class method from Expression.
    :rtype: Callable
    """
    return getattr(Expression, '_expr')


def _raw_expr(e: Any) -> 'Expression':
    """
    Convert any value to an Expression object.
    
    This is an internal helper function that wraps the cached _expr method.
    
    :param e: The value to convert to an Expression.
    :type e: Any
    
    :return: An Expression object wrapping the input value.
    :rtype: Expression
    """
    return _raw_expr_func()(e)


def efunc(e: Any) -> Callable:
    """
    Get callable object from any types.

    :param e: Original object.
    :type e: Any
    
    :return: Callable object. If given ``e`` is an :class:`Expression`, its callable method will be returned. \
        If given ``e`` is a function, an equivalent method will be returned. Otherwise, a method which always return \
        ``e`` will be returned.
    :rtype: Callable

    .. note::
        This is the key feature of the native expressions, you need to use :func:`efunc` function to transform \
        expressions to callable functions.

    Examples::
        >>> from hbutils.expression import keep, efunc, expr
        >>>
        >>> e1 = keep()
        >>> efunc(e1 == 1)(1)
        True
        >>> efunc(e1 == 1)(2)
        False
        >>>
        >>> e2 = expr(lambda x: x + 2)
        >>> efunc(e2 == 1)(-1)
        True
        >>> efunc(e2 == 1)(1)
        False
    """
    return getattr(_raw_expr(e), '_fcall')


class Expression:
    """
    Base class of expressions.
    
    This class provides the foundation for building composable expressions.
    It wraps a callable function and provides methods to combine expressions
    into more complex ones.
    
    The Expression class can be subclassed to create custom expression types
    with specialized operators and methods.
    """

    def __init__(self, func: Optional[Callable] = None):
        """
        Constructor of :class:`Expression`.

        :param func: Callable function, default is ``None`` which means a ``lambda x: x`` will be used.
        :type func: Optional[Callable]
        """
        self._fcall = func or (lambda x: x)

    def _func(self, func: Callable, *args, **kwargs) -> 'Expression':
        """
        Expression building based on given ``func`` and arguments.
        
        This method creates a new expression by composing the given function with
        the provided arguments. Each argument is converted to a callable using efunc,
        allowing for nested expression composition.

        :param func: Logical function to apply to the evaluated arguments.
        :type func: Callable
        :param args: Positional arguments, can be expressions, callables, or constants.
        :type args: Any
        :param kwargs: Key-word arguments, can be expressions, callables, or constants.
        :type kwargs: Any
        
        :return: New expression with current class.
        :rtype: Expression

        Examples::
            >>> from hbutils.expression import efunc, Expression
            >>>
            >>> class MyExpression(Expression):
            ...     def add(self, other):
            ...         return self._func(lambda x, y: x + y, self, other)
            ...
            >>>
            >>> e1 = MyExpression()
            >>> efunc(e1.add(1))(5)  # 5 + 1 = 6
            6
            >>> efunc(e1.add(e1.add(1)))(5)  # 5 + (5 + 1) = 11
            11
        """
        _args = tuple(efunc(v) for v in args)
        _kwargs = {k: efunc(v) for k, v in kwargs.items()}

        def _new_func(x):
            return func(
                *(v(x) for v in _args),
                **{k: v(x) for k, v in _kwargs.items()},
            )

        return self.__class__(_new_func)

    @classmethod
    def _expr(cls, v: Any) -> 'Expression':
        """
        Build expression with this class.
        
        This class method converts any value into an Expression object:
        - If v is already an Expression, return it as-is
        - If v is callable, wrap it in an Expression
        - Otherwise, create an Expression that returns the constant value v

        :param v: Any types of value.
        :type v: Any
        
        :return: An expression object.
        :rtype: Expression
        """
        if isinstance(v, Expression):
            return v
        elif callable(v):
            return cls(v)
        else:
            return cls(lambda x: v)
