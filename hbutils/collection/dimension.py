"""
Overview:
    Dimension operations for multi-dimensional array structures.
    
    This module provides utilities for working with nested list/tuple structures
    that represent multi-dimensional arrays (cubes). It includes functions for:
    
    - Determining the shape of cube arrays
    - Switching/transposing dimensions
    - Swapping 2D array dimensions
    
    These operations are useful for manipulating nested data structures without
    requiring external dependencies like NumPy.
"""
__all__ = [
    'cube_shape', 'dimension_switch', 'swap_2d',
]


def _s_cube_shape(c, path):
    """
    Internal recursive function to calculate the shape of a cube array.
    
    :param c: The current level of the nested structure to analyze.
    :type c: list or tuple or any
    :param path: The current path in the nested structure for error reporting.
    :type path: tuple
    
    :return: The shape tuple of the current level and all nested levels.
    :rtype: tuple
    :raises ValueError: If the structure is not a valid cube (inconsistent shapes at the same level).
    """
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
    Get the shape of a cube array (nested list/tuple structure).
    
    This function analyzes a nested list or tuple structure and returns its shape
    as a tuple of dimensions. The structure must be a valid "cube" where all
    elements at the same nesting level have consistent shapes.
    
    :param c: The cube array to analyze (nested list/tuple structure).
    :type c: list or tuple
    
    :return: Shape of the cube as a tuple of dimension sizes.
    :rtype: tuple
    :raises ValueError: If the structure is not a valid cube (inconsistent shapes).
    
    Examples::
        >>> import numpy
        >>> from hbutils.collection import cube_shape
        >>> a = numpy.random.randint(-5, 15, (3, 5, 7, 9)).tolist()
        >>> cube_shape(a)
        (3, 5, 7, 9)
        
        >>> # 2D example
        >>> cube_shape([[1, 2, 3], [4, 5, 6]])
        (2, 3)
        
        >>> # Invalid cube (mismatched dimensions)
        >>> cube_shape([[1, 2], [3, 4, 5]])
        Traceback (most recent call last):
        ...
        ValueError: Mismatching between (0,) and (1,), this is not a cube!
    """
    return _s_cube_shape(c, ())


def dimension_switch(c, dimensions):
    """
    Switch (transpose) the dimensions of a cube array according to a specified order.
    
    This function rearranges the dimensions of a multi-dimensional nested structure
    according to the provided dimension order. It's similar to NumPy's transpose
    operation but works with nested Python lists/tuples.
    
    :param c: Multi-dimensional array (nested list/tuple structure).
    :type c: list or tuple
    :param dimensions: New order of dimensions as a tuple/list of indices (0 to N-1).
                      Each index should appear exactly once.
    :type dimensions: tuple or list
    
    :return: Array with switched dimensions.
    :rtype: list
    :raises ValueError: If dimensions parameter is invalid (missing indices, duplicates, or out of range).
    
    Examples::
        >>> import numpy
        >>> from hbutils.collection import cube_shape, dimension_switch
        >>> a = numpy.random.randint(-5, 15, (3, 5, 7, 9)).tolist()
        >>> cube_shape(a)
        (3, 5, 7, 9)
        >>> b = dimension_switch(a, (3, 0, 2, 1))
        >>> cube_shape(b)
        (9, 3, 7, 5)
        
        >>> # 2D transpose example
        >>> arr = [[1, 2, 3], [4, 5, 6]]
        >>> dimension_switch(arr, (1, 0))
        [[1, 4], [2, 5], [3, 6]]
    """
    shape = cube_shape(c)
    n = len(shape)
    if sorted(set(dimensions)) != list(range(len(shape))):
        raise ValueError(f'Invalid dimensions - {repr(dimensions)}.', dimensions)

    def _recursive(p, path):
        """
        Recursive helper function to build the switched array.
        
        :param p: Current depth level in the recursion.
        :type p: int
        :param path: Current path of indices being built.
        :type path: tuple
        
        :return: Element or nested list at the current recursion level.
        :rtype: any or list
        """
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
    Swap the dimensions of a 2D array (transpose rows and columns).
    
    This is a convenience function that transposes a 2D nested list/tuple structure
    by swapping its two dimensions. It's equivalent to calling dimension_switch(c, (1, 0)).
    
    :param c: 2D array (nested list/tuple structure).
    :type c: list or tuple
    
    :return: Transposed 2D array.
    :rtype: list
    
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
         
        >>> # Simple example
        >>> swap_2d([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
    """
    return dimension_switch(c, (1, 0))
