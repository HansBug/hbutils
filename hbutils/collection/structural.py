"""
Structural operations for nested collection processing.

This module provides utilities for flattening nested sequences and walking through
nested structures composed of dictionaries, lists, and tuples. It exposes functions
to flatten nested sequences into a flat list as well as to traverse nested structures
and retrieve full paths to each leaf element.

The module contains the following public components:

* :func:`sq_flatten` - Recursively flatten a nested sequence into a flat list.
* :func:`nested_walk` - Yield path-value pairs for each leaf element in a nested structure.
* :func:`nested_flatten` - Collect path-value pairs from a nested structure into a list.

Example::

    >>> from hbutils.collection.structural import sq_flatten, nested_walk, nested_flatten
    >>> sq_flatten([1, [2, (3, 4)], 5])
    [1, 2, 3, 4, 5]
    >>> list(nested_walk({'a': 1, 'b': [2, {'c': 3}]}))
    [(('a',), 1), (('b', 0), 2), (('b', 1, 'c'), 3)]
    >>> nested_flatten({'a': 1, 'b': [2, {'c': 3}]})
    [(('a',), 1), (('b', 0), 2), (('b', 1, 'c'), 3)]

"""
from typing import Iterator, Tuple, Union, List, Any

__all__ = [
    'sq_flatten',
    'nested_walk', 'nested_flatten',
]


def _g_sq_flatten(s: Any) -> Iterator[Any]:
    """
    Internal generator for recursively flattening sequences.

    This helper yields each leaf element from a nested structure composed of
    lists and tuples. Non-sequence elements are yielded directly.

    :param s: The object to flatten. Lists and tuples are traversed recursively.
    :type s: Any
    :yield: Individual elements from the flattened sequence.
    :rtype: Iterator[Any]
    """
    if isinstance(s, (list, tuple)):
        for item in s:
            yield from _g_sq_flatten(item)
    else:
        yield s


def sq_flatten(s: Union[list, tuple]) -> List[Any]:
    """
    Flatten a nested sequence into a single-level list.

    This function recursively flattens nested lists and tuples into a single flat list,
    preserving the original traversal order of elements.

    :param s: The given sequence to flatten (can contain nested lists and tuples).
    :type s: Union[list, tuple]
    :return: Flattened sequence as a list.
    :rtype: List[Any]

    Examples::
        >>> from hbutils.collection import sq_flatten
        >>> sq_flatten([1, 2, [3, 4], [5, [6, 7], (8, 9, 10)], 11])
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    """
    return list(_g_sq_flatten(s))


def _nested_walk(s: Any, path: Tuple[Union[int, str], ...]) -> Iterator[Tuple[Tuple[Union[int, str], ...], Any]]:
    """
    Internal recursive function for walking through nested structures.

    This helper traverses dictionaries, lists, and tuples. For each leaf element,
    it yields a tuple containing the path and the element value.

    :param s: The structure to walk through (can be dict, list, tuple, or other types).
    :type s: Any
    :param path: The current path as a tuple of keys/indices.
    :type path: Tuple[Union[int, str], ...]
    :yield: Tuple of (path, value) for each leaf element in the structure.
    :rtype: Iterator[Tuple[Tuple[Union[int, str], ...], Any]]
    """
    if isinstance(s, dict):
        for k, v in s.items():
            yield from _nested_walk(v, (*path, k))
    elif isinstance(s, (list, tuple)):
        for i, v in enumerate(s):
            yield from _nested_walk(v, (*path, i))
    else:
        yield path, s


def nested_walk(s: Any) -> Iterator[Tuple[Tuple[Union[int, str], ...], Any]]:
    """
    Walk through a nested structure and yield paths and values for all leaf elements.

    This function traverses nested dictionaries, lists, and tuples, yielding a tuple
    containing the path (as a tuple of keys/indices) and the value for each leaf element.

    :param s: Given nested structure to walk through.
    :type s: Any
    :return: Iterator yielding tuples of (path, value) for each leaf element.
    :rtype: Iterator[Tuple[Tuple[Union[int, str], ...], Any]]

    Examples::
        >>> from hbutils.collection import nested_walk
        >>> for p, v in nested_walk({'a': 1, 'b': ['c', 'd', {'x': (3, 4), 'y': 'f'}]}):
        ...     print(p, v)
        ...
        ('a',) 1
        ('b', 0) c
        ('b', 1) d
        ('b', 2, 'x', 0) 3
        ('b', 2, 'x', 1) 4
        ('b', 2, 'y') f
    """
    yield from _nested_walk(s, ())


def nested_flatten(s: Any) -> List[Tuple[Tuple[Union[int, str], ...], Any]]:
    """
    Flatten a nested structure into a list of (path, value) tuples.

    This function converts a nested structure (dictionaries, lists, tuples) into a flat list
    where each element is a tuple containing the path to a leaf element and its value.

    :param s: Given nested structure to flatten.
    :type s: Any
    :return: List of tuples containing (path, value) for each leaf element.
    :rtype: List[Tuple[Tuple[Union[int, str], ...], Any]]

    Examples::
        >>> from hbutils.collection import nested_flatten
        >>> print(nested_flatten({'a': 1, 'b': ['c', 'd', {'x': (3, 4), 'y': 'f'}]}))
        [(('a',), 1), (('b', 0), 'c'), (('b', 1), 'd'), (('b', 2, 'x', 0), 3), (('b', 2, 'x', 1), 4), (('b', 2, 'y'), 'f')]
    """
    return list(nested_walk(s))
