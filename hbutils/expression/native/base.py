from functools import lru_cache
from typing import Callable

__all__ = [
    'efunc',
    'Expression',
]


@lru_cache()
def _raw_expr_func():
    return getattr(Expression, '_expr')


def _raw_expr(e) -> 'Expression':
    return _raw_expr_func()(e)


def efunc(e) -> Callable:
    """
    Overview:
        Get callable object from any types.

    :param e: Original object.
    :return: Callable object. If given ``e`` is an :class:`Expression`, its callable method will be returned. \
        If given ``e`` is a function, an equivalent method will be returned. Otherwise, a method which always return \
        ``e`` will be returned.

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
    Overview:
        Base class of expressions.
    """

    def __init__(self, func=None):
        """
        Constructor of :class:`Expression`.

        :param func: Callable function, default is ``None`` which means a ``lambda x: x`` will be used.
        """
        self._fcall = func or (lambda x: x)

    def _func(self, func: Callable, *args, **kwargs):
        """
        Expression building based on given ``func`` and arguments.

        :param func: Logical function.
        :param args: Positional arguments.
        :param kwargs: Key-word arguments.
        :return: New expression with current class.

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
    def _expr(cls, v):
        """
        Build expression with this class.

        :param v: Any types of value.
        :return: An expression object.
        """
        if isinstance(v, Expression):
            return v
        elif callable(v):
            return cls(v)
        else:
            return cls(lambda x: v)
