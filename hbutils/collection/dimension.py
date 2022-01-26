"""
Overview:
    Dimension operations.
"""
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
    """
    Overview:
        Get the shape of cube array.
        When it is not a cube, raise ``ValueError``.
    Arguments:
        - c: The given cube.

    Returns:
        - shape: Shape of the cube.

    Examples::
        >>> import numpy
        >>> from hbutils.collection import cube_shape
        >>> a = numpy.random.randint(-5, 15, (3, 5, 7, 9)).tolist()
        >>> cube_shape(a)
        (3, 5, 7, 9)
    """
    return _s_cube_shape(c, ())


def dimension_switch(c, dimensions):
    """
    Overview:
        Switch the dimensions of the cube array.
    Arguments:
        - c: Multiple dimensioned array.
        - dimensions: New order of dimensions, should be a tuple of 0 - N-1.

    Returns:
        - switched: Switched array.

    Examples::
        >>> import numpy
        >>> from hbutils.collection import cube_shape, dimension_switch
        >>> a = numpy.random.randint(-5, 15, (3, 5, 7, 9)).tolist()
        >>> cube_shape(a)
        (3, 5, 7, 9)
        >>> b = dimension_switch(a, (3, 0, 2, 1))
        >>> cube_shape(b)
        (9, 3, 7, 5)
    """
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
    """
    Overview:
        Swap 2d array's dimension.
    Arguments:
        - c: 2d array.

    Returns:
        - swapped: Swapped array.

    Examples::
        >>> from hbutils.collection import swap_2d
        >>> swap_2d([
        ...     [9, 6, 4, 11, 5, -2, 1],
        ...     [0, 0, 11, 5, 8, -4, 9],
        ...     [0, 2, 13, 7, 0, 13, 0]
        ... ])
        [[9, 0, 0],
         [6, 0, 2],
         [4, 11, 13],
         [11, 5, 7],
         [5, 8, 0],
         [-2, -4, 13],
         [1, 9, 0]]
    """
    return dimension_switch(c, (1, 0))
