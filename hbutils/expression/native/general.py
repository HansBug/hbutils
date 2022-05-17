from typing import Optional, Type

from .base import BaseExpression
from .feature import CheckExpression

__all__ = [
    'GeneralExpression',
    'expr', 'keep',
]


class GeneralExpression(CheckExpression):
    pass


def expr(v, cls: Optional[Type[BaseExpression]] = None):
    cls = cls or GeneralExpression
    return getattr(cls, '_expr')(v)


def keep(cls: Optional[Type[BaseExpression]] = None):
    return expr(lambda x: x, cls)
