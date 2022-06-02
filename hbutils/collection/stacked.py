from collections.abc import Mapping
from typing import Iterator, TypeVar

__all__ = [
    'StackedMapping',
]

_KeyType = TypeVar('_KeyType')
_ValueType = TypeVar('_ValueType')


class StackedMapping(Mapping):
    """
    Overview:
        Stacked mapping data structure.

        Multiple mapping-liked object (such as ``dict``) can be stacked together and accessed like one mapping object.

    .. note::
        :class:`StackedMapping` is readonly. The ``__setitem__`` and ``__delitem__``'s behaviour cannot be defined, \
        because which dict to write or delete can not be determined.

    Examples::
        >>> from hbutils.collection import StackedMapping
        >>>
        >>> d1 = {'a': 1, 'b': 2}
        >>> d2 = {'b': 3, 'c': 4, 'd': 5}
        >>> d3 = {'c': 6, 'e': 7}
        >>> s = StackedMapping(d1, d2, d3)  ## stack together, d3 > d2 > d1
        >>>
        >>> for key, value in s.items():  # __iter__
        ...     print(key, value)
        a 1
        b 3
        c 6
        d 5
        e 7
        >>> s['a']  # __getitem__, from d1['a']
        1
        >>> s['b']  # from d2['b'], d2 > d1
        3
        >>> s['c']  # from d3['c'], d3 > d2
        6
        >>> s['d']  # from d2['d']
        5
        >>> s['e']  # from d3['e']
        7
        >>> 'c' in s  # __contains__
        True
        >>> 'f' in s  # 'f' not found in neither d1, d2 nor d3
        False
        >>> s == {'a': 1, 'b': 3, 'c': 6, 'd': 5, 'e': 7}  # __iter__
        True
        >>> len(s)  # __len__
        5
        >>>
        >>> d2['c'] = 11  ## update original dicts
        >>> del d2['b']
        >>> del d3['c']
        >>> del d1['b']
        >>>
        >>> s['a']  # __getitem__, from d1['a']
        1
        >>> s['b']  # 'b' nor found in neither d1, d2 nor d3
        KeyError: 'b'
        >>> s['c']  # from d2['c']
        11
        >>> s['d']  # from d2['d']
        5
        >>> s['e']  # from d3['e']
        7
        >>> len(s)  # 'b' is no longer here
        4
    """

    def __init__(self, *mps: Mapping):
        """
        Constructor of :class:`StackedMapping`.

        Later mappings will be stacked on top of the earlier ones.

        :param mps: Multiple mapping objects.
        """
        self._mps = mps

    def __getitem__(self, k: _KeyType) -> _ValueType:
        for m in reversed(self._mps):
            try:
                return m[k]
            except KeyError:
                continue

        raise KeyError(k)

    def _key_iter(self):
        _exist_keys = set()
        for m in self._mps:
            for k in m.keys():
                if k not in _exist_keys:
                    _exist_keys.add(k)
                    yield k

    def __len__(self) -> int:
        return len(list(self._key_iter()))

    def __iter__(self) -> Iterator[_KeyType]:
        yield from self._key_iter()
