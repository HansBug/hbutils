"""
Overview:
    Structural operations module providing utilities for flattening and walking through nested data structures.
    This module includes functions for flattening sequences and nested structures (dictionaries, lists, tuples),
    as well as walking through nested structures to extract paths and values.
"""
from typing import Iterator, Tuple, Union, List

__all__ = [
    'sq_flatten',
    'nested_walk', 'nested_flatten',
]


def _g_sq_flatten(s):
    """
    Internal generator function for recursively flattening sequences.

    :param s: The sequence to flatten (can be list, tuple, or other types).
    :type s: Union[list, tuple, object]

    :yield: Individual elements from the flattened sequence.
    :rtype: Iterator[object]
    """
    if isinstance(s, (list, tuple)):
        for item in s:
            yield from _g_sq_flatten(item)
    else:
        yield s


def sq_flatten(s):
    """
    Flatten a nested sequence into a single-level list.

    This function recursively flattens nested lists and tuples into a single flat list,
    preserving the order of elements.

    :param s: The given sequence to flatten (can contain nested lists and tuples).
    :type s: Union[list, tuple]

    :return: Flattened sequence as a list.
    :rtype: list

    Examples::
        >>> from hbutils.collection import sq_flatten
        >>> sq_flatten([1, 2, [3, 4], [5, [6, 7], (8, 9, 10)], 11])
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    """
    return list(_g_sq_flatten(s))


def _nested_walk(s, path):
    """
    Internal recursive function for walking through nested structures.

    :param s: The structure to walk through (can be dict, list, tuple, or other types).
    :type s: Union[dict, list, tuple, object]
    :param path: The current path as a tuple of keys/indices.
    :type path: tuple

    :yield: Tuple of (path, value) for each leaf element in the structure.
    :rtype: Iterator[Tuple[Tuple[Union[int, str], ...], object]]
    """
    if isinstance(s, dict):
        for k, v in s.items():
            yield from _nested_walk(v, (*path, k))
    elif isinstance(s, (list, tuple)):
        for i, v in enumerate(s):
            yield from _nested_walk(v, (*path, i))
    else:
        yield path, s


def nested_walk(s) -> Iterator[Tuple[Tuple[Union[int, str], ...], object]]:
    """
    Walk through a nested structure and yield paths and values for all leaf elements.

    This function traverses nested dictionaries, lists, and tuples, yielding a tuple
    containing the path (as a tuple of keys/indices) and the value for each leaf element.

    :param s: Given nested structure to walk through.
    :type s: Union[dict, list, tuple, object]

    :return: Iterator yielding tuples of (path, value) for each leaf element.
    :rtype: Iterator[Tuple[Tuple[Union[int, str], ...], object]]

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


def nested_flatten(s) -> List[Tuple[Tuple[Union[int, str], ...], object]]:
    """
    Flatten a nested structure into a list of (path, value) tuples.

    This function converts a nested structure (dictionaries, lists, tuples) into a flat list
    where each element is a tuple containing the path to a leaf element and its value.

    :param s: Given nested structure to flatten.
    :type s: Union[dict, list, tuple, object]

    :return: List of tuples containing (path, value) for each leaf element.
    :rtype: List[Tuple[Tuple[Union[int, str], ...], object]]

    Examples::
        >>> from hbutils.collection import nested_flatten
        >>> print(nested_flatten({'a': 1, 'b': ['c', 'd', {'x': (3, 4), 'y': 'f'}]}))
        [(('a',), 1), (('b', 0), 'c'), (('b', 1), 'd'), (('b', 2, 'x', 0), 3), (('b', 2, 'x', 1), 4), (('b', 2, 'y'), 'f')]
    """
    return list(nested_walk(s))
