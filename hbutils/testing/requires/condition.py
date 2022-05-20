import unittest
from typing import Optional

from ...expression import efunc

__all__ = [
    'pre_condition',
]

_DEFAULT_REASON = 'Precondition not satisfied.'


def pre_condition(cond, skip_reason: Optional[str] = None):
    """
    Overview:
        Set pre-condition for the cases of unittest.
        Can be used to both functions and classes.

    :param cond: Condition expression.
    :param skip_reason: Reason when skipping.
    :return: Skip decorator, based on :func:`unittest.skipUnless`.

    .. note::
        See :data:`vpython`, :data:`vpip`, :class:`OS` and :class:`Impl` for actual examples.
    """
    condition = efunc(cond)

    def _decorator(fc):
        mark = unittest.skipUnless(condition(None), skip_reason or _DEFAULT_REASON)
        return mark(fc)

    return _decorator
