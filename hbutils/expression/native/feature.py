"""
Expression module providing various expression types with operator overloading support.

This module defines several expression classes that extend the base Expression class,
each providing different sets of operator overloads for various use cases:

- CheckExpression: Basic equality/inequality checks
- ComparableExpression: Full comparison operations
- IndexedExpression: Item access operations
- ObjectExpression: Attribute access and callable operations
- LogicalExpression: Logical operations (and, or, not)
- MathExpression: Mathematical operations
- BitwiseExpression: Bitwise operations

These expression classes enable building complex expression trees through operator
overloading, useful for creating DSLs, query builders, or deferred computation systems.
"""

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
    Check expression.

    Features:
        * ``__eq__``, which means ``x == y``.
        * ``__ne__``, which means ``x != y``.
    """

    def __eq__(self, other):
        """
        Equality comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the equality comparison.
        :rtype: Expression

        Example::
            >>> expr = CheckExpression(...)
            >>> result = expr == 5
        """
        return self._func(lambda x, y: x == y, self, other)

    def __ne__(self, other):
        """
        Inequality comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the inequality comparison.
        :rtype: Expression

        Example::
            >>> expr = CheckExpression(...)
            >>> result = expr != 5
        """
        return self._func(lambda x, y: x != y, self, other)


class ComparableExpression(CheckExpression):
    """
    Comparable expression.

    Features:
        * ``__eq__``, which means ``x == y`` (the same as :class:`CheckExpression`).
        * ``__ne__``, which means ``x != y`` (the same as :class:`CheckExpression`).
        * ``__ge__``, which means ``x >= y``.
        * ``__gt__``, which means ``x > y``.
        * ``__le__``, which means ``x <= y``.
        * ``__lt__``, which means ``x < y``.
    """

    def __le__(self, other):
        """
        Less than or equal to comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the less than or equal comparison.
        :rtype: Expression

        Example::
            >>> expr = ComparableExpression(...)
            >>> result = expr <= 10
        """
        return self._func(lambda x, y: x <= y, self, other)

    def __lt__(self, other):
        """
        Less than comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the less than comparison.
        :rtype: Expression

        Example::
            >>> expr = ComparableExpression(...)
            >>> result = expr < 10
        """
        return self._func(lambda x, y: x < y, self, other)

    def __ge__(self, other):
        """
        Greater than or equal to comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the greater than or equal comparison.
        :rtype: Expression

        Example::
            >>> expr = ComparableExpression(...)
            >>> result = expr >= 5
        """
        return self._func(lambda x, y: x >= y, self, other)

    def __gt__(self, other):
        """
        Greater than comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the greater than comparison.
        :rtype: Expression

        Example::
            >>> expr = ComparableExpression(...)
            >>> result = expr > 5
        """
        return self._func(lambda x, y: x > y, self, other)


class IndexedExpression(Expression):
    """
    Indexed expression.

    Features:
        * ``__getitem__``, which means ``x[y]``.
    """

    def __getitem__(self, item):
        """
        Item access operator.

        :param item: The index or key to access.
        :type item: Any
        :return: A new expression representing the item access.
        :rtype: Expression

        Example::
            >>> expr = IndexedExpression(...)
            >>> result = expr[0]
            >>> result = expr['key']
        """
        return self._func(lambda x, y: x[y], self, item)


class ObjectExpression(Expression):
    """
    Object-like expression.

    Features:
        * ``__getattr__``, which means ``x.y``.
        * ``__call__``, which means ``x(*args, **kwargs)``.
    """

    def __getattr__(self, item):
        """
        Attribute access operator.

        :param item: The attribute name to access.
        :type item: str
        :return: A new expression representing the attribute access.
        :rtype: Expression

        Example::
            >>> expr = ObjectExpression(...)
            >>> result = expr.attribute_name
        """
        return self._func(lambda x, y: getattr(x, y), self, item)

    def __call__(self, *args, **kwargs):
        """
        Call operator for making the expression callable.

        :param args: Positional arguments to pass to the call.
        :type args: tuple
        :param kwargs: Keyword arguments to pass to the call.
        :type kwargs: dict
        :return: A new expression representing the function call.
        :rtype: Expression

        Example::
            >>> expr = ObjectExpression(...)
            >>> result = expr(arg1, arg2, key=value)
        """
        return self._func(lambda s, *args_, **kwargs_: s(*args_, **kwargs_), self, *args, **kwargs)


class LogicalExpression(Expression):
    """
    Logic expression.

    Features:
        * ``__and__``, which means ``x and y`` (written as ``x & y``).
        * ``__or__``, which means ``x or y`` (written as ``x | y``).
        * ``__invert__``, which means ``not x`` (written as ``~x``).

    .. note::
        Do not use this with :class:`BitwiseExpression`, or unexpected conflict will be caused.
    """

    def __and__(self, other):
        """
        Logical AND operator.

        :param other: The right operand for the AND operation.
        :type other: Any
        :return: A new expression representing the logical AND.
        :rtype: Expression

        Example::
            >>> expr1 = LogicalExpression(...)
            >>> expr2 = LogicalExpression(...)
            >>> result = expr1 & expr2
        """
        return self._func(lambda x, y: x and y, self, other)

    def __rand__(self, other):
        """
        Reverse logical AND operator.

        :param other: The left operand for the AND operation.
        :type other: Any
        :return: A new expression representing the logical AND.
        :rtype: Expression

        Example::
            >>> expr = LogicalExpression(...)
            >>> result = True & expr
        """
        return self._func(lambda x, y: x and y, other, self)

    def __or__(self, other):
        """
        Logical OR operator.

        :param other: The right operand for the OR operation.
        :type other: Any
        :return: A new expression representing the logical OR.
        :rtype: Expression

        Example::
            >>> expr1 = LogicalExpression(...)
            >>> expr2 = LogicalExpression(...)
            >>> result = expr1 | expr2
        """
        return self._func(lambda x, y: x or y, self, other)

    def __ror__(self, other):
        """
        Reverse logical OR operator.

        :param other: The left operand for the OR operation.
        :type other: Any
        :return: A new expression representing the logical OR.
        :rtype: Expression

        Example::
            >>> expr = LogicalExpression(...)
            >>> result = False | expr
        """
        return self._func(lambda x, y: x or y, other, self)

    def __invert__(self):
        """
        Logical NOT operator.

        :return: A new expression representing the logical NOT.
        :rtype: Expression

        Example::
            >>> expr = LogicalExpression(...)
            >>> result = ~expr
        """
        return self._func(lambda x: not x, self)


class MathExpression(Expression):
    """
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
        """
        Addition operator.

        :param other: The value to add.
        :type other: Any
        :return: A new expression representing the addition.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = expr + 5
        """
        return self._func(lambda x, y: x + y, self, other)

    def __radd__(self, other):
        """
        Reverse addition operator.

        :param other: The left operand for addition.
        :type other: Any
        :return: A new expression representing the addition.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = 5 + expr
        """
        return self._func(lambda x, y: x + y, other, self)

    def __sub__(self, other):
        """
        Subtraction operator.

        :param other: The value to subtract.
        :type other: Any
        :return: A new expression representing the subtraction.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = expr - 5
        """
        return self._func(lambda x, y: x - y, self, other)

    def __rsub__(self, other):
        """
        Reverse subtraction operator.

        :param other: The left operand for subtraction.
        :type other: Any
        :return: A new expression representing the subtraction.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = 10 - expr
        """
        return self._func(lambda x, y: x - y, other, self)

    def __mul__(self, other):
        """
        Multiplication operator.

        :param other: The value to multiply by.
        :type other: Any
        :return: A new expression representing the multiplication.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = expr * 3
        """
        return self._func(lambda x, y: x * y, self, other)

    def __rmul__(self, other):
        """
        Reverse multiplication operator.

        :param other: The left operand for multiplication.
        :type other: Any
        :return: A new expression representing the multiplication.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = 3 * expr
        """
        return self._func(lambda x, y: x * y, other, self)

    def __truediv__(self, other):
        """
        True division operator.

        :param other: The divisor.
        :type other: Any
        :return: A new expression representing the division.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = expr / 2
        """
        return self._func(lambda x, y: x / y, self, other)

    def __rtruediv__(self, other):
        """
        Reverse true division operator.

        :param other: The dividend.
        :type other: Any
        :return: A new expression representing the division.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = 10 / expr
        """
        return self._func(lambda x, y: x / y, other, self)

    def __floordiv__(self, other):
        """
        Floor division operator.

        :param other: The divisor.
        :type other: Any
        :return: A new expression representing the floor division.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = expr // 2
        """
        return self._func(lambda x, y: x // y, self, other)

    def __rfloordiv__(self, other):
        """
        Reverse floor division operator.

        :param other: The dividend.
        :type other: Any
        :return: A new expression representing the floor division.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = 10 // expr
        """
        return self._func(lambda x, y: x // y, other, self)

    def __mod__(self, other):
        """
        Modulo operator.

        :param other: The divisor for modulo operation.
        :type other: Any
        :return: A new expression representing the modulo.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = expr % 3
        """
        return self._func(lambda x, y: x % y, self, other)

    def __rmod__(self, other):
        """
        Reverse modulo operator.

        :param other: The dividend for modulo operation.
        :type other: Any
        :return: A new expression representing the modulo.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = 10 % expr
        """
        return self._func(lambda x, y: x % y, other, self)

    def __pow__(self, power):
        """
        Power operator.

        :param power: The exponent.
        :type power: Any
        :return: A new expression representing the power operation.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = expr ** 2
        """
        return self._func(lambda x, y: x ** y, self, power)

    def __rpow__(self, other):
        """
        Reverse power operator.

        :param other: The base for power operation.
        :type other: Any
        :return: A new expression representing the power operation.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = 2 ** expr
        """
        return self._func(lambda x, y: x ** y, other, self)

    def __pos__(self):
        """
        Unary positive operator.

        :return: A new expression representing the positive value.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = +expr
        """
        return self._func(lambda x: +x, self)

    def __neg__(self):
        """
        Unary negative operator.

        :return: A new expression representing the negative value.
        :rtype: Expression

        Example::
            >>> expr = MathExpression(...)
            >>> result = -expr
        """
        return self._func(lambda x: -x, self)


class BitwiseExpression(Expression):
    """
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
        """
        Bitwise OR operator.

        :param other: The right operand for bitwise OR.
        :type other: Any
        :return: A new expression representing the bitwise OR.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = expr | 0b1010
        """
        return self._func(lambda x, y: x | y, self, other)

    def __ror__(self, other):
        """
        Reverse bitwise OR operator.

        :param other: The left operand for bitwise OR.
        :type other: Any
        :return: A new expression representing the bitwise OR.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = 0b1010 | expr
        """
        return self._func(lambda x, y: x | y, other, self)

    def __xor__(self, other):
        """
        Bitwise XOR operator.

        :param other: The right operand for bitwise XOR.
        :type other: Any
        :return: A new expression representing the bitwise XOR.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = expr ^ 0b1010
        """
        return self._func(lambda x, y: x ^ y, self, other)

    def __rxor__(self, other):
        """
        Reverse bitwise XOR operator.

        :param other: The left operand for bitwise XOR.
        :type other: Any
        :return: A new expression representing the bitwise XOR.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = 0b1010 ^ expr
        """
        return self._func(lambda x, y: x ^ y, other, self)

    def __and__(self, other):
        """
        Bitwise AND operator.

        :param other: The right operand for bitwise AND.
        :type other: Any
        :return: A new expression representing the bitwise AND.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = expr & 0b1010
        """
        return self._func(lambda x, y: x & y, self, other)

    def __rand__(self, other):
        """
        Reverse bitwise AND operator.

        :param other: The left operand for bitwise AND.
        :type other: Any
        :return: A new expression representing the bitwise AND.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = 0b1010 & expr
        """
        return self._func(lambda x, y: x & y, other, self)

    def __invert__(self):
        """
        Bitwise NOT operator.

        :return: A new expression representing the bitwise NOT.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = ~expr
        """
        return self._func(lambda x: ~x, self)

    def __lshift__(self, other):
        """
        Left shift operator.

        :param other: The number of positions to shift left.
        :type other: Any
        :return: A new expression representing the left shift.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = expr << 2
        """
        return self._func(lambda x, y: x << y, self, other)

    def __rlshift__(self, other):
        """
        Reverse left shift operator.

        :param other: The value to be shifted left.
        :type other: Any
        :return: A new expression representing the left shift.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = 5 << expr
        """
        return self._func(lambda x, y: x << y, other, self)

    def __rshift__(self, other):
        """
        Right shift operator.

        :param other: The number of positions to shift right.
        :type other: Any
        :return: A new expression representing the right shift.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = expr >> 2
        """
        return self._func(lambda x, y: x >> y, self, other)

    def __rrshift__(self, other):
        """
        Reverse right shift operator.

        :param other: The value to be shifted right.
        :type other: Any
        :return: A new expression representing the right shift.
        :rtype: Expression

        Example::
            >>> expr = BitwiseExpression(...)
            >>> result = 20 >> expr
        """
        return self._func(lambda x, y: x >> y, other, self)
