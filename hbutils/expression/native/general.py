"""
General expression utilities for native expression building.

This module defines a combined expression class that aggregates comparison,
indexing, object access, logical, and arithmetic behaviors. It also exposes
factory helpers to convert arbitrary values into expression instances, build
identity expressions, or create constant expressions.

The module contains the following public components:

* :class:`GeneralExpression` - Combined expression type with multiple features.
* :func:`expr` - Factory to convert values/callables to expressions.
* :func:`keep` - Factory for identity expressions.
* :func:`raw` - Factory for constant expressions.

Example::

    >>> from hbutils.expression.native.general import GeneralExpression, expr, keep, raw
    >>> e_add = expr(lambda x: x + 1)
    >>> e_id = keep()
    >>> e_const = raw(42)
    >>> # Expressions are composable through their base features.
    >>> getter = expr(lambda d: d["value"])
"""

from typing import Any, Optional, Type

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
    General-purpose expression with combined feature support.

    This class mixes in comparison, indexing, object access, logical, and
    arithmetic behaviors by inheriting from the corresponding feature classes.

    Features included:

    * :class:`~hbutils.expression.native.feature.ComparableExpression`
    * :class:`~hbutils.expression.native.feature.IndexedExpression`
    * :class:`~hbutils.expression.native.feature.ObjectExpression`
    * :class:`~hbutils.expression.native.feature.LogicalExpression`
    * :class:`~hbutils.expression.native.feature.MathExpression`

    Example::

        >>> expr_obj = GeneralExpression._expr(lambda x: x + 1)
        >>> # The resulting expression can be used with all supported operators.
    """
    pass


def expr(v: Any, cls: Optional[Type[Expression]] = None) -> Expression:
    """
    Transform any value into an :class:`Expression` instance.

    This function converts values into expressions using the following rules:

    * If ``v`` is already an :class:`Expression`, it is returned unchanged.
    * If ``v`` is callable, it is wrapped as an expression.
    * Otherwise, a constant expression that returns ``v`` is created.

    :param v: Value to be converted into an expression.
    :type v: Any
    :param cls: Expression class to construct, defaults to ``None`` which
        selects :class:`GeneralExpression`.
    :type cls: Optional[Type[Expression]]
    :return: The generated expression object.
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


def keep(cls: Optional[Type[Expression]] = None) -> Expression:
    """
    Create an identity expression that returns its input unchanged.

    This is an alias for ``expr(lambda x: x, cls)``.

    :param cls: Expression class to construct, defaults to ``None`` which
        selects :class:`GeneralExpression`.
    :type cls: Optional[Type[Expression]]
    :return: Identity expression.
    :rtype: Expression

    Example::

        >>> identity = keep()
        >>> # The expression will return input unchanged
    """
    return expr(lambda x: x, cls)


def raw(v: Any, cls: Optional[Type[Expression]] = None) -> Expression:
    """
    Create a constant expression that always returns the same value.

    This is an alias for ``expr(lambda x: v, cls)`` and ignores its input.

    :param v: Constant value returned by the expression.
    :type v: Any
    :param cls: Expression class to construct, defaults to ``None`` which
        selects :class:`GeneralExpression`.
    :type cls: Optional[Type[Expression]]
    :return: Constant expression.
    :rtype: Expression

    Example::

        >>> constant = raw(42)
        >>> # The expression will always return 42, regardless of input
    """
    return expr(lambda x: v, cls)
