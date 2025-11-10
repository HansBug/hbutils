"""
This module provides a general expression system with various features including comparison, indexing,
object operations, logical operations, and mathematical operations. It offers convenient factory functions
to create expressions from different types of values.

The main components include:
- GeneralExpression: A comprehensive expression class combining multiple expression features
- expr: Factory function to transform objects into expressions
- keep: Factory function to create identity expressions
- raw: Factory function to create constant expressions
"""

from typing import Optional, Type

from .base import Expression
from .feature import ComparableExpression, IndexedExpression, LogicalExpression, MathExpression, ObjectExpression

__all__ = [
    'GeneralExpression',
    'expr', 'keep', 'raw',
]


class GeneralExpression(
    ComparableExpression,
    IndexedExpression,
    ObjectExpression,
    LogicalExpression,
    MathExpression,
):
    """
    A general-purpose expression class that combines multiple expression features.

    This class inherits from multiple expression base classes to provide a comprehensive
    set of operations including comparisons, indexing, object operations, logical operations,
    and mathematical operations.

    Features:
        Inherited from :class:`ComparableExpression`, :class:`IndexedExpression`, :class:`ObjectExpression`,
        :class:`LogicalExpression` and :class:`MathExpression`.

    Example::
        >>> expr_obj = GeneralExpression._expr(lambda x: x + 1)
        >>> # Use the expression object for various operations
    """
    pass


def expr(v, cls: Optional[Type[Expression]] = None):
    """
    Transform any objects to :class:`Expression`.

    This function intelligently converts different types of values into expressions:
    - If the given ``v`` is already an :class:`Expression`, it returns ``v`` unchanged.
    - If the given ``v`` is a callable object, it creates an expression with ``v`` as the transformation function.
    - Otherwise, it creates an expression with ``lambda x: v`` as the transformation function (constant expression).

    :param v: Original value to be converted into an expression. Can be an Expression, callable, or any other value.
    :type v: Any
    :param cls: Class of expression, should be a subclass of :class:`Expression`. Default is ``None`` which
        means :class:`GeneralExpression` will be used.
    :type cls: Optional[Type[Expression]]

    :return: Generated expression object.
    :rtype: Expression

    Example::
        >>> # Create expression from callable
        >>> e1 = expr(lambda x: x * 2)
        >>> # Create expression from constant
        >>> e2 = expr(42)
        >>> # Pass through existing expression
        >>> e3 = expr(e1)
    """
    cls = cls or GeneralExpression
    return getattr(cls, '_expr')(v)


def keep(cls: Optional[Type[Expression]] = None):
    """
    Create an identity expression that returns the input unchanged.

    This is an alias for ``expr(lambda x: x, cls)``, which creates an expression
    that simply passes through its input without any transformation.

    :param cls: Class of expression, should be a subclass of :class:`Expression`. Default is ``None`` which
        means :class:`GeneralExpression` will be used.
    :type cls: Optional[Type[Expression]]

    :return: Generated identity expression.
    :rtype: Expression

    Example::
        >>> identity = keep()
        >>> # The expression will return input unchanged
    """
    return expr(lambda x: x, cls)


def raw(v, cls: Optional[Type[Expression]] = None):
    """
    Create a constant expression that always returns the same value.

    This is an alias for ``expr(lambda x: v, cls)``, which creates an expression
    that ignores its input and always returns the constant value ``v``.

    :param v: Raw value to be returned by the expression, regardless of input.
    :type v: Any
    :param cls: Class of expression, should be a subclass of :class:`Expression`. Default is ``None`` which
        means :class:`GeneralExpression` will be used.
    :type cls: Optional[Type[Expression]]

    :return: Generated constant expression.
    :rtype: Expression

    Example::
        >>> constant = raw(42)
        >>> # The expression will always return 42, regardless of input
    """
    return expr(lambda x: v, cls)
