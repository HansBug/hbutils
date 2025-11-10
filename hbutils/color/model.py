"""
Overview:
    Color model, include rgb, hsv, hls color system.
    
    More color system will be supported soon.
"""
import colorsys
import math
import re
from typing import Optional, Union, Tuple, Callable

from .base import _name_to_hex, _CSS3_NAME_MAPS
from ..reflection.func import post_process, raising, freduce, dynamic_call, warning_

__all__ = ['Color']


def _round_mapper(min_: float, max_: float) -> Callable[[float], float]:
    """
    Create a mapper function that rounds values to a specified range.

    :param min_: Minimum value of the range.
    :type min_: float
    :param max_: Maximum value of the range.
    :type max_: float
    :return: A function that maps input values to the specified range.
    :rtype: Callable[[float], float]
    
    Example::
        >>> mapper = _round_mapper(0.0, 1.0)
        >>> mapper(1.5)  # Value greater than max
        0.5
        >>> mapper(-0.5)  # Value less than min
        0.5
    """
    min_, max_ = min(min_, max_), max(min_, max_)
    round_ = max_ - min_

    def _func(v):
        if v < min_:
            v += math.ceil((min_ - v) / round_) * round_
        if v > max_:
            v -= math.ceil((v - max_) / round_) * round_

        return v

    return _func


def _range_mapper(min_: Optional[float], max_: Optional[float], warning: Optional[Callable] = None) -> Callable[
    [float], float]:
    """
    Create a mapper function that clamps values to a specified range with optional warning.

    :param min_: Minimum value of the range, or None for no minimum limit.
    :type min_: Optional[float]
    :param max_: Maximum value of the range, or None for no maximum limit.
    :type max_: Optional[float]
    :param warning: Optional warning function to call when value is out of range.
    :type warning: Optional[Callable]
    :return: A function that clamps input values to the specified range.
    :rtype: Callable[[float], float]
    
    Example::
        >>> mapper = _range_mapper(0.0, 1.0)
        >>> mapper(1.5)  # Value greater than max
        1.0
        >>> mapper(-0.5)  # Value less than min
        0.0
    """
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
    """
    Overview:
        A proxy class that provides getter and setter functionality.
    """

    def __init__(self, getter: Callable, setter: Optional[Callable] = None):
        """
        Initialize the GetSetProxy.

        :param getter: Function to get the value.
        :type getter: Callable
        :param setter: Optional function to set the value. If None, setter will raise NotImplementedError.
        :type setter: Optional[Callable]
        """
        self.__getter = getter
        self.__setter = setter or raising(lambda x: NotImplementedError)

    def set(self, value):
        """
        Set the value using the setter function.

        :param value: Value to set.
        :return: Result of the setter function.
        """
        return self.__setter(value)

    def get(self):
        """
        Get the value using the getter function.

        :return: The retrieved value.
        """
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
        :type this: Color
        :param r: Get-set proxy for red.
        :type r: GetSetProxy
        :param g: Get-set proxy for green.
        :type g: GetSetProxy
        :param b: Get-set proxy for blue.
        :type b: GetSetProxy
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
        
        :return: Red component value.
        :rtype: float
        """
        return self.__rp.get()

    @red.setter
    def red(self, new: float):
        """
        Set the red value.

        :param new: New red value.
        :type new: float
        """
        self.__rp.set(new)

    @property
    def green(self) -> float:
        """
        Green value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        
        :return: Green component value.
        :rtype: float
        """
        return self.__gp.get()

    @green.setter
    def green(self, new: float):
        """
        Set the green value.

        :param new: New green value.
        :type new: float
        """
        self.__gp.set(new)

    @property
    def blue(self) -> float:
        """
        Blue value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        
        :return: Blue component value.
        :rtype: float
        """
        return self.__bp.get()

    @blue.setter
    def blue(self, new: float):
        """
        Set the blue value.

        :param new: New blue value.
        :type new: float
        """
        self.__bp.set(new)

    def __iter__(self):
        """
        Iterator for this proxy.

        :return: Iterator yielding red, green, and blue values.
        :rtype: Iterator[float]

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

        :return: String representation of the RGB color proxy.
        :rtype: str

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
        :type this: Color
        :param h: Get-set proxy for hue.
        :type h: GetSetProxy
        :param s: Get-set proxy for saturation.
        :type s: GetSetProxy
        :param v: Get-set proxy for value.
        :type v: GetSetProxy
        """
        self.__this = this
        self.__hp = h
        self.__sp = s
        self.__vp = v

    @property
    def hue(self) -> float:
        """
        Hue value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        
        :return: Hue component value.
        :rtype: float
        """
        return self.__hp.get()

    @hue.setter
    def hue(self, new: float):
        """
        Set the hue value.

        :param new: New hue value.
        :type new: float
        """
        self.__hp.set(new)

    @property
    def saturation(self) -> float:
        """
        Saturation value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        
        :return: Saturation component value.
        :rtype: float
        """
        return self.__sp.get()

    @saturation.setter
    def saturation(self, new: float):
        """
        Set the saturation value.

        :param new: New saturation value.
        :type new: float
        """
        self.__sp.set(new)

    @property
    def value(self) -> float:
        """
        Value value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        
        :return: Value (brightness) component value.
        :rtype: float
        """
        return self.__vp.get()

    @value.setter
    def value(self, new: float):
        """
        Set the value.

        :param new: New value.
        :type new: float
        """
        self.__vp.set(new)

    @property
    def brightness(self) -> float:
        """
        Alias for ``value``.
        
        :return: Brightness (value) component value.
        :rtype: float
        """
        return self.value

    @brightness.setter
    def brightness(self, new: float):
        """
        Set the brightness value.

        :param new: New brightness value.
        :type new: float
        """
        self.value = new

    def __iter__(self):
        """
        Iterator for this proxy.

        :return: Iterator yielding hue, saturation, and value.
        :rtype: Iterator[float]

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

        :return: String representation of the HSV color proxy.
        :rtype: str

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
        :type this: Color
        :param h: Get-set proxy for hue.
        :type h: GetSetProxy
        :param l: Get-set proxy for lightness.
        :type l: GetSetProxy
        :param s: Get-set proxy for saturation.
        :type s: GetSetProxy
        """
        self.__this = this
        self.__hp = h
        self.__lp = l
        self.__sp = s

    @property
    def hue(self) -> float:
        """
        Hue value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        
        :return: Hue component value.
        :rtype: float
        """
        return self.__hp.get()

    @hue.setter
    def hue(self, new: float):
        """
        Set the hue value.

        :param new: New hue value.
        :type new: float
        """
        self.__hp.set(new)

    @property
    def lightness(self) -> float:
        """
        Lightness value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        
        :return: Lightness component value.
        :rtype: float
        """
        return self.__lp.get()

    @lightness.setter
    def lightness(self, new: float):
        """
        Set the lightness value.

        :param new: New lightness value.
        :type new: float
        """
        self.__lp.set(new)

    @property
    def saturation(self) -> float:
        """
        Saturation value (within :math:`\\left[0.0, 1.0\\right]`).

        .. note::
            Setter is available, the change will affect the :class:`Color` object.
        
        :return: Saturation component value.
        :rtype: float
        """
        return self.__sp.get()

    @saturation.setter
    def saturation(self, new: float):
        """
        Set the saturation value.

        :param new: New saturation value.
        :type new: float
        """
        self.__sp.set(new)

    def __iter__(self):
        """
        Iterator for this proxy.

        :return: Iterator yielding hue, lightness, and saturation.
        :rtype: Iterator[float]

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

        :return: String representation of the HLS color proxy.
        :rtype: str

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
    """
    Return b if a is None, otherwise return a.

    :param a: First value.
    :param b: Second value.
    :return: a if a is not None, otherwise b.
    """
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
        Constructor of ``Color``.

        :param c: Color value, can be hex string value, tuple rgb value, or another Color object.
        :type c: Union[str, Tuple[float, float, float], Color]
        :param alpha: Alpha value of color, default is None which means no alpha value.
        :type alpha: Optional[float]
        :raises TypeError: If c is not a valid color type.
        :raises ValueError: If c is an invalid string color format.
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

        .. note::
            Setter is available.
        
        :return: Alpha value, or None if no alpha is set.
        :rtype: Optional[float]
        """
        return self.__alpha

    @alpha.setter
    def alpha(self, new: Optional[float]):
        """
        Set the alpha value.

        :param new: New alpha value.
        :type new: Optional[float]
        """
        if new is not None:
            new = _a_mapper(new)
        self.__alpha = new

    def __get_rgb(self) -> Tuple[float, float, float]:
        """
        Get RGB values.

        :return: Tuple of (red, green, blue) values.
        :rtype: Tuple[float, float, float]
        """
        return self.__r, self.__g, self.__b

    def __set_rgb(self, r: Optional[float] = None, g: Optional[float] = None, b: Optional[float] = None):
        """
        Set RGB values.

        :param r: Red value, or None to keep current value.
        :type r: Optional[float]
        :param g: Green value, or None to keep current value.
        :type g: Optional[float]
        :param b: Blue value, or None to keep current value.
        :type b: Optional[float]
        """
        self.__r, self.__g, self.__b = map(lambda args: _ratio_or(*args), zip((r, g, b), self.__get_rgb()))

    @property
    def rgb(self) -> RGBColorProxy:
        """
        Get rgb color system based color proxy.
        See :class:`RGBColorProxy`.

        :return: Rgb color proxy.
        :rtype: RGBColorProxy
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

    def __get_hsv(self) -> Tuple[float, float, float]:
        """
        Get HSV values.

        :return: Tuple of (hue, saturation, value) values.
        :rtype: Tuple[float, float, float]
        """
        return colorsys.rgb_to_hsv(self.__r, self.__g, self.__b)

    def __set_hsv(self, h: Optional[float] = None, s: Optional[float] = None, v: Optional[float] = None):
        """
        Set HSV values.

        :param h: Hue value, or None to keep current value.
        :type h: Optional[float]
        :param s: Saturation value, or None to keep current value.
        :type s: Optional[float]
        :param v: Value (brightness) value, or None to keep current value.
        :type v: Optional[float]
        """
        h, s, v = map(lambda args: _ratio_or(*args), zip((h, s, v), self.__get_hsv()))
        self.__r, self.__g, self.__b = colorsys.hsv_to_rgb(h, s, v)

    @property
    def hsv(self) -> HSVColorProxy:
        """
        Get hsv color system based color proxy.
        See :class:`HSVColorProxy`.

        :return: Hsv color proxy.
        :rtype: HSVColorProxy
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

    def __get_hls(self) -> Tuple[float, float, float]:
        """
        Get HLS values.

        :return: Tuple of (hue, lightness, saturation) values.
        :rtype: Tuple[float, float, float]
        """
        return colorsys.rgb_to_hls(self.__r, self.__g, self.__b)

    def __set_hls(self, h: Optional[float] = None, l_: Optional[float] = None, s: Optional[float] = None):
        """
        Set HLS values.

        :param h: Hue value, or None to keep current value.
        :type h: Optional[float]
        :param l_: Lightness value, or None to keep current value.
        :type l_: Optional[float]
        :param s: Saturation value, or None to keep current value.
        :type s: Optional[float]
        """
        h, l, s = map(lambda args: _ratio_or(*args), zip((h, l_, s), self.__get_hls()))
        self.__r, self.__g, self.__b = colorsys.hls_to_rgb(h, l, s)

    @property
    def hls(self) -> HLSColorProxy:
        """
        Get hls color system based color proxy.
        See :class:`HLSColorProxy`.

        :return: Hls color proxy.
        :rtype: HLSColorProxy
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

    def __get_hex(self, include_alpha: bool) -> str:
        """
        Get hexadecimal representation of the color.

        :param include_alpha: Whether to include alpha channel in the hex string.
        :type include_alpha: bool
        :return: Hexadecimal color string.
        :rtype: str
        """
        rs, gs, bs = _ratio_to_hex(self.__r), _ratio_to_hex(self.__g), _ratio_to_hex(self.__b)
        as_ = _ratio_to_hex(self.__alpha) if self.__alpha is not None and include_alpha else ''

        return '#' + rs + gs + bs + as_

    def __get_name(self) -> str:
        """
        Get the CSS3 color name if available, otherwise return hex string.

        :return: Color name or hex string.
        :rtype: str
        """
        _hex = self.__get_hex(False).lower()
        return _CSS3_NAME_MAPS.get(_hex, _hex)

    def __repr__(self) -> str:
        """
        Get the string representation of the Color object.

        :return: String representation.
        :rtype: str
        """
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

    def __str__(self) -> str:
        """
        Hex format of this :class:`Color` object.
        
        :return: Hexadecimal color string.
        :rtype: str
        """
        return self.__get_hex(True)

    def __getstate__(self) -> Tuple[float, float, float, Optional[float]]:
        """
        Dump color as pickle object.

        :return: Dumped data object containing (r, g, b, alpha).
        :rtype: Tuple[float, float, float, Optional[float]]
        """
        return self.__r, self.__g, self.__b, self.__alpha

    def __setstate__(self, v: Tuple[float, float, float, Optional[float]]):
        """
        Load color from pickle object.

        :param v: Dumped data object containing (r, g, b, alpha).
        :type v: Tuple[float, float, float, Optional[float]]
        """
        self.__r, self.__g, self.__b, self.__alpha = v

    def __hash__(self) -> int:
        """
        Get hash value of current object.

        :return: Hash value of current color.
        :rtype: int
        """
        return hash(self.__getstate__())

    def __eq__(self, other) -> bool:
        """
        Get equality between colors.

        :param other: Another object to compare with.
        :return: True if equal, False otherwise.
        :rtype: bool
        """
        if other is self:
            return True
        elif type(other) == type(self):
            return other.__getstate__() == self.__getstate__()
        else:
            return False

    @classmethod
    def from_rgb(cls, r: float, g: float, b: float, alpha: Optional[float] = None) -> 'Color':
        """
        Load color from rgb system.

        :param r: Red value, should be a float value in :math:`\\left[0, 1\\right]`.
        :type r: float
        :param g: Green value, should be a float value in :math:`\\left[0, 1\\right]`.
        :type g: float
        :param b: Blue value, should be a float value in :math:`\\left[0, 1\\right]`.
        :type b: float
        :param alpha: Alpha value, should be a float value in :math:`\\left[0, 1\\right]`, \
            default is None which means no alpha value is used.
        :type alpha: Optional[float]
        :return: Color object.
        :rtype: Color
        """
        return cls((r, g, b), alpha)

    @classmethod
    def from_hex(cls, hex_: str) -> 'Color':
        r"""
        Load color from hexadecimal rgb string.

        :param hex\_: Hexadecimal string, maybe starts with ``#``.
        :type hex\_: str
        :return: Color object.
        :rtype: Color
        """
        return cls(hex_)

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float, alpha: Optional[float] = None) -> 'Color':
        """
        Load color from hsv system.

        :param h: Hue value, should be a float value in :math:`\\left[0, 1\\right)`.
        :type h: float
        :param s: Saturation value, should be a float value in :math:`\\left[0, 1\\right]`.
        :type s: float
        :param v: Brightness (value) value, should be a float value in :math:`\\left[0, 1\\right]`.
        :type v: float
        :param alpha: Alpha value, should be a float value in :math:`\\left[0, 1\\right]`, \
            default is None which means no alpha value is used.
        :type alpha: Optional[float]
        :return: Color object.
        :rtype: Color
        """
        return cls(colorsys.hsv_to_rgb(h, s, v), alpha)

    @classmethod
    def from_hls(cls, h: float, l: float, s: float, alpha: Optional[float] = None) -> 'Color':
        """
        Load color from hls system.

        :param h: Hue value, should be a float value in :math:`\\left[0, 1\\right)`.
        :type h: float
        :param l: Lightness value, should be a float value in :math:`\\left[0, 1\\right]`.
        :type l: float
        :param s: Saturation value, should be a float value in :math:`\\left[0, 1\\right]`.
        :type s: float
        :param alpha: Alpha value, should be a float value in :math:`\\left[0, 1\\right]`, \
            default is None which means no alpha value is used.
        :type alpha: Optional[float]
        :return: Color object.
        :rtype: Color
        """
        return cls(colorsys.hls_to_rgb(h, l, s), alpha)
