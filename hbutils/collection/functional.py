"""
Functional utilities for nested collection processing.

This module provides function-oriented helpers for recursively transforming
nested collection structures such as dictionaries, lists, and tuples. It is
primarily focused on applying a callable to every leaf value in a nested
structure while preserving the original container types and hierarchy.

The module exposes the following public functionality:

* :func:`nested_map` - Apply a callable to all leaf values in a nested structure.

The implementation relies on :func:`hbutils.reflection.dynamic_call` to allow
flexible call signatures for mapping functions, enabling callables that accept
zero, one, or two positional parameters.

Example::

    >>> from hbutils.collection.functional import nested_map
    >>> nested_map(lambda x: x * 2, {'a': [1, 2], 'b': (3, {'c': 4})})
    {'a': [2, 4], 'b': (6, {'c': 8})}
    >>> nested_map(lambda x, p: (x, p), [10, {'k': 20}])
    [(10, (0,)), {'k': (20, (1, 'k'))}]
    >>> nested_map(lambda: 42, (1, 2, 3))
    (42, 42, 42)
"""
from typing import Any, Callable, Tuple

from ..reflection import dynamic_call

__all__ = [
    'nested_map'
]


def nested_map(f: Callable[..., Any], s: Any) -> Any:
    """
    Map a callable over a nested structure.

    This function recursively traverses a nested structure (containing lists,
    tuples, and dictionaries) and applies the given function to each leaf value.
    The callable can optionally accept the path to the current element as a
    parameter. Paths are represented as tuples of keys and indices.

    The callable ``f`` is wrapped by :func:`hbutils.reflection.dynamic_call`,
    which allows it to accept flexible argument counts:

    * ``f()`` will be called with no arguments.
    * ``f(value)`` will be called with the leaf value.
    * ``f(value, path)`` will be called with the leaf value and its path.

    :param f: The function to apply to each leaf value.
    :type f: Callable[..., Any]
    :param s: The nested structure to map over. Supported containers are
              dictionaries, lists, and tuples. All other values are treated as
              leaf values.
    :type s: Any
    :return: A new nested structure with the same container types and hierarchy
             as the input, with the function applied to all leaf values.
    :rtype: Any

    Example::

        >>> from hbutils.collection.functional import nested_map
        >>> nested_map(lambda x: x + 1, [
        ...     2, 3, (4, {'x': 2, 'y': 4}),
        ...     {'a': 3, 'b': (4, 5)},
        ... ])
        [3, 4, (5, {'x': 3, 'y': 5}), {'a': 4, 'b': (5, 6)}]
        >>> nested_map(lambda x, p: (x + 1) * len(p), [
        ...     2, 3, (4, {'x': 2, 'y': 4}),
        ...     {'a': 3, 'b': (4, 5)},
        ... ])
        [3, 4, (10, {'x': 9, 'y': 15}), {'a': 8, 'b': (15, 18)}]
        >>> nested_map(lambda: 233, [
        ...     2, 3, (4, {'x': 2, 'y': 4}),
        ...     {'a': 3, 'b': (4, 5)},
        ... ])
        [233, 233, (233, {'x': 233, 'y': 233}), {'a': 233, 'b': (233, 233)}]
    """
    _df = dynamic_call(f)

    def _recursion(sval: Any, p: Tuple[Any, ...]) -> Any:
        """
        Recursively traverse and map the nested structure.

        :param sval: The current value being processed.
        :type sval: Any
        :param p: The path to the current value (tuple of keys/indices).
        :type p: Tuple[Any, ...]
        :return: The mapped value or structure.
        :rtype: Any
        """
        if isinstance(sval, dict):
            return type(sval)({k: _recursion(v, (*p, k)) for k, v in sval.items()})
        elif isinstance(sval, (list, tuple)):
            return type(sval)(_recursion(v, (*p, i)) for i, v in enumerate(sval))
        else:
            return _df(sval, p)

    return _recursion(s, ())
