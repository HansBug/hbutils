"""
Overview:
    Function operations for nested structure.
"""
from ..reflection import dynamic_call

__all__ = [
    'nested_map'
]


def nested_map(f, s):
    """
    Overview:
        Map the nested structure with a function.

    Arguments:
        - f: The given function.
        - s: Nested structure.

    Returns:
        - result: Mapped nested structure.

    Examples::
        >>> from hbutils.collection import nested_map
        >>> nested_map(lambda x: x + 1, [
        ...     2, 3, (4, {'x': 2, 'y': 4}),
        ...     {'a': 3, 'b': (4, 5)},
        ... ])
        [3, 4, (5, {'x': 3, 'y': 5}), {'a': 4, 'b': (5, 6)}]
        >>> nested_map(lambda x, p: (x + 1) *  len(p), [
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

    def _recursion(sval, p):
        if isinstance(sval, dict):
            return type(sval)({k: _recursion(v, (*p, k)) for k, v in sval.items()})
        elif isinstance(sval, (list, tuple)):
            return type(sval)(_recursion(v, (*p, i)) for i, v in enumerate(sval))
        else:
            return _df(sval, p)

    return _recursion(s, ())
