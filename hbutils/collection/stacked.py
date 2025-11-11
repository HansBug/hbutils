"""
Overview:
    This module provides a stacked mapping data structure that allows multiple mapping-like objects 
    (such as dictionaries) to be layered together and accessed as a single unified mapping. 
    Later mappings in the stack take precedence over earlier ones when accessing values.
    
    The StackedMapping class is read-only and does not support item assignment or deletion operations,
    as it would be ambiguous which underlying mapping should be modified.
"""

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
        >>> s = StackedMapping(d1, d2, d3)  # stack together, d3 > d2 > d1
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
        >>> d2['c'] = 11  # update original dicts
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

        Later mappings will be stacked on top of the earlier ones, meaning they take precedence
        when retrieving values for keys that exist in multiple mappings.

        :param mps: Multiple mapping objects to stack together.
        :type mps: Mapping
        
        Example::
            >>> d1 = {'a': 1}
            >>> d2 = {'b': 2}
            >>> s = StackedMapping(d1, d2)
            >>> len(s)
            2
        """
        self._mps = mps

    def __getitem__(self, k: _KeyType) -> _ValueType:
        """
        Get the value associated with the given key.
        
        Searches through the stacked mappings in reverse order (from last to first),
        returning the value from the first mapping that contains the key.

        :param k: The key to look up.
        :type k: _KeyType
        
        :return: The value associated with the key.
        :rtype: _ValueType
        
        :raises KeyError: If the key is not found in any of the stacked mappings.
        
        Example::
            >>> d1 = {'a': 1}
            >>> d2 = {'a': 2, 'b': 3}
            >>> s = StackedMapping(d1, d2)
            >>> s['a']  # Returns value from d2 (last mapping)
            2
            >>> s['b']  # Returns value from d2
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
        Internal method to iterate over all unique keys in the stacked mappings.
        
        Yields keys in the order they first appear across all mappings, ensuring
        each key is yielded only once even if it appears in multiple mappings.

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
            >>> len(s)  # 'a', 'b', 'c' = 3 unique keys
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
