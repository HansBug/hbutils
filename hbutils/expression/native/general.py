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
    Overview:
        General expression.

    Features:
        Inherited from :class:`ComparableExpression`, :class:`IndexedExpression`, :class:`ObjectExpression`, \
        :class:`LogicalExpression` and :class:`MathExpression`.
    """
    pass


def expr(v, cls: Optional[Type[Expression]] = None):
    """
    Overview:
        Transform any objects to :class:`Expression`.

        * If the given ``v`` is an :class:`Expression`, ``v`` will be returned.
        * If the given ``v`` is a callable object, expression with ``v`` will be returned.
        * Otherwise, expression with ``lambda x: v`` will be returned.

    :param v: Original value.
    :param cls: Class of expression, should be a subclass of :class:`Expression`. Default is ``None`` which \
        means :class:`GeneralExpression` will be used.
    :return: Generated expression.
    """
    cls = cls or GeneralExpression
    return getattr(cls, '_expr')(v)


def keep(cls: Optional[Type[Expression]] = None):
    """
    Overview:
        Alias for ``expr(lambda x: x, cls)``.

    :param cls: Class of expression, should be a subclass of :class:`Expression`. Default is ``None`` which \
        means :class:`GeneralExpression` will be used.
    :return: Generated expression.
    """
    return expr(lambda x: x, cls)


def raw(v, cls: Optional[Type[Expression]] = None):
    """
    Overview:
        Alias for ``expr(lambda x: v, cls)``.

    :param v: Raw value.
    :param cls: Class of expression, should be a subclass of :class:`Expression`. Default is ``None`` which \
        means :class:`GeneralExpression` will be used.
    :return: Generated expression.
    """
    return expr(lambda x: v, cls)
