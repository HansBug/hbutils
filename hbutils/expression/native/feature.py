from .base import BaseExpression

__all__ = [
    'CheckExpression',
]


class CheckExpression(BaseExpression):
    def __eq__(self, other):
        return self._func(lambda x, y: x == y, self, other)

    def __ne__(self, other):
        return self._func(lambda x, y: x != y, self, other)
