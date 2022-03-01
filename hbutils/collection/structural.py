"""
Overview:
    Structural operations.
"""
from typing import Iterator, Tuple, Union, List

__all__ = [
    'sq_flatten',
    'nested_walk', 'nested_flatten',
]


def _g_sq_flatten(s):
    if isinstance(s, (list, tuple)):
        for item in s:
            yield from _g_sq_flatten(item)
    else:
        yield s


def sq_flatten(s):
    """
    Overview:
        Sequence flatten.
    Arguments:
        - s: The given sequence.

    Returns:
        - flatted: Flatted sequence.

    Examples::
        >>> from hbutils.collection import sq_flatten
        >>> sq_flatten([1, 2, [3, 4], [5, [6, 7], (8, 9, 10)], 11])
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    """
    return list(_g_sq_flatten(s))


def _nested_walk(s, path):
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
    Overview:
        Walk for nested structure.

    Arguments:
        - s: Given structure.

    Returns:
        - walk_iter (:obj:`Iterator[Tuple[Tuple[Union[int, str], ...], object]]`): Iterator of the walk result.

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
    Overview:
        Flatten for nested structure.

    Arguments:
        - s: Given structure.

    Returns:
        - flatted (:obj:`List[Tuple[Tuple[Union[int, str], ...], object]]`): List of the flatted result.

    Examples::
        >>> from hbutils.collection import nested_flatten
        >>> print(nested_flatten({'a': 1, 'b': ['c', 'd', {'x': (3, 4), 'y': 'f'}]}))
        [(('a',), 1), (('b', 0), 'c'), (('b', 1), 'd'), (('b', 2, 'x', 0), 3), (('b', 2, 'x', 1), 4), (('b', 2, 'y'), 'f')]
    """
    return list(nested_walk(s))
