"""
Overview:
    Color model, include rgb, hsv, hls color system.
    
    More color system will be supported soon.
"""
import colorsys
import math
import re
from typing import Optional, Union, Tuple

from .base import _name_to_hex, _CSS3_NAME_MAPS
from ..reflection.func import post_process, raising, freduce, dynamic_call, warning_

__all__ = ['Color']


def _round_mapper(min_: float, max_: float):
    min_, max_ = min(min_, max_), max(min_, max_)
    round_ = max_ - min_

    def _func(v):
        if v < min_:
            v += math.ceil((min_ - v) / round_) * round_
        if v > max_:
            v -= math.ceil((v - max_) / round_) * round_

        return v

    return _func


def _range_mapper(min_: Optional[float], max_: Optional[float], warning=None):
    if min_ is not None and max_ is not None:
        min_, max_ = min(min_, max_), max(min_, max_)
    warning = dynamic_call(warning_(warning if warning is not None else lambda: None))

    def _func(v):
        if max_ is not None and v > max_:
            warning(v, min_, max_)
            return max_
        elif min_ is not None and v < min_:
            warning(v, min_, max_)
            return min_
        else:
            return v

    return _func


class GetSetProxy:
    def __init__(self, getter, setter=None):
        self.__getter = getter
        self.__setter = setter or raising(lambda x: NotImplementedError)

    def set(self, value):
        return self.__setter(value)

    def get(self):
        return self.__getter()


_r_mapper = _range_mapper(0.0, 1.0, lambda v, min_, max_: Warning(
    'Red value should be no less than %.3d and no more than %.3d, but %.3d found.' % (min_, max_, v)))
_g_mapper = _range_mapper(0.0, 1.0, lambda v, min_, max_: Warning(
    'Green value should be no less than %.3d and no more than %.3d, but %.3d found.' % (min_, max_, v)))
_b_mapper = _range_mapper(0.0, 1.0, lambda v, min_, max_: Warning(
    'Blue value should be no less than %.3d and no more than %.3d, but %.3d found.' % (min_, max_, v)))
_a_mapper = _range_mapper(0.0, 1.0, lambda v, min_, max_: Warning(
    'Alpha value should be no less than %.3d and no more than %.3d, but %.3d found.' % (min_, max_, v)))


class RGBColorProxy:
    """
    Overview:
        Color proxy for RGB space.
    """

    def __init__(self, this: 'Color', r: GetSetProxy, g: GetSetProxy, b: GetSetProxy):
        """
        Constructor of :class:`RGBColorProxy`.

        :param this: Original color object.
        :param r: Get-set proxy for red.
        :param g: Get-set proxy for green.
        :param b: Get-set proxy for blue.
        """
        self.__this = this
        self.__rp = r
        self.__gp = g
        self.__bp = b

    @property
    def red(self) -> float:
        """
        Red value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__rp.get()

    @red.setter
    def red(self, new: float):
        self.__rp.set(new)

    @property
    def green(self) -> float:
        """
        Green value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__gp.get()

    @green.setter
    def green(self, new: float):
        self.__gp.set(new)

    @property
    def blue(self) -> float:
        """
        Blue value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__bp.get()

    @blue.setter
    def blue(self, new: float):
        self.__bp.set(new)

    def __iter__(self):
        """
        Iterator for this proxy.

        Examples::
            >>> from hbutils.color import Color
            >>>
            >>> c = Color('green')
            >>> r, g, b = c.rgb
            >>> print(r, g, b)
            0.0 0.5019607843137255 0.0
        """
        yield self.red
        yield self.green
        yield self.blue

    def __repr__(self):
        """
        Representation format.

        Examples::
            >>> from hbutils.color import Color
            >>>
            >>> c = Color('green')
            >>> c.rgb
            <RGBColorProxy red: 0.000, green: 0.502, blue: 0.000>
        """
        return '<{cls} red: {red}, green: {green}, blue: {blue}>'.format(
            cls=self.__class__.__name__,
            red='%.3f' % (self.red,),
            green='%.3f' % (self.green,),
            blue='%.3f' % (self.blue,),
        )


_hsv_h_mapper = _round_mapper(0.0, 1.0)
_hsv_s_mapper = _range_mapper(0.0, 1.0, lambda v, min_, max_: Warning(
    'Saturation value should be no less than %.3d and no more than %.3d, but %.3d found.' % (min_, max_, v)))
_hsv_v_mapper = _range_mapper(0.0, 1.0, lambda v, min_, max_: Warning(
    'Brightness(value) value should be no less than %.3d and no more than %.3d, but %.3d found.' % (min_, max_, v)))


class HSVColorProxy:
    """
    Overview:
        Color proxy for HSV space.
    """

    def __init__(self, this: 'Color', h: GetSetProxy, s: GetSetProxy, v: GetSetProxy):
        """
        Constructor of :class:`HSVColorProxy`.

        :param this: Original color object.
        :param h: Get-set proxy for hue.
        :param s: Get-set proxy for saturation.
        :param v: Get-set proxy for value.
        """
        this.__this = this
        self.__hp = h
        self.__sp = s
        self.__vp = v

    @property
    def hue(self) -> float:
        """
        Hue value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__hp.get()

    @hue.setter
    def hue(self, new: float):
        self.__hp.set(new)

    @property
    def saturation(self) -> float:
        """
        Saturation value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__sp.get()

    @saturation.setter
    def saturation(self, new: float):
        self.__sp.set(new)

    @property
    def value(self) -> float:
        """
        Value value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__vp.get()

    @value.setter
    def value(self, new: float):
        self.__vp.set(new)

    @property
    def brightness(self) -> float:
        """
        Alias for ``value``.
        """
        return self.value

    @brightness.setter
    def brightness(self, new: float):
        self.value = new

    def __iter__(self):
        """
        Iterator for this proxy.

        Examples::
            >>> from hbutils.color import Color
            >>>
            >>> c = Color('green')
            >>> h, s, v = c.hsv
            >>> print(h, s, v)
            0.3333333333333333 1.0 0.5019607843137255
        """
        yield self.hue
        yield self.saturation
        yield self.value

    def __repr__(self):
        """
        Representation format.

        Examples::
            >>> from hbutils.color import Color
            >>>
            >>> c = Color('green')
            >>> c.hsv
            <HSVColorProxy hue: 0.333, saturation: 1.000, value: 0.502>
        """
        return '<{cls} hue: {hue}, saturation: {saturation}, value: {value}>'.format(
            cls=self.__class__.__name__,
            hue='%.3f' % (self.hue,),
            saturation='%.3f' % (self.saturation,),
            value='%.3f' % (self.value,),
        )


_hls_h_mapper = _round_mapper(0.0, 1.0)
_hls_l_mapper = _range_mapper(0.0, 1.0, lambda v, min_, max_: Warning(
    'Lightness value should be no less than %.3d and no more than %.3d, but %.3d found.' % (min_, max_, v)))
_hls_s_mapper = _range_mapper(0.0, 1.0, lambda v, min_, max_: Warning(
    'Saturation value should be no less than %.3d and no more than %.3d, but %.3d found.' % (min_, max_, v)))


class HLSColorProxy:
    """
    Overview:
        Color proxy for HLS space.
    """

    def __init__(self, this: 'Color', h: GetSetProxy, l: GetSetProxy, s: GetSetProxy):
        """
        Constructor of :class:`HLSColorProxy`.

        :param this: Original color object.
        :param h: Get-set proxy for hue.
        :param l: Get-set proxy for lightness.
        :param s: Get-set proxy for saturation.
        """
        this.__this = this
        self.__hp = h
        self.__lp = l
        self.__sp = s

    @property
    def hue(self) -> float:
        """
        Hue value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__hp.get()

    @hue.setter
    def hue(self, new: float):
        self.__hp.set(new)

    @property
    def lightness(self) -> float:
        """
        Lightness value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__lp.get()

    @lightness.setter
    def lightness(self, new: float):
        self.__lp.set(new)

    @property
    def saturation(self) -> float:
        """
        Saturation value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        """
        return self.__sp.get()

    @saturation.setter
    def saturation(self, new: float):
        self.__sp.set(new)

    def __iter__(self):
        """
        Iterator for this proxy.

        Examples::
            >>> from hbutils.color import Color
            >>>
            >>> c = Color('green')
            >>> h, l, s = c.hls
            >>> print(h, l, s)
            0.3333333333333333 0.25098039215686274 1.0
        """
        yield self.hue
        yield self.lightness
        yield self.saturation

    def __repr__(self):
        """
        Representation format.

        Examples::
            >>> from hbutils.color import Color
            >>>
            >>> c = Color('green')
            >>> c.hls
            <HLSColorProxy hue: 0.333, lightness: 0.251, saturation: 1.000>
        """
        return '<{cls} hue: {hue}, lightness: {lightness}, saturation: {saturation}>'.format(
            cls=self.__class__.__name__,
            hue='%.3f' % (self.hue,),
            lightness='%.3f' % (self.lightness,),
            saturation='%.3f' % (self.saturation,),
        )


_ratio_to_255 = lambda x: int(round(x * 255))
_ratio_to_hex = post_process(lambda x: '%02x' % (x,))(_ratio_to_255)
_hex_to_255 = lambda x: int(x, base=16) if x is not None else None
_hex_to_ratio = post_process(lambda x: x / 255.0 if x is not None else None)(_hex_to_255)

_RGB_COLOR_PATTERN = re.compile(r'^#?([a-fA-F\d]{2})([a-fA-F\d]{2})([a-fA-F\d]{2})([a-fA-F\d]{2}|)$')


@freduce(init=None)
def _ratio_or(a, b):
    return b if a is None else a


class Color:
    """
    Overview:
        Color utility object.

    Examples::
        >>> from hbutils.color import Color
        >>>
        >>> c = Color('red')  # from name
        >>> c
        <Color red>
        >>> str(c)  # hex format
        '#ff0000'
        >>> (c.rgb.red, c.rgb.green, c.rgb.blue)            # rgb format
        (1.0, 0.0, 0.0)
        >>> (c.hls.hue, c.hls.lightness, c.hls.saturation)  # hls format
        (0.0, 0.5, 1.0)
        >>> (c.hsv.hue, c.hsv.value, c.hsv.saturation)      # hsv format
        (0.0, 1.0, 1.0)


        >>> c1 = Color('#56a3f0')  # from hex
        >>> c1
        <Color #56a3f0>
        >>> str(c1)  # hex format
        '#56a3f0'
        >>> (c1.rgb.red, c1.rgb.green, c1.rgb.blue)            # rgb format
        (0.33725490196078434, 0.6392156862745098, 0.9411764705882353)
        >>> (c1.hls.hue, c1.hls.lightness, c1.hls.saturation)  # hls format
        (0.5833333333333334, 0.6392156862745098, 0.8369565217391304)
        >>> (c1.hsv.hue, c1.hsv.value, c1.hsv.saturation)      # hsv format
        (0.5833333333333334, 0.9411764705882353, 0.6416666666666666)


        >>> c2 = Color('#56a3f077')  # from hex
        >>> c2
        <Color #56a3f0, alpha: 0.467>
        >>> c2.alpha  # alpha value
        0.4666666666666667
        >>> str(c2)   # hex format
        '#56a3f077'
    """

    def __init__(self, c: Union[str, Tuple[float, float, float], 'Color'], alpha: Optional[float] = None):
        """
        Overview:
            Constructor of ``Color``.

        Arguments:
            - c (:obj:`Union[str, Tuple[float, float, float]]`): Color value, can be hex string value \
                or tuple rgb value.
            - alpha: (:obj:`Optional[float]`): Alpha value of color, \
                default is `None` which means no alpha value.
        """
        if isinstance(c, tuple):
            self.__r, self.__g, self.__b = _r_mapper(c[0]), _g_mapper(c[1]), _b_mapper(c[2])
            self.__alpha = _a_mapper(alpha) if alpha is not None else None
        elif isinstance(c, Color):
            self.__init__(str(c), alpha)
        elif isinstance(c, str):
            if _RGB_COLOR_PATTERN.fullmatch(c):
                _rgb_hex = c
            else:
                try:
                    _rgb_hex = _name_to_hex(c)
                except ValueError:
                    raise ValueError("Invalid string color, matching of pattern {pattern} or english name "
                                     "expected but {actual} found.".format(pattern=repr(_RGB_COLOR_PATTERN.pattern),
                                                                           actual=repr(c), ))

            _finding = _RGB_COLOR_PATTERN.findall(_rgb_hex)
            _first = _finding[0]
            rs, gs, bs, as_ = _first
            as_ = None if not as_ else as_

            r, g, b, a = map(_hex_to_ratio, (rs, gs, bs, as_))
            if alpha is not None:
                a = alpha

            self.__init__((r, g, b), a)

        else:
            raise TypeError('Unknown color value - {c}.'.format(c=repr(c)))

    @property
    def alpha(self) -> Optional[float]:
        """
        Alpha value, which means the transparent ratio (within :math:`\\left[0.0, 1.0\\right]`).

        :: note::
            Setter is available.
        """
        return self.__alpha

    @alpha.setter
    def alpha(self, new: Optional[float]):
        if new is not None:
            new = _a_mapper(new)
        self.__alpha = new

    def __get_rgb(self):
        return self.__r, self.__g, self.__b

    def __set_rgb(self, r=None, g=None, b=None):
        self.__r, self.__g, self.__b = map(lambda args: _ratio_or(*args), zip((r, g, b), self.__get_rgb()))

    @property
    def rgb(self) -> RGBColorProxy:
        """
        Overview:
            Get rgb color system based color proxy.
            See :class:`RGBColorProxy`.

        Returns:
            - proxy (:obj:`RGBColorProxy`): Rgb color proxy.
        """
        return RGBColorProxy(
            self,
            GetSetProxy(
                lambda: self.__r,
                lambda x: self.__set_rgb(r=_r_mapper(x)),
            ),
            GetSetProxy(
                lambda: self.__g,
                lambda x: self.__set_rgb(g=_g_mapper(x)),
            ),
            GetSetProxy(
                lambda: self.__b,
                lambda x: self.__set_rgb(b=_b_mapper(x)),
            ),
        )

    def __get_hsv(self):
        return colorsys.rgb_to_hsv(self.__r, self.__g, self.__b)

    def __set_hsv(self, h=None, s=None, v=None):
        h, s, v = map(lambda args: _ratio_or(*args), zip((h, s, v), self.__get_hsv()))
        self.__r, self.__g, self.__b = colorsys.hsv_to_rgb(h, s, v)

    @property
    def hsv(self) -> HSVColorProxy:
        """
        Overview:
            Get hsv color system based color proxy.
            See :class:`HSVColorProxy`.

        Returns:
            - proxy (:obj:`HSVColorProxy`): Hsv color proxy.
        """
        return HSVColorProxy(
            self,
            GetSetProxy(
                lambda: self.__get_hsv()[0],
                lambda x: self.__set_hsv(h=_hsv_h_mapper(x)),
            ),
            GetSetProxy(
                lambda: self.__get_hsv()[1],
                lambda x: self.__set_hsv(s=_hsv_s_mapper(x)),
            ),
            GetSetProxy(
                lambda: self.__get_hsv()[2],
                lambda x: self.__set_hsv(v=_hsv_v_mapper(x)),
            ),
        )

    def __get_hls(self):
        return colorsys.rgb_to_hls(self.__r, self.__g, self.__b)

    def __set_hls(self, h=None, l_=None, s=None):
        h, l, s = map(lambda args: _ratio_or(*args), zip((h, l_, s), self.__get_hls()))
        self.__r, self.__g, self.__b = colorsys.hls_to_rgb(h, l, s)

    @property
    def hls(self) -> HLSColorProxy:
        """
        Overview:
            Get hls color system based color proxy.
            See :class:`HLSColorProxy`.

        Returns:
            - proxy (:obj:`HLSColorProxy`): Hls color proxy.
        """
        return HLSColorProxy(
            self,
            GetSetProxy(
                lambda: self.__get_hls()[0],
                lambda x: self.__set_hls(h=_hls_h_mapper(x)),
            ),
            GetSetProxy(
                lambda: self.__get_hls()[1],
                lambda x: self.__set_hls(l_=_hls_l_mapper(x)),
            ),
            GetSetProxy(
                lambda: self.__get_hls()[2],
                lambda x: self.__set_hls(s=_hls_s_mapper(x)),
            ),
        )

    def __get_hex(self, include_alpha: bool):
        rs, gs, bs = _ratio_to_hex(self.__r), _ratio_to_hex(self.__g), _ratio_to_hex(self.__b)
        as_ = _ratio_to_hex(self.__alpha) if self.__alpha is not None and include_alpha else ''

        return '#' + rs + gs + bs + as_

    def __get_name(self):
        _hex = self.__get_hex(False).lower()
        return _CSS3_NAME_MAPS.get(_hex, _hex)

    def __repr__(self):
        if self.__alpha is not None:
            return '<{cls} {hex}, alpha: {alpha}>'.format(
                cls=self.__class__.__name__,
                hex=self.__get_name(),
                alpha='%.3f' % (self.__alpha,),
            )
        else:
            return '<{cls} {hex}>'.format(
                cls=self.__class__.__name__,
                hex=self.__get_name(),
            )

    def __str__(self):
        """
        Hex format of this :class:`Color` object.
        """
        return self.__get_hex(True)

    def __getstate__(self) -> Tuple[float, float, float, Optional[float]]:
        """
        Overview:
            Dump color as pickle object.

        Returns:
            - info (:obj:`Tuple[float, float, float, Optional[float]]`): Dumped data object.
        """
        return self.__r, self.__g, self.__b, self.__alpha

    def __setstate__(self, v: Tuple[float, float, float, Optional[float]]):
        """
        Overview:
            Load color from pickle object.

        Args:
            - v (:obj:`Tuple[float, float, float, Optional[float]]`): Dumped data object.
        """
        self.__r, self.__g, self.__b, self.__alpha = v

    def __hash__(self):
        """
        Overview:
            Get hash value of current object.

        Returns:
            - hash (:obj:`int`): Hash value of current color.
        """
        return hash(self.__getstate__())

    def __eq__(self, other):
        """
        Overview:
            Get equality between colors.

        Arguments:
            - other: Another object.

        Returns:
            - equal (:obj:`bool`): Equal or not.
        """
        if other is self:
            return True
        elif type(other) == type(self):
            return other.__getstate__() == self.__getstate__()
        else:
            return False

    @classmethod
    def from_rgb(cls, r, g, b, alpha=None) -> 'Color':
        """
        Overview:
            Load color from rgb system.

        Arguments:
            - r (:obj:`float`): Red value, should be a float value in :math:`\\left[0, 1\\right)`.
            - g (:obj:`float`): Green value, should be a float value in :math:`\\left[0, 1\\right]`.
            - b (:obj:`float`): Blue value, should be a float value in :math:`\\left[0, 1\\right]`.
            - alpha (:obj:`Optional[float]`): Alpha value, should be a float value \
                in :math:`\\left[0, 1\\right]`, default is None which means no alpha value is used.

        Returns:
            - color (:obj:`Color`): Color object.
        """
        return cls((r, g, b), alpha)

    @classmethod
    def from_hex(cls, hex_: str) -> 'Color':
        r"""
        Overview:
            Load color from hexadecimal rgb string.

        Arguments:
            - hex\_ (:obj:`str`): Hexadecimal string, maybe starts with ``#``.

        Returns:
            - color (:obj:`Color`): Color object.
        """
        return cls(hex_)

    @classmethod
    def from_hsv(cls, h, s, v, alpha=None) -> 'Color':
        """
        Overview:
            Load color from hsv system.

        Arguments:
            - h (:obj:`float`): Hue value, should be a float value in :math:`\\left[0, 1\\right)`.
            - s (:obj:`float`): Saturation value, should be a float value in :math:`\\left[0, 1\\right]`.
            - v (:obj:`float`): Brightness (value) value, should be a float value \
                in :math:`\\left[0, 1\\right]`.
            - alpha (:obj:`Optional[float]`): Alpha value, should be a float value \
                in :math:`\\left[0, 1\\right]`, default is None which means no alpha value is used.

        Returns:
            - color (:obj:`Color`): Color object.
        """
        return cls(colorsys.hsv_to_rgb(h, s, v), alpha)

    @classmethod
    def from_hls(cls, h: float, l: float, s: float, alpha: Optional[float] = None) -> 'Color':
        """
        Overview:
            Load color from hls system.

        Arguments:
            - h (:obj:`float`): Hue value, should be a float value in :math:`\\left[0, 1\\right)`.
            - l (:obj:`float`): Lightness value, should be a float value in :math:`\\left[0, 1\\right]`.
            - s (:obj:`float`): Saturation value, should be a float value in :math:`\\left[0, 1\\right]`.
            - alpha (:obj:`Optional[float]`): Alpha value, should be a float value \
                in :math:`\\left[0, 1\\right]`, default is None which means no alpha value is used.

        Returns:
            - color (:obj:`Color`): Color object.
        """
        return cls(colorsys.hls_to_rgb(h, l, s), alpha)
