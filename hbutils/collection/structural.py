"""
Overview:
    Structural operations.
"""
__all__ = [
    'sq_flatten',
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
