from bisect import bisect_right
from typing import Sequence, Union, Tuple, Callable

__all__ = [
    'linear_map',
]


def linear_map(points: Union[Sequence[float], Sequence[Tuple[float, float]]]) -> Callable[[float], float]:
    """
    Overview:
        Multiple-staged linear gradient calculation based on float number.

    :param points: Points for this linear mapping. If the sequence consists of float numbers, it will be seen as the \
        simple linear mapping. If the elements are binary tuples (contains 2 float numbers), it means the x-range is \
        assigned.
    :return: A callable function for linear mapping.

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
        if xys[0][0] <= x <= xys[-1][0]:
            _index = bisect_right([x_ for x_, _ in xys[:-1]], x) - 1
            x1, y1 = xys[_index]
            x2, y2 = xys[_index + 1]

            r = (x - x1) / (x2 - x1)
            return (1 - r) * y1 + r * y2
        else:
            raise ValueError(f'Invalid x value, [{xys[0][0]!r}, {xys[-1][0]!r}] expected but {x!r} found.')

    return _linear
