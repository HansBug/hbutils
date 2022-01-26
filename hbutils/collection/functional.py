__all__ = [
    'nested_map'
]


def nested_map(f, s):
    """
    Overview:

    Arguments:
        - f:
        - s:

    Returns:

    """
    if isinstance(s, dict):
        return type(s)({k: nested_map(f, v) for k, v in s.items()})
    elif isinstance(s, (list, tuple)):
        return type(s)(nested_map(f, v) for v in s)
    else:
        return f(s)
