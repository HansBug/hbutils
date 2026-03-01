"""
Stacked mapping utilities for layered lookup behavior.

This module provides a read-only stacked mapping implementation that allows
multiple mapping-like objects (e.g., dictionaries) to be layered together and
accessed as a single unified mapping. When a key exists in multiple mappings,
the value from the most recently stacked mapping takes precedence.

The module contains the following main component:

* :class:`StackedMapping` - Read-only stacked mapping with layered key lookup

.. note::
   The stacked mapping is read-only. Because it is ambiguous which underlying
   mapping should be modified, item assignment and deletion are intentionally
   unsupported.

Example::

    >>> from hbutils.collection.stacked import StackedMapping
    >>> d1 = {'a': 1, 'b': 2}
    >>> d2 = {'b': 3, 'c': 4, 'd': 5}
    >>> d3 = {'c': 6, 'e': 7}
    >>> s = StackedMapping(d1, d2, d3)  # d3 > d2 > d1
    >>> s['a']
    1
    >>> s['b']
    3
    >>> s['c']
    6
    >>> list(s)
    ['a', 'b', 'c', 'd', 'e']

"""

from collections.abc import Mapping
from typing import Iterator, Tuple, TypeVar

__all__ = [
    'StackedMapping',
]

_KeyType = TypeVar('_KeyType')
_ValueType = TypeVar('_ValueType')


class StackedMapping(Mapping):
    """
    Read-only stacked mapping data structure for layered key lookup.

    Multiple mapping-like objects (such as ``dict``) can be stacked together and
    accessed as a single mapping. When the same key exists in multiple mappings,
    the value from the most recently stacked mapping is returned.

    .. note::
       :class:`StackedMapping` is read-only. The behavior of ``__setitem__`` and
       ``__delitem__`` cannot be defined because it is ambiguous which
       underlying mapping should be modified.

    Example::

        >>> from hbutils.collection import StackedMapping
        >>> d1 = {'a': 1, 'b': 2}
        >>> d2 = {'b': 3, 'c': 4, 'd': 5}
        >>> d3 = {'c': 6, 'e': 7}
        >>> s = StackedMapping(d1, d2, d3)  # d3 > d2 > d1
        >>> list(s.items())
        [('a', 1), ('b', 3), ('c', 6), ('d', 5), ('e', 7)]
        >>> s['c']
        6
        >>> 'f' in s
        False
        >>> len(s)
        5
    """

    def __init__(self, *mps: Mapping) -> None:
        """
        Initialize a stacked mapping instance.

        Later mappings are stacked on top of earlier ones, meaning they take
        precedence when retrieving values for keys that exist in multiple
        mappings.

        :param mps: Mapping objects to stack together, in order of precedence.
        :type mps: Mapping

        Example::

            >>> d1 = {'a': 1}
            >>> d2 = {'b': 2}
            >>> s = StackedMapping(d1, d2)
            >>> len(s)
            2
        """
        self._mps: Tuple[Mapping, ...] = mps

    def __getitem__(self, k: _KeyType) -> _ValueType:
        """
        Get the value associated with the given key.

        This method searches through the stacked mappings in reverse order
        (from last to first), returning the value from the first mapping that
        contains the key.

        :param k: The key to look up.
        :type k: _KeyType
        :return: The value associated with the key.
        :rtype: _ValueType
        :raises KeyError: If the key is not found in any of the stacked mappings.

        Example::

            >>> d1 = {'a': 1}
            >>> d2 = {'a': 2, 'b': 3}
            >>> s = StackedMapping(d1, d2)
            >>> s['a']  # from d2 (last mapping)
            2
            >>> s['b']
            3
        """
        for m in reversed(self._mps):
            try:
                return m[k]
            except KeyError:
                continue

        raise KeyError(k)

    def _key_iter(self) -> Iterator[_KeyType]:
        """
        Iterate over all unique keys in the stacked mappings.

        Keys are yielded in the order they first appear across all mappings.
        Each key is yielded only once, even if it appears in multiple mappings.

        :return: An iterator over all unique keys.
        :rtype: Iterator[_KeyType]

        Example::

            >>> d1 = {'a': 1, 'b': 2}
            >>> d2 = {'b': 3, 'c': 4}
            >>> s = StackedMapping(d1, d2)
            >>> list(s._key_iter())
            ['a', 'b', 'c']
        """
        _exist_keys = set()
        for m in self._mps:
            for k in m.keys():
                if k not in _exist_keys:
                    _exist_keys.add(k)
                    yield k

    def __len__(self) -> int:
        """
        Get the number of unique keys across all stacked mappings.

        :return: The total number of unique keys.
        :rtype: int

        Example::

            >>> d1 = {'a': 1, 'b': 2}
            >>> d2 = {'b': 3, 'c': 4}
            >>> s = StackedMapping(d1, d2)
            >>> len(s)
            3
        """
        return len(list(self._key_iter()))

    def __iter__(self) -> Iterator[_KeyType]:
        """
        Iterate over all unique keys in the stacked mappings.

        :return: An iterator over all unique keys.
        :rtype: Iterator[_KeyType]

        Example::

            >>> d1 = {'a': 1, 'b': 2}
            >>> d2 = {'c': 3}
            >>> s = StackedMapping(d1, d2)
            >>> list(s)
            ['a', 'b', 'c']
        """
        yield from self._key_iter()
