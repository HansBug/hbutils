import unittest

from ...expression import efunc

__all__ = [
    'test_when',
]


def test_when(cond):
    need_test = efunc(cond)(None)
    mark = unittest.skipUnless(need_test, 'Environment requirement is not meet, skipped.')

    def _decorator(fc):
        return mark(fc)

    return _decorator
