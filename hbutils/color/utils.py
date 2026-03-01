"""
Color utility helpers for perceptual distance, random palettes, and gradients.

This module provides utility functions built on top of :class:`hbutils.color.model.Color`
for common color-related operations:

* :func:`visual_distance` - Perceptual distance between two colors in RGB space
* :func:`rnd_colors` - Generator for visually distinct random colors
* :func:`linear_gradient` - Linear gradient interpolation between multiple colors

The functions are designed to accept :class:`Color` objects, CSS3 color names,
hexadecimal strings, or RGB tuples when appropriate.

Example::

    >>> from hbutils.color import visual_distance, rnd_colors, linear_gradient
    >>>
    >>> visual_distance('red', '#00ff00')
    2.5495097567963922
    >>>
    >>> for c in rnd_colors(3):
    ...     print(c)
    #ff00ee
    #00ff00
    #009cff
    >>>
    >>> grad = linear_gradient(('red', 'yellow', 'lime'))
    >>> grad(0.5)
    <Color yellow>

"""
import math
import random
from typing import Iterator, Union, Sequence, Tuple, Callable, Optional

from .model import Color
from ..algorithm import linear_map

__all__ = [
    'visual_distance',
    'rnd_colors',
    'linear_gradient',
]


def _to_color(color: Union[Color, str, Tuple[float, float, float]]) -> Color:
    """
    Convert a color-like value into a :class:`Color` object.

    The input can be a :class:`Color` instance, a CSS3 name, a hexadecimal
    string, or an RGB tuple. If the input is already a :class:`Color`, it is
    returned as-is; otherwise, a new :class:`Color` is constructed.

    :param color: Color representation to convert.
    :type color: Union[Color, str, Tuple[float, float, float]]
    :return: Converted :class:`Color` object.
    :rtype: Color
    :raises TypeError: If the value is not supported by :class:`Color`.
    :raises ValueError: If a string color is invalid.

    Example::

        >>> from hbutils.color import Color
        >>> _to_color('red')
        <Color red>
        >>> _to_color(Color('#ffffff'))
        <Color white>
    """
    if isinstance(color, Color):
        return color
    else:
        return Color(color)


def visual_distance(c1: Union[Color, str], c2: Union[Color, str]) -> float:
    """
    Calculate the visual distance between two colors.

    This function computes the perceptual distance between two colors using
    a weighted Euclidean distance in RGB space. The weights are based on the
    average red component to account for human perception differences.

    :param c1: First color, can be a :class:`Color` object or string representation.
    :type c1: Union[Color, str]
    :param c2: Second color, can be a :class:`Color` object or string representation.
    :type c2: Union[Color, str]
    :return: Distance value representing visual difference between colors.
    :rtype: float
    :raises TypeError: If either color is an unsupported type.
    :raises ValueError: If a string color is invalid.

    Examples::

        >>> from hbutils.color import visual_distance
        >>> visual_distance('#ff0000', '#00ff00')
        2.5495097567963922
        >>> visual_distance('#778800', '#887700')
        0.16996731711975946
    """
    c1, c2 = _to_color(c1), _to_color(c2)
    rgb1, rgb2 = c1.rgb, c2.rgb
    rmean = (rgb1.red + rgb2.red) / 2
    dr = rgb1.red - rgb2.red
    dg = rgb1.green - rgb2.green
    db = rgb1.blue - rgb2.blue

    return math.sqrt(
        (2 + rmean) * dr * dr +
        4 * dg * dg +
        (3 - rmean) * db * db
    )


def _dis_ratio(k: int) -> float:
    """
    Calculate the distance ratio based on color index.

    This helper adjusts the minimum distance requirement when generating
    random colors to balance distinctiveness and feasibility.

    :param k: Index of the color relative to previously generated colors.
    :type k: int
    :return: Distance ratio value.
    :rtype: float
    """
    if k < 3:
        return 6.0
    if k < 6:
        return 2.0
    elif k < 8:
        return 0.7
    else:
        return 1.0


def rnd_colors(
        count: int,
        lightness: float = 0.5,
        saturation: float = 1.0,
        alpha: Optional[float] = None,
        init_dis: float = 4.0,
        lr: float = 0.95,
        ur: float = 1.5,
        rnd: Optional[random.Random] = None
) -> Iterator[Color]:
    """
    Generate random colors that are visually distinct from each other.

    This generator creates ``count`` colors in HLS space and enforces a
    minimum visual distance between each new color and all previously generated
    colors. When many attempts fail, the minimum distance is relaxed; when
    generation succeeds quickly, the distance is increased.

    :param count: Number of colors to generate.
    :type count: int
    :param lightness: Lightness value in HLS color space (0.0 to 1.0).
    :type lightness: float
    :param saturation: Saturation value in HLS color space (0.0 to 1.0).
    :type saturation: float
    :param alpha: Alpha (transparency) value for colors; ``None`` means no alpha.
    :type alpha: Optional[float]
    :param init_dis: Initial minimum distance between colors.
    :type init_dis: float
    :param lr: Lower ratio for decreasing minimum distance after failures.
    :type lr: float
    :param ur: Upper ratio for increasing minimum distance after successes.
    :type ur: float
    :param rnd: Random number generator instance; if ``None``, ``random.Random(0)`` is used.
    :type rnd: Optional[random.Random]
    :return: Iterator yielding :class:`Color` objects.
    :rtype: Iterator[Color]

    .. note::
       The generator yields colors lazily; iteration triggers the generation.

    Examples::

        >>> from hbutils.color import rnd_colors
        >>> for c in rnd_colors(3):
        ...     print(c)
        #ff00ee
        #00ff00
        #009cff

        >>> for c in rnd_colors(3, 0.8, 0.9):
        ...     print(c)
        #fa9ef4
        #9efaa1
        #9eb4fa
    """
    rnd = rnd or random.Random(0)
    min_distance = init_dis
    _exist_colors = []
    for i in range(count):
        try_cnt, total_try_cnt = 0, 0
        while True:
            new_color = Color.from_hls(rnd.random(), lightness, saturation)
            if not _exist_colors or all(
                    [visual_distance(color_, new_color) >= min_distance * _dis_ratio(i - j)
                     for j, color_ in enumerate(_exist_colors)]):
                _exist_colors.append(new_color)
                if total_try_cnt <= count * 2:
                    min_distance *= ur

                yield Color(new_color, alpha)
                break
            else:
                try_cnt += 1
                total_try_cnt += 1
                if try_cnt >= count * 2:
                    min_distance *= lr
                    try_cnt = 0


def linear_gradient(
        colors: Union[
            Sequence[Union[Color, str, Tuple[float, float, float]]],
            Sequence[Tuple[float, Union[Color, str, Tuple[float, float, float]]]]
        ]
) -> Callable[[float], Color]:
    """
    Create a linear gradient function from a sequence of colors.

    This function creates a gradient mapping that interpolates linearly between
    the provided colors. Colors can be provided either as a simple sequence
    (evenly distributed) or as position-color tuples for custom positioning.

    :param colors: Sequence of colors or position-color tuples. If a simple
                   sequence, colors are evenly distributed from 0 to 1.
                   If tuples, the first element is position and the second
                   is the color.
    :type colors: Union[Sequence[Union[Color, str, Tuple[float, float, float]]], \
Sequence[Tuple[float, Union[Color, str, Tuple[float, float, float]]]]]
    :return: A function that maps a float position to the interpolated color.
    :rtype: Callable[[float], Color]
    :raises AssertionError: If control points are empty or not strictly increasing.
    :raises ZeroDivisionError: If only one control point is provided.
    :raises TypeError: If input is not iterable or contains invalid elements.
    :raises ValueError: If the gradient function is evaluated outside valid range
                        or if any color value is invalid.

    Examples::

        - Simple Linear Gradientation

        >>> from hbutils.color import linear_gradient
        >>>
        >>> f = linear_gradient(('red', 'yellow', 'lime'))
        >>> f(0)
        <Color red>
        >>> f(0.25)
        <Color #ff8000>
        >>> f(0.5)
        <Color yellow>
        >>> f(1)
        <Color lime>

        - Complex Linear Gradientation

        >>> f = linear_gradient(((-0.2, 'red'), (0.7, '#ffff0044'), (1.1, 'lime')))
        >>> f(-0.2)
        <Color red, alpha: 1.000>
        >>> f(0.7)
        <Color yellow, alpha: 0.267>
        >>> f(1.1)
        <Color lime, alpha: 1.000>

    """
    try:
        xys = [(x, _to_color(y)) for x, y in colors]
    except ValueError:
        pts = list(colors)
        n = len(pts)
        xys = [(i / (n - 1), _to_color(y)) for i, y in enumerate(colors)]

    rmap = linear_map([(x, y.rgb.red) for x, y in xys])
    gmap = linear_map([(x, y.rgb.green) for x, y in xys])
    bmap = linear_map([(x, y.rgb.blue) for x, y in xys])
    if any([y.alpha is not None for _, y in xys]):
        amap = linear_map([(x, y.alpha if y.alpha is not None else 1.0) for x, y in xys])
    else:
        # noinspection PyUnusedLocal
        def amap(x: float) -> Optional[float]:
            """
            Return ``None`` for alpha channel when no alpha values are specified.

            :param x: Position parameter (unused).
            :type x: float
            :return: ``None``.
            :rtype: Optional[float]
            """
            return None

    def _gradient(x: float) -> Color:
        """
        Interpolate color at given position.

        :param x: Position in the gradient (typically within the defined range).
        :type x: float
        :return: Interpolated color at position ``x``.
        :rtype: Color
        """
        return Color((rmap(x), gmap(x), bmap(x)), amap(x))

    return _gradient
