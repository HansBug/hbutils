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
    return list(_g_sq_flatten(s))
