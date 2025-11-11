"""
Overview:
    Useful color utilities based on color model.
    
    This module provides utilities for color manipulation including:
    
    - Visual distance calculation between colors
    - Random color generation with visual distinctiveness
    - Linear gradient generation between multiple colors
"""
import math
import random
from typing import Iterator, Union, Sequence, Tuple, Callable

from .model import Color
from ..algorithm import linear_map

__all__ = [
    'visual_distance',
    'rnd_colors',
    'linear_gradient',
]


def _to_color(color: Color):
    """
    Convert input to Color object if it's not already one.
    
    :param color: Color object or color representation.
    :type color: Color
    :return: Color object.
    :rtype: Color
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

    :param c1: First color, can be a Color object or string representation.
    :type c1: Union[Color, str]
    :param c2: Second color, can be a Color object or string representation.
    :type c2: Union[Color, str]
    :return: Distance value representing visual difference between colors.
    :rtype: float

    Examples::
        >>> from hbutils.color import visual_distance, Color
        >>> visual_distance(
        ...     '#ff0000',
        ...     '#00ff00'
        ... )
        2.5495097567963922
        >>> visual_distance(
        ...     '#778800',
        ...     '#887700'
        ... )
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


def _dis_ratio(k):
    """
    Calculate distance ratio based on color index.
    
    This function returns different ratio values based on the index to control
    the minimum distance between colors during random generation.
    
    :param k: Index of the color.
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
        count, lightness=0.5, saturation=1.0, alpha=None,
        init_dis=4.0, lr=0.95, ur=1.5,
        rnd=None
) -> Iterator[Color]:
    """
    Generate random colors that are visually distinct from each other.
    
    This function generates a specified number of colors with controlled visual
    distinctiveness. It uses the HLS color space and ensures generated colors
    maintain a minimum visual distance from previously generated colors.

    :param count: Number of colors to generate.
    :type count: int
    :param lightness: Lightness value in HLS color space (0.0 to 1.0), default is 0.5.
    :type lightness: float
    :param saturation: Saturation value in HLS color space (0.0 to 1.0), default is 1.0.
    :type saturation: float
    :param alpha: Alpha (transparency) value for colors, default is None.
    :type alpha: float, optional
    :param init_dis: Initial minimum distance between colors, default is 4.0.
    :type init_dis: float
    :param lr: Lower ratio for adjusting minimum distance when generation fails, default is 0.95.
    :type lr: float
    :param ur: Upper ratio for adjusting minimum distance when generation succeeds, default is 1.5.
    :type ur: float
    :param rnd: Random number generator instance, default is random.Random(0).
    :type rnd: random.Random, optional
    :return: Iterator yielding Color objects.
    :rtype: Iterator[Color]

    Examples::
        >>> from hbutils.color import rnd_colors
        >>> for c in rnd_colors(12):
        ...     print(c)
        #ff00ee
        #00ff00
        #009cff
        #ff006c
        #c9ff00
        #00f3ff
        #d100ff
        #ffaf00
        #00ff6c
        #4100ff
        #ff5300
        #46ff00

        >>> for c in rnd_colors(12, 0.8, 0.9):
        ...     print(c)
        #fa9ef4
        #9efaa1
        #9eb4fa
        #faa69e
        #c5fa9e
        #9ed6fa
        #f09efa
        #faf89e
        #9ef9fa
        #c09efa
        #fabe9e
        #9efaca
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


def linear_gradient(colors: Union[Sequence[Union[Color, str]], Sequence[Tuple[float, Union[Color, str]]]]) \
        -> Callable[[float], Color]:
    """
    Create a linear gradient function from a sequence of colors.
    
    This function creates a gradient mapping that interpolates linearly between
    the provided colors. Colors can be provided either as a simple sequence
    (evenly distributed) or as position-color tuples for custom positioning.

    :param colors: Sequence of colors or position-color tuples. If simple sequence,
                   colors are evenly distributed from 0 to 1. If tuples, first element
                   is position (float) and second is color.
    :type colors: Union[Sequence[Union[Color, str]], Sequence[Tuple[float, Union[Color, str]]]]
    :return: A function that takes a float parameter and returns the interpolated Color.
    :rtype: Callable[[float], Color]

    Examples::
        - Simple Linear Gradientation

        >>> from hbutils.color import linear_gradient
        >>>
        >>> f = linear_gradient(('red', 'yellow', 'lime'))
        >>> f(0)
        <Color red>
        >>> f(0.25)
        <Color #ff8000>
        >>> f(1 / 3)
        <Color #ffaa00>
        >>> f(0.5)
        <Color yellow>
        >>> f(2 / 3)
        <Color #aaff00>
        >>> f(0.75)
        <Color #80ff00>
        >>> f(1)
        <Color lime>

        - Complex Linear Gradientation

        >>> f = linear_gradient(((-0.2, 'red'), (0.7, '#ffff0044'), (1.1, 'lime')))
        >>> f(-0.2)
        <Color red, alpha: 1.000>
        >>> f(0)
        <Color #ff3900, alpha: 0.837>
        >>> f(0.25)
        <Color #ff8000, alpha: 0.633>
        >>> f(1 / 3)
        <Color #ff9700, alpha: 0.565>
        >>> f(0.5)
        <Color #ffc600, alpha: 0.430>
        >>> f(2 / 3)
        <Color #fff600, alpha: 0.294>
        >>> f(0.7)
        <Color yellow, alpha: 0.267>
        >>> f(0.75)
        <Color #dfff00, alpha: 0.358>
        >>> f(0.8)
        <Color #bfff00, alpha: 0.450>
        >>> f(1)
        <Color #40ff00, alpha: 0.817>
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
        def amap(x):
            """
            Return None for alpha channel when no alpha values are specified.
            
            :param x: Position parameter (unused).
            :type x: float
            :return: None.
            :rtype: None
            """
            return None

    def _gradient(x: float) -> Color:
        """
        Interpolate color at given position.
        
        :param x: Position in the gradient (typically 0.0 to 1.0).
        :type x: float
        :return: Interpolated color at position x.
        :rtype: Color
        """
        return Color((rmap(x), gmap(x), bmap(x)), amap(x))

    return _gradient
