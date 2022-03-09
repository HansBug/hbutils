"""
Overview:
    Base interface to quickly implement a comparable object.
"""
import operator as ops

__all__ = [
    'IComparable',
]


class IComparable:
    """
    Overview:
        Interface for a comparable object.

    Examples::
        >>> from hbutils.model import IComparable
        >>> class MyValue(IComparable):
        ...     def __init__(self, v) -> None:
        ...         self._v = v
        ...
        ...     def _cmpkey(self):
        ...         return self._v
        ...

        >>> MyValue(1) == MyValue(1)
        True
        >>> MyValue(1) == MyValue(2)
        False
        >>> MyValue(1) != MyValue(2)
        True
        >>> MyValue(1) > MyValue(2)
        False
        >>> MyValue(1) >= MyValue(2)
        False
        >>> MyValue(1) < MyValue(2)
        True
        >>> MyValue(1) <= MyValue(2)
        True
    """

    def _cmpkey(self):
        """
        Function for getting a key value which is used for comparison.

        :return: A value used to compare.
        """
        raise NotImplementedError  # pragma: no cover

    def _cmpcheck(self, op, other, default=False):
        if type(self) == type(other):
            return op(self._cmpkey(), other._cmpkey())
        else:
            return default

    def __eq__(self, other):
        if self is other:
            return True
        else:
            return self._cmpcheck(ops.__eq__, other, default=False)

    def __ne__(self, other):
        if self is other:
            return False
        else:
            return self._cmpcheck(ops.__ne__, other, default=True)

    def __lt__(self, other):
        return self._cmpcheck(ops.__lt__, other)

    def __le__(self, other):
        return self._cmpcheck(ops.__le__, other)

    def __gt__(self, other):
        return self._cmpcheck(ops.__gt__, other)

    def __ge__(self, other):
        return self._cmpcheck(ops.__ge__, other)
