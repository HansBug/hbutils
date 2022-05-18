from .base import Expression

__all__ = [
    'CheckExpression',
    'ComparableExpression',
    'IndexedExpression',
    'AttredExpression',
    'CallableExpression',
    'LogicalExpression',
    'MathExpression',
    'BitMathExpression',
]


class CheckExpression(Expression):
    def __eq__(self, other):
        return self._func(lambda x, y: x == y, self, other)

    def __ne__(self, other):
        return self._func(lambda x, y: x != y, self, other)


class ComparableExpression(CheckExpression):
    def __le__(self, other):
        return self._func(lambda x, y: x <= y, self, other)

    def __lt__(self, other):
        return self._func(lambda x, y: x < y, self, other)

    def __ge__(self, other):
        return self._func(lambda x, y: x >= y, self, other)

    def __gt__(self, other):
        return self._func(lambda x, y: x > y, self, other)


class IndexedExpression(Expression):
    def __getitem__(self, item):
        return self._func(lambda x, y: x[y], self, item)


class AttredExpression(Expression):
    def __getattr__(self, item):
        return self._func(lambda x, y: getattr(x, y), self, item)


class CallableExpression(Expression):
    def __call__(self, *args, **kwargs):
        return self._func(lambda s, *args_, **kwargs_: s(*args_, **kwargs_), self, *args, **kwargs)


class LogicalExpression(Expression):
    """
    Overview:
        Logic expression.

    .. note::
        Do not use this with :class:`BitMathExpression`, or unexpected conflict will be caused.
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


class BitMathExpression(Expression):
    """
    Overview:
        Binary math expression class.

    .. note::
        Do not use this with :class:`LogicExpression`, or unexpected conflict will be caused.
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
