"""
Sequence collection utilities for deduplication and grouping operations.

This module provides lightweight helpers for manipulating sequences and
iterables. The focus is on preserving ordering and offering flexible grouping
behavior with optional post-processing of each group.

The module contains the following public functions:

* :func:`unique` - Remove duplicate elements while preserving original order
* :func:`group_by` - Group elements by a key function with optional post-processing

.. note::
   The :func:`unique` function relies on hashing for membership checks. Elements
   must therefore be hashable, and the input sequence type must be constructible
   from a list for the result to be returned with the same type.

Example::

    >>> from hbutils.collection.sequence import unique, group_by
    >>> unique([1, 2, 3, 1, 2])
    [1, 2, 3]
    >>> group_by(['apple', 'pear', 'peach'], key=lambda x: x[0])
    {'a': ['apple'], 'p': ['pear', 'peach']}

"""

from typing import Union, TypeVar, Sequence, Callable, Optional, Dict, List, Iterable

__all__ = [
    'unique',
    'group_by',
]

_ElementType = TypeVar('_ElementType')


def unique(s: Union[Sequence[_ElementType]]) -> Sequence[_ElementType]:
    """
    Remove duplicate elements from a sequence while preserving original order.

    This function iterates through the input sequence, keeping the first
    occurrence of each element. The returned sequence is constructed by calling
    ``type(s)`` on the list of unique items, preserving the original sequence
    type where possible.

    :param s: Original sequence to be deduplicated.
    :type s: Union[Sequence[_ElementType]]
    :return: Unique sequence with the original input type when constructible.
    :rtype: Sequence[_ElementType]
    :raises TypeError: If elements are unhashable or if ``type(s)`` cannot be
        constructed from a list.

    Examples::
        >>> from hbutils.collection import unique
        >>>
        >>> unique([1, 2, 3, 1])
        [1, 2, 3]
        >>> unique(('a', 'b', 'a', 'c', 'd', 'e', 'b'))
        ('a', 'b', 'c', 'd', 'e')
        >>> unique([3, 1, 2, 1, 4, 3])
        [3, 1, 2, 4]
    """
    _set, _result = set(), []
    for element in s:
        if element not in _set:
            _result.append(element)
            _set.add(element)

    return type(s)(_result)


_GroupType = TypeVar('_GroupType')
_ResultType = TypeVar('_ResultType')


def group_by(s: Iterable[_ElementType],
             key: Callable[[_ElementType], _GroupType],
             gfunc: Optional[Callable[[List[_ElementType]], _ResultType]] = None) -> Dict[_GroupType, _ResultType]:
    """
    Group iterable elements by a key function with optional post-processing.

    Elements from the input iterable are collected into lists keyed by the
    result of ``key``. If ``gfunc`` is provided, each group list is passed to
    this function and the returned value is used as the group result. When
    ``gfunc`` is ``None``, the raw lists are returned.

    :param s: Elements to be grouped.
    :type s: Iterable[_ElementType]
    :param key: Callable that computes the grouping key for each element.
    :type key: Callable[[_ElementType], _GroupType]
    :param gfunc: Optional post-processing function for each group. If ``None``,
        group values are returned as raw lists. Defaults to ``None``.
    :type gfunc: Optional[Callable[[List[_ElementType]], _ResultType]]
    :return: Dictionary mapping group keys to processed group values.
    :rtype: Dict[_GroupType, _ResultType]

    Examples::
        >>> from hbutils.collection import group_by
        >>>
        >>> foods = [
        ...     'apple', 'orange', 'pear',
        ...     'banana', 'fish', 'pork', 'milk',
        ... ]
        >>> group_by(foods, len)  # group by length
        {5: ['apple'], 6: ['orange', 'banana'], 4: ['pear', 'fish', 'pork', 'milk']}
        >>> group_by(foods, len, len)  # group and get length
        {5: 1, 6: 2, 4: 4}
        >>> group_by(foods, lambda x: x[0])  # group by first letter
        {'a': ['apple'], 'o': ['orange'], 'p': ['pear', 'pork'], 'b': ['banana'], 'f': ['fish'], 'm': ['milk']}
        >>> group_by(foods, lambda x: x[0], len)  # group and get length
        {'a': 1, 'o': 1, 'p': 2, 'b': 1, 'f': 1, 'm': 1}
    """
    gfunc = gfunc or (lambda x: x)

    _result_dict: Dict[_GroupType, List[_ElementType]] = {}
    for item in s:
        _item_key = key(item)
        if _item_key not in _result_dict:
            _result_dict[_item_key] = []
        _result_dict[_item_key].append(item)

    return {
        key: gfunc(grps)
        for key, grps in _result_dict.items()
    }
