"""
Operator-oriented expression feature classes.

This module provides a set of expression subclasses that extend
:class:`hbutils.expression.native.base.Expression` with operator overloading.
Each subclass offers a focused set of operators for building expression trees
that can later be evaluated through :func:`hbutils.expression.native.base.efunc`.

The main public components are:

* :class:`CheckExpression` - Equality/inequality operators.
* :class:`ComparableExpression` - Full comparison operators.
* :class:`IndexedExpression` - Item access operator.
* :class:`ObjectExpression` - Attribute access and call operators.
* :class:`LogicalExpression` - Logical operations implemented via bitwise
  operators (``&``, ``|``, ``~``).
* :class:`MathExpression` - Arithmetic operators.
* :class:`BitwiseExpression` - Bitwise operators.

These classes allow building composable expression trees suitable for
domain-specific languages, query builders, or deferred computation.

Example::

    >>> from hbutils.expression.native.feature import MathExpression
    >>> from hbutils.expression.native.base import efunc
    >>> expr = MathExpression()
    >>> calc = efunc((expr + 1) * 2)
    >>> calc(3)
    8

.. note::
   Operators return a new instance of the same class, preserving the expression
   type during chaining.

"""

from typing import Any

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
    Expression supporting basic equality checks.

    This class provides only the ``==`` and ``!=`` operators for building
    comparison expressions.

    Example::

        >>> from hbutils.expression.native.feature import CheckExpression
        >>> from hbutils.expression.native.base import efunc
        >>> expr = CheckExpression()
        >>> is_five = efunc(expr == 5)
        >>> is_five(5)
        True
    """

    def __eq__(self, other: Any) -> Expression:
        """
        Equality comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the equality comparison.
        :rtype: Expression

        Example::

            >>> expr = CheckExpression()
            >>> result = expr == 5
        """
        return self._func(lambda x, y: x == y, self, other)

    def __ne__(self, other: Any) -> Expression:
        """
        Inequality comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the inequality comparison.
        :rtype: Expression

        Example::

            >>> expr = CheckExpression()
            >>> result = expr != 5
        """
        return self._func(lambda x, y: x != y, self, other)


class ComparableExpression(CheckExpression):
    """
    Expression supporting full comparison operations.

    This class extends :class:`CheckExpression` by adding ``<=``, ``<``,
    ``>=``, and ``>`` comparisons.

    Example::

        >>> from hbutils.expression.native.feature import ComparableExpression
        >>> from hbutils.expression.native.base import efunc
        >>> expr = ComparableExpression()
        >>> is_between = efunc((expr >= 1) & (expr < 3))
        >>> is_between(2)
        True
    """

    def __le__(self, other: Any) -> Expression:
        """
        Less than or equal to comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the less than or equal comparison.
        :rtype: Expression

        Example::

            >>> expr = ComparableExpression()
            >>> result = expr <= 10
        """
        return self._func(lambda x, y: x <= y, self, other)

    def __lt__(self, other: Any) -> Expression:
        """
        Less than comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the less than comparison.
        :rtype: Expression

        Example::

            >>> expr = ComparableExpression()
            >>> result = expr < 10
        """
        return self._func(lambda x, y: x < y, self, other)

    def __ge__(self, other: Any) -> Expression:
        """
        Greater than or equal to comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the greater than or equal comparison.
        :rtype: Expression

        Example::

            >>> expr = ComparableExpression()
            >>> result = expr >= 5
        """
        return self._func(lambda x, y: x >= y, self, other)

    def __gt__(self, other: Any) -> Expression:
        """
        Greater than comparison operator.

        :param other: The value to compare with.
        :type other: Any
        :return: A new expression representing the greater than comparison.
        :rtype: Expression

        Example::

            >>> expr = ComparableExpression()
            >>> result = expr > 5
        """
        return self._func(lambda x, y: x > y, self, other)


class IndexedExpression(Expression):
    """
    Expression supporting indexed access.

    This class enables ``expr[key]`` syntax, which produces a new expression
    that indexes into the evaluation target.

    Example::

        >>> from hbutils.expression.native.feature import IndexedExpression
        >>> from hbutils.expression.native.base import efunc
        >>> expr = IndexedExpression()
        >>> getter = efunc(expr["key"])
        >>> getter({"key": "value"})
        'value'
    """

    def __getitem__(self, item: Any) -> Expression:
        """
        Item access operator.

        :param item: The index or key to access.
        :type item: Any
        :return: A new expression representing the item access.
        :rtype: Expression

        Example::

            >>> expr = IndexedExpression()
            >>> result = expr[0]
            >>> result = expr['key']
        """
        return self._func(lambda x, y: x[y], self, item)


class ObjectExpression(Expression):
    """
    Expression supporting attribute access and callable behavior.

    This class supports:

    * Attribute access via ``expr.attr``.
    * Calling via ``expr(*args, **kwargs)``.

    Example::

        >>> from hbutils.expression.native.feature import ObjectExpression
        >>> from hbutils.expression.native.base import efunc
        >>> expr = ObjectExpression()
        >>> attr_getter = efunc(expr.real)
        >>> attr_getter(3+4j)
        3.0
    """

    def __getattr__(self, item: str) -> Expression:
        """
        Attribute access operator.

        :param item: The attribute name to access.
        :type item: str
        :return: A new expression representing the attribute access.
        :rtype: Expression

        Example::

            >>> expr = ObjectExpression()
            >>> result = expr.attribute_name
        """
        return self._func(lambda x, y: getattr(x, y), self, item)

    def __call__(self, *args: Any, **kwargs: Any) -> Expression:
        """
        Call operator for making the expression callable.

        :param args: Positional arguments to pass to the call.
        :type args: Any
        :param kwargs: Keyword arguments to pass to the call.
        :type kwargs: Any
        :return: A new expression representing the function call.
        :rtype: Expression

        Example::

            >>> expr = ObjectExpression()
            >>> result = expr(arg1, arg2, key=value)
        """
        return self._func(lambda s, *args_, **kwargs_: s(*args_, **kwargs_), self, *args, **kwargs)


class LogicalExpression(Expression):
    """
    Expression supporting logical operations.

    The logical operations are implemented using bitwise operators:

    * ``&`` for logical ``and``.
    * ``|`` for logical ``or``.
    * ``~`` for logical ``not``.

    .. note::
       Do not combine this class with :class:`BitwiseExpression` in a single
       expression chain because both reuse bitwise operators.

    Example::

        >>> from hbutils.expression.native.feature import LogicalExpression
        >>> from hbutils.expression.native.base import efunc
        >>> expr = LogicalExpression()
        >>> is_true = efunc(expr & True)
        >>> is_true(True)
        True
    """

    def __and__(self, other: Any) -> Expression:
        """
        Logical AND operator.

        :param other: The right operand for the AND operation.
        :type other: Any
        :return: A new expression representing the logical AND.
        :rtype: Expression

        Example::

            >>> expr1 = LogicalExpression()
            >>> expr2 = LogicalExpression()
            >>> result = expr1 & expr2
        """
        return self._func(lambda x, y: x and y, self, other)

    def __rand__(self, other: Any) -> Expression:
        """
        Reverse logical AND operator.

        :param other: The left operand for the AND operation.
        :type other: Any
        :return: A new expression representing the logical AND.
        :rtype: Expression

        Example::

            >>> expr = LogicalExpression()
            >>> result = True & expr
        """
        return self._func(lambda x, y: x and y, other, self)

    def __or__(self, other: Any) -> Expression:
        """
        Logical OR operator.

        :param other: The right operand for the OR operation.
        :type other: Any
        :return: A new expression representing the logical OR.
        :rtype: Expression

        Example::

            >>> expr1 = LogicalExpression()
            >>> expr2 = LogicalExpression()
            >>> result = expr1 | expr2
        """
        return self._func(lambda x, y: x or y, self, other)

    def __ror__(self, other: Any) -> Expression:
        """
        Reverse logical OR operator.

        :param other: The left operand for the OR operation.
        :type other: Any
        :return: A new expression representing the logical OR.
        :rtype: Expression

        Example::

            >>> expr = LogicalExpression()
            >>> result = False | expr
        """
        return self._func(lambda x, y: x or y, other, self)

    def __invert__(self) -> Expression:
        """
        Logical NOT operator.

        :return: A new expression representing the logical NOT.
        :rtype: Expression

        Example::

            >>> expr = LogicalExpression()
            >>> result = ~expr
        """
        return self._func(lambda x: not x, self)


class MathExpression(Expression):
    """
    Expression supporting arithmetic operations.

    This class provides the usual arithmetic operators, including unary
    operators for positive/negative.

    Example::

        >>> from hbutils.expression.native.feature import MathExpression
        >>> from hbutils.expression.native.base import efunc
        >>> expr = MathExpression()
        >>> f = efunc(-(expr * 2) + 1)
        >>> f(3)
        -5
    """

    def __add__(self, other: Any) -> Expression:
        """
        Addition operator.

        :param other: The value to add.
        :type other: Any
        :return: A new expression representing the addition.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = expr + 5
        """
        return self._func(lambda x, y: x + y, self, other)

    def __radd__(self, other: Any) -> Expression:
        """
        Reverse addition operator.

        :param other: The left operand for addition.
        :type other: Any
        :return: A new expression representing the addition.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = 5 + expr
        """
        return self._func(lambda x, y: x + y, other, self)

    def __sub__(self, other: Any) -> Expression:
        """
        Subtraction operator.

        :param other: The value to subtract.
        :type other: Any
        :return: A new expression representing the subtraction.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = expr - 5
        """
        return self._func(lambda x, y: x - y, self, other)

    def __rsub__(self, other: Any) -> Expression:
        """
        Reverse subtraction operator.

        :param other: The left operand for subtraction.
        :type other: Any
        :return: A new expression representing the subtraction.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = 10 - expr
        """
        return self._func(lambda x, y: x - y, other, self)

    def __mul__(self, other: Any) -> Expression:
        """
        Multiplication operator.

        :param other: The value to multiply by.
        :type other: Any
        :return: A new expression representing the multiplication.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = expr * 3
        """
        return self._func(lambda x, y: x * y, self, other)

    def __rmul__(self, other: Any) -> Expression:
        """
        Reverse multiplication operator.

        :param other: The left operand for multiplication.
        :type other: Any
        :return: A new expression representing the multiplication.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = 3 * expr
        """
        return self._func(lambda x, y: x * y, other, self)

    def __truediv__(self, other: Any) -> Expression:
        """
        True division operator.

        :param other: The divisor.
        :type other: Any
        :return: A new expression representing the division.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = expr / 2
        """
        return self._func(lambda x, y: x / y, self, other)

    def __rtruediv__(self, other: Any) -> Expression:
        """
        Reverse true division operator.

        :param other: The dividend.
        :type other: Any
        :return: A new expression representing the division.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = 10 / expr
        """
        return self._func(lambda x, y: x / y, other, self)

    def __floordiv__(self, other: Any) -> Expression:
        """
        Floor division operator.

        :param other: The divisor.
        :type other: Any
        :return: A new expression representing the floor division.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = expr // 2
        """
        return self._func(lambda x, y: x // y, self, other)

    def __rfloordiv__(self, other: Any) -> Expression:
        """
        Reverse floor division operator.

        :param other: The dividend.
        :type other: Any
        :return: A new expression representing the floor division.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = 10 // expr
        """
        return self._func(lambda x, y: x // y, other, self)

    def __mod__(self, other: Any) -> Expression:
        """
        Modulo operator.

        :param other: The divisor for modulo operation.
        :type other: Any
        :return: A new expression representing the modulo.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = expr % 3
        """
        return self._func(lambda x, y: x % y, self, other)

    def __rmod__(self, other: Any) -> Expression:
        """
        Reverse modulo operator.

        :param other: The dividend for modulo operation.
        :type other: Any
        :return: A new expression representing the modulo.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = 10 % expr
        """
        return self._func(lambda x, y: x % y, other, self)

    def __pow__(self, power: Any) -> Expression:
        """
        Power operator.

        :param power: The exponent.
        :type power: Any
        :return: A new expression representing the power operation.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = expr ** 2
        """
        return self._func(lambda x, y: x ** y, self, power)

    def __rpow__(self, other: Any) -> Expression:
        """
        Reverse power operator.

        :param other: The base for power operation.
        :type other: Any
        :return: A new expression representing the power operation.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = 2 ** expr
        """
        return self._func(lambda x, y: x ** y, other, self)

    def __pos__(self) -> Expression:
        """
        Unary positive operator.

        :return: A new expression representing the positive value.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = +expr
        """
        return self._func(lambda x: +x, self)

    def __neg__(self) -> Expression:
        """
        Unary negative operator.

        :return: A new expression representing the negative value.
        :rtype: Expression

        Example::

            >>> expr = MathExpression()
            >>> result = -expr
        """
        return self._func(lambda x: -x, self)


class BitwiseExpression(Expression):
    """
    Expression supporting bitwise operations.

    This class provides operators for bitwise logic and shifts.

    .. note::
       Do not combine this class with :class:`LogicalExpression` in a single
       expression chain because both reuse bitwise operators.

    Example::

        >>> from hbutils.expression.native.feature import BitwiseExpression
        >>> from hbutils.expression.native.base import efunc
        >>> expr = BitwiseExpression()
        >>> f = efunc(expr | 0b0011)
        >>> f(0b0100)
        7
    """

    def __or__(self, other: Any) -> Expression:
        """
        Bitwise OR operator.

        :param other: The right operand for bitwise OR.
        :type other: Any
        :return: A new expression representing the bitwise OR.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = expr | 0b1010
        """
        return self._func(lambda x, y: x | y, self, other)

    def __ror__(self, other: Any) -> Expression:
        """
        Reverse bitwise OR operator.

        :param other: The left operand for bitwise OR.
        :type other: Any
        :return: A new expression representing the bitwise OR.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = 0b1010 | expr
        """
        return self._func(lambda x, y: x | y, other, self)

    def __xor__(self, other: Any) -> Expression:
        """
        Bitwise XOR operator.

        :param other: The right operand for bitwise XOR.
        :type other: Any
        :return: A new expression representing the bitwise XOR.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = expr ^ 0b1010
        """
        return self._func(lambda x, y: x ^ y, self, other)

    def __rxor__(self, other: Any) -> Expression:
        """
        Reverse bitwise XOR operator.

        :param other: The left operand for bitwise XOR.
        :type other: Any
        :return: A new expression representing the bitwise XOR.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = 0b1010 ^ expr
        """
        return self._func(lambda x, y: x ^ y, other, self)

    def __and__(self, other: Any) -> Expression:
        """
        Bitwise AND operator.

        :param other: The right operand for bitwise AND.
        :type other: Any
        :return: A new expression representing the bitwise AND.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = expr & 0b1010
        """
        return self._func(lambda x, y: x & y, self, other)

    def __rand__(self, other: Any) -> Expression:
        """
        Reverse bitwise AND operator.

        :param other: The left operand for bitwise AND.
        :type other: Any
        :return: A new expression representing the bitwise AND.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = 0b1010 & expr
        """
        return self._func(lambda x, y: x & y, other, self)

    def __invert__(self) -> Expression:
        """
        Bitwise NOT operator.

        :return: A new expression representing the bitwise NOT.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = ~expr
        """
        return self._func(lambda x: ~x, self)

    def __lshift__(self, other: Any) -> Expression:
        """
        Left shift operator.

        :param other: The number of positions to shift left.
        :type other: Any
        :return: A new expression representing the left shift.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = expr << 2
        """
        return self._func(lambda x, y: x << y, self, other)

    def __rlshift__(self, other: Any) -> Expression:
        """
        Reverse left shift operator.

        :param other: The value to be shifted left.
        :type other: Any
        :return: A new expression representing the left shift.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = 5 << expr
        """
        return self._func(lambda x, y: x << y, other, self)

    def __rshift__(self, other: Any) -> Expression:
        """
        Right shift operator.

        :param other: The number of positions to shift right.
        :type other: Any
        :return: A new expression representing the right shift.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = expr >> 2
        """
        return self._func(lambda x, y: x >> y, self, other)

    def __rrshift__(self, other: Any) -> Expression:
        """
        Reverse right shift operator.

        :param other: The value to be shifted right.
        :type other: Any
        :return: A new expression representing the right shift.
        :rtype: Expression

        Example::

            >>> expr = BitwiseExpression()
            >>> result = 20 >> expr
        """
        return self._func(lambda x, y: x >> y, other, self)
