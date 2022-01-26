"""
Overview:
    Function operations for nested structure.
"""
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
    """
    if isinstance(s, dict):
        return type(s)({k: nested_map(f, v) for k, v in s.items()})
    elif isinstance(s, (list, tuple)):
        return type(s)(nested_map(f, v) for v in s)
    else:
        return f(s)
