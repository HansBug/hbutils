"""
Piecewise linear mapping utilities.

This module provides utilities for creating multi-staged linear gradient mappings
based on float numbers. It exposes a single public factory function,
:func:`linear_map`, which builds a callable piecewise linear mapping from
control points. Control points can be specified as a sequence of y-values with
automatic x-spacing or as explicit ``(x, y)`` tuples.

The module contains the following main components:

* :func:`linear_map` - Create a callable piecewise linear mapping function

.. note::
   When using implicit x-spacing (a sequence of y-values), at least two points
   are required. A single point causes a ``ZeroDivisionError`` because the
   spacing denominator becomes zero.

Example::

    >>> from hbutils.algorithm.linear import linear_map
    >>> # Implicit x-spacing over [0, 1]
    >>> f = linear_map((0.0, 1.0, 0.5))
    >>> f(0.5)
    1.0
    >>> # Explicit x-coordinates
    >>> g = linear_map(((-0.2, 0.0), (0.7, 1.0), (1.1, 0.5)))
    >>> g(0.7)
    1.0
"""

from bisect import bisect_right
from typing import Sequence, Union, Tuple, Callable

__all__ = [
    'linear_map',
]


def linear_map(points: Union[Sequence[float], Sequence[Tuple[float, float]]]) -> Callable[[float], float]:
    """
    Create a multiple-staged linear gradient calculation function based on control points.

    This function generates a piecewise linear mapping function from a sequence of control points.
    The points can be specified in two ways:

    1. Simple sequence of y-values: x-values are automatically distributed evenly from 0 to 1.
       The spacing uses ``i / (n - 1)``, so at least two points are required.
    2. Sequence of ``(x, y)`` tuples: explicit x and y coordinates for each control point.

    The returned callable performs linear interpolation between the neighboring control points.
    If explicit tuples are supplied, the order check uses Python's tuple ordering, which requires
    the sequence of tuples to be strictly increasing lexicographically (typically implying
    strictly increasing x-values; if x-values are equal, the y-values must be strictly increasing).

    :param points: Points for this linear mapping. If the sequence consists of float numbers, it will be seen as the
                   simple linear mapping with x-values automatically distributed from 0 to 1. If the elements are
                   binary tuples (contains 2 float numbers), it means the x-range is assigned explicitly.
    :type points: Union[Sequence[float], Sequence[Tuple[float, float]]]
    :return: A callable function for linear mapping that takes a float x-value and returns the interpolated y-value.
    :rtype: Callable[[float], float]
    :raises AssertionError: If ``points`` is empty or if the control points are not strictly increasing under tuple
                            ordering.
    :raises ZeroDivisionError: If ``points`` contains a single y-value, causing the implicit x-spacing denominator
                               to be zero.
    :raises TypeError: If ``points`` is not iterable or contains elements incompatible with the expected formats.
    :raises ValueError: If the input x-value to the returned function is outside the valid range.

    Examples::
        - Simple Linear Mapping

        >>> from hbutils.algorithm import linear_map
        >>>
        >>> f = linear_map((0, 1, 0.5))
        >>> f(0)
        0.0
        >>> f(0.25)
        0.5
        >>> f(1 / 3)
        0.6666666666666666
        >>> f(0.5)
        1.0
        >>> f(2 / 3)
        0.8333333333333334
        >>> f(0.75)
        0.75
        >>> f(1)
        0.5

        - Complex Linear Mapping (x values are customized)

        >>> f = linear_map(((-0.2, 0), (0.7, 1), (1.1, 0.5)))
        >>> f(-0.2)
        0.0
        >>> f(0)
        0.22222222222222227
        >>> f(0.25)
        0.5000000000000001
        >>> f(1 / 3)
        0.5925925925925927
        >>> f(0.5)
        0.7777777777777778
        >>> f(2 / 3)
        0.9629629629629631
        >>> f(0.7)
        1.0
        >>> f(0.75)
        0.9375
        >>> f(0.8)
        0.875
        >>> f(1)
        0.625
        >>> f(1.1)
        0.5

    """
    assert points, f'Points should be non-empty, but {points!r} found.'

    try:
        xys = [(x, y) for x, y in points]
    except TypeError:
        pts = list(points)
        n = len(pts)
        xys = [(i / (n - 1), y) for i, y in enumerate(points)]

    for i, (x1_, x2_) in enumerate(zip(xys[:-1], xys[1:])):
        assert x1_ < x2_, f'The former x value should be no more than the latter one, ' \
                          f'but {x1_} (at {i}) >= {x2_} (at {i + 1}) found.'

    def _linear(x: float) -> float:
        """
        Perform linear interpolation for the given x-value.

        This internal function performs piecewise linear interpolation based on the control points
        defined in the outer scope. It uses binary search to find the appropriate segment and then
        performs linear interpolation within that segment.

        :param x: The x-coordinate for which to calculate the interpolated y-value.
        :type x: float
        :return: The interpolated y-value at position x.
        :rtype: float
        :raises ValueError: If x is outside the valid range defined by the control points.

        .. note::
           When only a single control point is provided, the internal interpolation attempts to
           divide by zero due to the lack of a valid segment.

        """
        if xys[0][0] <= x <= xys[-1][0]:
            _index = bisect_right([x_ for x_, _ in xys[:-1]], x) - 1
            x1, y1 = xys[_index]
            x2, y2 = xys[_index + 1]

            r = (x - x1) / (x2 - x1)
            return (1 - r) * y1 + r * y2
        else:
            raise ValueError(f'Invalid x value, [{xys[0][0]!r}, {xys[-1][0]!r}] expected but {x!r} found.')

    return _linear
