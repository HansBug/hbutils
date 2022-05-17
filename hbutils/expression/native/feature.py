from .base import BaseExpression

__all__ = [
    'CheckExpression',
    'ComparableExpression',
]


class CheckExpression(BaseExpression):
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
