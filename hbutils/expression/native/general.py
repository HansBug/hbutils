from typing import Optional, Type

from .base import Expression
from .feature import ComparableExpression, IndexedExpression, AttredExpression, LogicalExpression, MathExpression

__all__ = [
    'GeneralExpression',
    'expr', 'keep', 'raw',
]


class GeneralExpression(
    ComparableExpression,
    IndexedExpression,
    AttredExpression,
    LogicalExpression,
    MathExpression,
):
    pass


def expr(v, cls: Optional[Type[Expression]] = None):
    cls = cls or GeneralExpression
    return getattr(cls, '_expr')(v)


def keep(cls: Optional[Type[Expression]] = None):
    return expr(lambda x: x, cls)


def raw(v, cls: Optional[Type[Expression]] = None):
    return expr(lambda x: v, cls)
