from .base import Expression

__all__ = [
    'CheckExpression',
    'ComparableExpression',
    'IndexedExpression',
    'ObjectExpression',
    'LogicalExpression',
    'MathExpression',
    'BitwiseExpression',
]


class CheckExpression(Expression):
    """
    Overview:
        Check expression.

    Features:
        * ``__eq__``, which means ``x == y``.
        * ``__ne__``, which means ``x == y``.
    """

    def __eq__(self, other):
        return self._func(lambda x, y: x == y, self, other)

    def __ne__(self, other):
        return self._func(lambda x, y: x != y, self, other)


class ComparableExpression(CheckExpression):
    """
    Overview:
        Comparable expression.

    Features:
        * ``__eq__``, which means ``x == y`` (the same as :class:`CheckExpression`).
        * ``__ne__``, which means ``x == y`` (the same as :class:`CheckExpression`).
        * ``__ge__``, which means ``x >= y``.
        * ``__gt__``, which means ``x > y``.
        * ``__le__``, which means ``x <= y``.
        * ``__lt__``, which means ``x < y``.
    """

    def __le__(self, other):
        return self._func(lambda x, y: x <= y, self, other)

    def __lt__(self, other):
        return self._func(lambda x, y: x < y, self, other)

    def __ge__(self, other):
        return self._func(lambda x, y: x >= y, self, other)

    def __gt__(self, other):
        return self._func(lambda x, y: x > y, self, other)


class IndexedExpression(Expression):
    """
    Overview:
        Indexed expression.

    Features:
        * ``__getitem__``, which means ``x[y]``.
    """

    def __getitem__(self, item):
        return self._func(lambda x, y: x[y], self, item)


class ObjectExpression(Expression):
    """
    Overview:
        Object-like expression.

    Features:
        * ``__getattr__``, which means ``x.y``.
        * ``__call__``, which means ``x(*args, **kwargs)``.
    """

    def __getattr__(self, item):
        return self._func(lambda x, y: getattr(x, y), self, item)

    def __call__(self, *args, **kwargs):
        return self._func(lambda s, *args_, **kwargs_: s(*args_, **kwargs_), self, *args, **kwargs)


class LogicalExpression(Expression):
    """
    Overview:
        Logic expression.

    Features:
        * ``__and__``, which means ``x and y`` (written as ``x & y``).
        * ``__or__``, which means ``x or y`` (written as ``x | y``).
        * ``__invert__``, which means ``not x`` (written as ``~x``).

    .. note::
        Do not use this with :class:`BitwiseExpression`, or unexpected conflict will be caused.
    """

    def __and__(self, other):
        return self._func(lambda x, y: x and y, self, other)

    def __rand__(self, other):
        return self._func(lambda x, y: x and y, other, self)

    def __or__(self, other):
        return self._func(lambda x, y: x or y, self, other)

    def __ror__(self, other):
        return self._func(lambda x, y: x or y, other, self)

    def __invert__(self):
        return self._func(lambda x: not x, self)


class MathExpression(Expression):
    """
    Overview:
        Math calculation expression.

    Features:
        * ``__add__``, which means ``x + y``.
        * ``__sub__``, which means ``x - y``.
        * ``__mul__``, which means ``x * y``.
        * ``__truediv__``, which means ``x / y``.
        * ``__floordiv__``, which means ``x // y``.
        * ``__mod__``, which means ``x % y``.
        * ``__pow__``, which means ``x ** y``.
        * ``__pos__``, which means ``+x``.
        * ``__neg__``, which means ``-x``.
    """

    def __add__(self, other):
        return self._func(lambda x, y: x + y, self, other)

    def __radd__(self, other):
        return self._func(lambda x, y: x + y, other, self)

    def __sub__(self, other):
        return self._func(lambda x, y: x - y, self, other)

    def __rsub__(self, other):
        return self._func(lambda x, y: x - y, other, self)

    def __mul__(self, other):
        return self._func(lambda x, y: x * y, self, other)

    def __rmul__(self, other):
        return self._func(lambda x, y: x * y, other, self)

    def __truediv__(self, other):
        return self._func(lambda x, y: x / y, self, other)

    def __rtruediv__(self, other):
        return self._func(lambda x, y: x / y, other, self)

    def __floordiv__(self, other):
        return self._func(lambda x, y: x // y, self, other)

    def __rfloordiv__(self, other):
        return self._func(lambda x, y: x // y, other, self)

    def __mod__(self, other):
        return self._func(lambda x, y: x % y, self, other)

    def __rmod__(self, other):
        return self._func(lambda x, y: x % y, other, self)

    def __pow__(self, power):
        return self._func(lambda x, y: x ** y, self, power)

    def __rpow__(self, other):
        return self._func(lambda x, y: x ** y, other, self)

    def __pos__(self):
        return self._func(lambda x: +x, self)

    def __neg__(self):
        return self._func(lambda x: -x, self)


class BitwiseExpression(Expression):
    """
    Overview:
        Bitwise expression class.

    Features:
        * ``__and__``, which means ``x & y`` (bitwise).
        * ``__or__``, which means ``x | y`` (bitwise).
        * ``__xor__``, which means ``x ^ y`` (bitwise).
        * ``__lshift__``, which means ``x << y`` (bitwise).
        * ``__rshift__``, which means ``x >> y`` (bitwise).
        * ``__invert__``, which means ``~x`` (bitwise).

    .. note::
        Do not use this with :class:`LogicalExpression`, or unexpected conflict will be caused.
    """

    def __or__(self, other):
        return self._func(lambda x, y: x | y, self, other)

    def __ror__(self, other):
        return self._func(lambda x, y: x | y, other, self)

    def __xor__(self, other):
        return self._func(lambda x, y: x ^ y, self, other)

    def __rxor__(self, other):
        return self._func(lambda x, y: x ^ y, other, self)

    def __and__(self, other):
        return self._func(lambda x, y: x & y, self, other)

    def __rand__(self, other):
        return self._func(lambda x, y: x & y, other, self)

    def __invert__(self):
        return self._func(lambda x: ~x, self)

    def __lshift__(self, other):
        return self._func(lambda x, y: x << y, self, other)

    def __rlshift__(self, other):
        return self._func(lambda x, y: x << y, other, self)

    def __rshift__(self, other):
        return self._func(lambda x, y: x >> y, self, other)

    def __rrshift__(self, other):
        return self._func(lambda x, y: x >> y, other, self)
