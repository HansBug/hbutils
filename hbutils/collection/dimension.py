__all__ = [
    'cube_shape', 'dimension_switch', 'swap_2d',
]


def _s_cube_shape(c, path):
    if isinstance(c, (list, tuple)):
        n = len(c)
        if n == 0:
            return (0,)
        else:
            first = c[0]
            first_shape = _s_cube_shape(first, (*path, 0))
            for i, item in enumerate(c[1:], start=1):
                item_shape = _s_cube_shape(item, (*path, i))
                if first_shape != item_shape:
                    raise ValueError(f'Mismatching between {repr((*path, 0))} and {repr((*path, 1))}, '
                                     f'this is not a cube!', ((*path, 0), first_shape), ((*path, 1), item_shape))
            return (n, *first_shape)
    else:
        return ()


def cube_shape(c):
    return _s_cube_shape(c, ())


def dimension_switch(c, dimensions):
    shape = cube_shape(c)
    n = len(shape)
    if sorted(set(dimensions)) != list(range(len(shape))):
        raise ValueError(f'Invalid dimensions - {repr(dimensions)}.', dimensions)

    def _recursive(p, path):
        if p >= n:
            actual_path = [None] * n
            for i, di in enumerate(dimensions):
                actual_path[di] = path[i]

            oc = c
            for ip in actual_path:
                oc = oc[ip]
            return oc
        else:
            return [_recursive(p + 1, (*path, i)) for i in range(shape[dimensions[p]])]

    return _recursive(0, ())


def swap_2d(c):
    return dimension_switch(c, (1, 0))
