import math
import pickle
from functools import wraps
from typing import Callable

import pytest

from hbutils.color import Color


def eq_extend(func: Callable[..., bool]):
    @wraps(func)
    def _new_func(a, b, *args, **kwargs):
        if isinstance(a, dict) and isinstance(b, dict):
            aks, bks = set(a.keys()), set(b.keys())
            if aks != bks:
                return False
            else:
                return all([_new_func(a[key], b[key], *args, **kwargs) for key in aks])
        elif (isinstance(a, tuple) and isinstance(b, tuple)) \
                or (isinstance(a, list) and isinstance(b, list)):
            length_a, length_b = len(a), len(b)
            if length_a != length_b:
                return False
            else:
                return all([_new_func(ai, bi, *args, **kwargs) for ai, bi in zip(a, b)])
        else:
            return func(a, b, *args, **kwargs)

    return _new_func


@eq_extend
def float_eq(a, b, eps=1e-5):
    return abs(a - b) < abs(eps)


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestColorModel:
    def test_basis(self):
        c1 = Color((0.8, 0.7, 0.5))
        assert float_eq(c1.rgb.red, 0.8)
        assert float_eq(c1.rgb.green, 0.7)
        assert float_eq(c1.rgb.blue, 0.5)
        assert c1.alpha is None
        assert str(c1) == '#ccb280'
        assert repr(c1) == '<Color #ccb280>'

    def test_basic_with_alpha(self):
        c1 = Color((0.8, 0.7, 0.5), 0.6)
        assert float_eq(c1.rgb.red, 0.8)
        assert float_eq(c1.rgb.green, 0.7)
        assert float_eq(c1.rgb.blue, 0.5)
        assert float_eq(c1.alpha, 0.6)
        assert str(c1) == '#ccb28099'
        assert repr(c1) == '<Color #ccb280, alpha: 0.600>'

    def test_basic_with_hex(self):
        c1 = Color('#aabbccdd')
        assert c1.rgb.red == int('aa', 16) / 255
        assert c1.rgb.green == int('bb', 16) / 255
        assert c1.rgb.blue == int('cc', 16) / 255
        assert c1.alpha == int('dd', 16) / 255

        with pytest.raises(ValueError):
            Color('#aabbccd')

        with pytest.warns(UserWarning):
            c2 = Color('#aabbccdd', alpha=0.8)
        assert c2.rgb.red == int('aa', 16) / 255
        assert c2.rgb.green == int('bb', 16) / 255
        assert c2.rgb.blue == int('cc', 16) / 255
        assert c2.alpha == int('dd', 16) / 255

        c3 = Color('#aabbcc', alpha=0.8)
        assert c3.rgb.red == int('aa', 16) / 255
        assert c3.rgb.green == int('bb', 16) / 255
        assert c3.rgb.blue == int('cc', 16) / 255
        assert c3.alpha == 0.8

    def test_basic_error(self):
        with pytest.raises(TypeError):
            Color(None)

    def test_dumps_hash_and_eq(self):
        c1 = Color('#aabbccdd')
        assert c1 == c1
        assert c1 == Color('#aabbccdd')
        assert pickle.loads(pickle.dumps(c1)) == c1
        assert c1 != 1

        assert hash(Color('#aabbccdd')) == hash(c1)

    def test_set_rgb(self):
        c1 = Color((0.8, 0.7, 0.5), 0.6)
        assert float_eq(c1.rgb.red, 0.8)
        assert float_eq(c1.rgb.green, 0.7)
        assert float_eq(c1.rgb.blue, 0.5)
        assert float_eq(c1.alpha, 0.6)

        r, g, b = c1.rgb
        assert float_eq((r, g, b), (0.8, 0.7, 0.5))
        assert repr(c1.rgb) == '<RGBColorProxy red: 0.800, green: 0.700, blue: 0.500>'

        c1.rgb.red *= 0.7
        c1.rgb.green *= 0.6
        c1.rgb.blue *= 0.8
        c1.alpha *= 0.9
        assert float_eq(c1.rgb.red, 0.56)
        assert float_eq(c1.rgb.green, 0.42)
        assert float_eq(c1.rgb.blue, 0.4)
        assert float_eq(c1.alpha, 0.54)
        assert str(c1) == '#8f6b668a'

        with pytest.warns(Warning):
            c1.rgb.red *= 10
        with pytest.warns(Warning):
            c1.rgb.green *= 10
        with pytest.warns(Warning):
            c1.rgb.blue *= 10
        with pytest.warns(Warning):
            c1.alpha *= 10
        assert float_eq(c1.rgb.red, 1.0)
        assert float_eq(c1.rgb.green, 1.0)
        assert float_eq(c1.rgb.blue, 1.0)
        assert float_eq(c1.alpha, 1.0)
        assert str(c1) == '#ffffffff'

        with pytest.warns(Warning):
            c1.rgb.red *= -10
        with pytest.warns(Warning):
            c1.rgb.green *= -10
        with pytest.warns(Warning):
            c1.rgb.blue *= -10
        with pytest.warns(Warning):
            c1.alpha *= -10

        assert float_eq(c1.rgb.red, 0.0)
        assert float_eq(c1.rgb.green, 0.0)
        assert float_eq(c1.rgb.blue, 0.0)
        assert float_eq(c1.alpha, 0.0)
        assert str(c1) == '#00000000'

    def test_set_hsv(self):
        c1 = Color((0.8, 0.7, 0.5), 0.6)

        h, s, v = c1.hsv
        assert repr(c1.hsv) == '<HSVColorProxy hue: 0.111, saturation: 0.375, value: 0.800>'

        assert Color.from_hsv(h, s, v, 0.6) == c1

        c1.hsv.hue *= 0.6
        c1.hsv.saturation *= 0.7
        c1.hsv.value *= 0.8
        assert float_eq(tuple(c1.hsv), (h * 0.6, s * 0.7, v * 0.8))
        h, s, v = c1.hsv

        with pytest.warns(None):
            c1.hsv.hue *= 1000
        with pytest.warns(Warning):
            c1.hsv.saturation *= 10
        with pytest.warns(Warning):
            c1.hsv.value *= 10
        assert float_eq(tuple(c1.hsv), (h * 1000 - math.floor(h * 1000), 1.0, 1.0))
        h, s, v = c1.hsv

        with pytest.warns(None):
            c1.hsv.hue *= -1000
        assert float_eq(tuple(c1.hsv), (h * -1000 - math.floor(h * -1000), s, v))

    def test_set_hls(self):
        c1 = Color((0.8, 0.7, 0.5), 0.6)

        h, l, s = c1.hls
        assert repr(c1.hls) == '<HLSColorProxy hue: 0.111, lightness: 0.650, saturation: 0.429>'

        assert Color.from_hls(h, l, s, 0.6) == c1

        c1.hls.hue *= 0.6
        c1.hls.lightness *= 0.7
        c1.hls.saturation *= 0.8
        assert float_eq(tuple(c1.hls), (h * 0.6, l * 0.7, s * 0.8))
        h, l, s = c1.hls

        with pytest.warns(None):
            c1.hls.hue *= 1000
        assert float_eq(tuple(c1.hls), (h * 1000 - math.floor(h * 1000), l, s))

        with pytest.warns(Warning):
            c1.hls.lightness += 1000
        assert float_eq(c1.hls.lightness, 1.0)
        c1.hls.lightness = 0.5

        with pytest.warns(Warning):
            c1.hls.saturation += 1000
        assert float_eq(c1.hls.saturation, 1.0)

    def test_from_rgb(self):
        assert Color.from_rgb(0.3, 0.4, 0.5) == Color((0.3, 0.4, 0.5))
        assert Color.from_rgb(0.3, 0.4, 0.5, 0.8) == Color((0.3, 0.4, 0.5), 0.8)

    def test_from_hex(self):
        c1 = Color.from_hex('#aabbccdd')
        assert c1.rgb.red == int('aa', 16) / 255
        assert c1.rgb.green == int('bb', 16) / 255
        assert c1.rgb.blue == int('cc', 16) / 255
        assert c1.alpha == int('dd', 16) / 255
