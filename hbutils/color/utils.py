"""
Overview:
    Useful color utilities based on color model
"""
import math
import random
from typing import Iterator

from .model import Color

__all__ = [
    'visual_distance',
    'rnd_colors',
]


def visual_distance(c1: Color, c2: Color) -> float:
    """
    Overview:
        Get distance of 2 colors.

    Arguments:
        - c1 (:obj:`Color`): First color.
        - c2 (:obj:`Color`): Second color.

    Returns:
        - distance (:obj:`float`): Distance of the colors.

    Examples::
        >>> from hbutils.color import visual_distance, Color
        >>> visual_distance(
        ...     Color.from_hex('#ff0000'),
        ...     Color.from_hex('#00ff00')
        ... )
        2.5495097567963922
        >>> visual_distance(
        ...     Color.from_hex('#778800'),
        ...     Color.from_hex('#887700')
        ... )
        0.16996731711975946
    """
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
    if k < 3:
        return 6.0
    if k < 6:
        return 2.0
    elif k < 8:
        return 0.7
    else:
        return 1.0


def rnd_colors(
        count, lightness=0.5, saturation=1.0,
        init_dis=4.0, lr=0.95, ur=1.5,
        rnd=None
) -> Iterator[Color]:
    """
    Overview:
        Generating random colors which are not similar.

    Arguments:
        - count: Count of colors.
        - lightness: Lightness of the colors (in HLS color space), default is ``0.5``.
        - saturation: Saturation of the colors (in HLS color space), default is ``1.0``.
        - init_dis: Initial distance of colors, default is ``4.0``.
        - lr: Lower ratio when generating, default is ``0.95``.
        - hr: Upper ratio when generating, default is ``1.5``.
        - rnd: Random object to be used, default is ``random.Random(0)``.

    Returns:
        - colors (:obj:`Iterator[Color]`): A iterator of colors.

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

                yield new_color
                break
            else:
                try_cnt += 1
                total_try_cnt += 1
                if try_cnt >= count * 2:
                    min_distance *= lr
                    try_cnt = 0
