"""
Native expression base utilities for building composable callable expressions.

This module provides the core building blocks for the native expression system.
It defines a lightweight :class:`Expression` base class for composing callables
and a helper function :func:`efunc` for converting arbitrary values into
callable objects. These utilities allow you to combine constants, callables,
and expression objects into reusable, composable expressions.

The module contains the following main components:

* :func:`efunc` - Convert any object into a callable function
* :class:`Expression` - Base class for building custom expression types

.. note::
   Only public interfaces are listed above. Internal helpers are used for
   caching and value conversion, but they are not part of the public API.

Example::

    >>> from hbutils.expression.native.base import Expression, efunc
    >>>
    >>> class MyExpression(Expression):
    ...     def add(self, other):
    ...         return self._func(lambda x, y: x + y, self, other)
    ...
    >>> e1 = MyExpression()
    >>> efunc(e1.add(1))(5)
    6
"""

from functools import lru_cache
from typing import Callable, Any, Optional, Dict, Tuple

__all__ = [
    'efunc',
    'Expression',
]


@lru_cache()
def _raw_expr_func() -> Callable:
    """
    Get the cached :meth:`Expression._expr` method.

    This function uses :func:`functools.lru_cache` to avoid repeated attribute
    lookups on the :class:`Expression` class, improving performance when
    converting values into expressions.

    :return: The :meth:`Expression._expr` class method.
    :rtype: Callable
    """
    return getattr(Expression, '_expr')


def _raw_expr(e: Any) -> 'Expression':
    """
    Convert any value to an :class:`Expression` object.

    This is an internal helper function that wraps the cached
    :meth:`Expression._expr` method.

    :param e: The value to convert to an expression.
    :type e: Any
    :return: An :class:`Expression` object wrapping the input value.
    :rtype: Expression
    """
    return _raw_expr_func()(e)


def efunc(e: Any) -> Callable:
    """
    Get a callable object from any type.

    This function is the primary entry point for converting arbitrary values
    into callables:

    * If ``e`` is an :class:`Expression`, its internal callable is returned.
    * If ``e`` is a callable, a wrapped expression callable is returned.
    * Otherwise, a callable that always returns ``e`` is returned.

    :param e: Original object.
    :type e: Any
    :return: Callable object derived from ``e``.
    :rtype: Callable

    .. note::
        This is the key feature of native expressions. Use :func:`efunc` to
        transform expressions into callable functions.

    Examples::

        >>> from hbutils.expression.native.base import Expression, efunc
        >>>
        >>> class MyExpression(Expression):
        ...     def add(self, other):
        ...         return self._func(lambda x, y: x + y, self, other)
        ...
        >>> e1 = MyExpression()
        >>> efunc(e1.add(1))(5)
        6
    """
    return getattr(_raw_expr(e), '_fcall')


class Expression:
    """
    Base class of expressions.

    This class provides the foundation for building composable expressions.
    It wraps a callable function and provides methods to combine expressions
    into more complex ones.

    The :class:`Expression` class can be subclassed to create custom expression
    types with specialized operators and methods.

    :param func: Callable function used by the expression. If ``None``, the
                 identity function ``lambda x: x`` is used.
    :type func: Optional[Callable]

    :ivar _fcall: Internal callable associated with this expression.
    :vartype _fcall: Callable
    """

    def __init__(self, func: Optional[Callable] = None):
        """
        Initialize an :class:`Expression` instance.

        :param func: Callable function, defaults to ``None`` which means the
                     identity function ``lambda x: x`` is used.
        :type func: Optional[Callable]
        """
        self._fcall = func or (lambda x: x)

    def _func(self, func: Callable, *args: Any, **kwargs: Any) -> 'Expression':
        """
        Build a new expression based on a given function and arguments.

        This method creates a new expression by composing the given function
        with the provided arguments. Each argument is converted to a callable
        using :func:`efunc`, allowing for nested expression composition.

        :param func: Logical function to apply to the evaluated arguments.
        :type func: Callable
        :param args: Positional arguments, which may be expressions, callables,
                     or constants.
        :type args: Any
        :param kwargs: Keyword arguments, which may be expressions, callables,
                       or constants.
        :type kwargs: Any
        :return: A new expression instance of the current class.
        :rtype: Expression

        Examples::

            >>> from hbutils.expression.native.base import Expression, efunc
            >>>
            >>> class MyExpression(Expression):
            ...     def add(self, other):
            ...         return self._func(lambda x, y: x + y, self, other)
            ...
            >>> e1 = MyExpression()
            >>> efunc(e1.add(1))(5)
            6
            >>> efunc(e1.add(e1.add(1)))(5)
            11
        """
        _args: Tuple[Callable, ...] = tuple(efunc(v) for v in args)
        _kwargs: Dict[str, Callable] = {k: efunc(v) for k, v in kwargs.items()}

        def _new_func(x: Any) -> Any:
            return func(
                *(v(x) for v in _args),
                **{k: v(x) for k, v in _kwargs.items()},
            )

        return self.__class__(_new_func)

    @classmethod
    def _expr(cls, v: Any) -> 'Expression':
        """
        Build an expression using this class.

        This class method converts any value into an :class:`Expression` object:

        * If ``v`` is already an :class:`Expression`, return it as-is.
        * If ``v`` is callable, wrap it in an expression.
        * Otherwise, create an expression that returns the constant value ``v``.

        :param v: Any value to convert.
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
