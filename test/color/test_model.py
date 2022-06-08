import math
import pickle

import pytest

from hbutils.color import Color


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestColorModel:
    def test_basis(self):
        c1 = Color((0.8, 0.7, 0.5))
        assert c1.rgb.red == pytest.approx(0.8)
        assert c1.rgb.green == pytest.approx(0.7)
        assert c1.rgb.blue == pytest.approx(0.5)
        assert c1.alpha is None
        assert str(c1) == '#ccb280'
        assert repr(c1) == '<Color #ccb280>'

        c2 = Color('#ff0000')
        assert str(c2) == '#ff0000'
        assert repr(c2) == '<Color red>'

        c3 = Color('lime')
        assert str(c3) == '#00ff00'
        assert repr(c3) == '<Color lime>'

    def test_basic_with_alpha(self):
        c1 = Color((0.8, 0.7, 0.5), 0.6)
        assert c1.rgb.red == pytest.approx(0.8)
        assert c1.rgb.green == pytest.approx(0.7)
        assert c1.rgb.blue == pytest.approx(0.5)
        assert c1.alpha == pytest.approx(0.6)
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

        c2 = Color('#aabbccdd', alpha=0.8)
        assert c2.rgb.red == int('aa', 16) / 255
        assert c2.rgb.green == int('bb', 16) / 255
        assert c2.rgb.blue == int('cc', 16) / 255
        assert c2.alpha == pytest.approx(0.8)

        c3 = Color('#aabbcc', alpha=0.8)
        assert c3.rgb.red == int('aa', 16) / 255
        assert c3.rgb.green == int('bb', 16) / 255
        assert c3.rgb.blue == int('cc', 16) / 255
        assert c3.alpha == 0.8

        c4 = Color(Color('#aabbcc'), alpha=0.8)
        assert c4.rgb.red == int('aa', 16) / 255
        assert c4.rgb.green == int('bb', 16) / 255
        assert c4.rgb.blue == int('cc', 16) / 255
        assert c4.alpha == pytest.approx(0.8)

        c5 = Color(Color('#aabbccdd'), alpha=0.8)
        assert c5.rgb.red == int('aa', 16) / 255
        assert c5.rgb.green == int('bb', 16) / 255
        assert c5.rgb.blue == int('cc', 16) / 255
        assert c5.alpha == pytest.approx(0.8)

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
        assert c1.rgb.red == pytest.approx(0.8)
        assert c1.rgb.green == pytest.approx(0.7)
        assert c1.rgb.blue == pytest.approx(0.5)
        assert c1.alpha == pytest.approx(0.6)

        r, g, b = c1.rgb
        assert (r, g, b) == pytest.approx((0.8, 0.7, 0.5))
        assert repr(c1.rgb) == '<RGBColorProxy red: 0.800, green: 0.700, blue: 0.500>'

        c1.rgb.red *= 0.7
        c1.rgb.green *= 0.6
        c1.rgb.blue *= 0.8
        c1.alpha *= 0.9
        assert c1.rgb.red == pytest.approx(0.56)
        assert c1.rgb.green == pytest.approx(0.42)
        assert c1.rgb.blue == pytest.approx(0.4)
        assert c1.alpha == pytest.approx(0.54)
        assert str(c1) == '#8f6b668a'

        with pytest.warns(Warning):
            c1.rgb.red *= 10
        with pytest.warns(Warning):
            c1.rgb.green *= 10
        with pytest.warns(Warning):
            c1.rgb.blue *= 10
        with pytest.warns(Warning):
            c1.alpha *= 10
        assert c1.rgb.red == pytest.approx(1.0)
        assert c1.rgb.green == pytest.approx(1.0)
        assert c1.rgb.blue == pytest.approx(1.0)
        assert c1.alpha == pytest.approx(1.0)
        assert str(c1) == '#ffffffff'

        with pytest.warns(Warning):
            c1.rgb.red *= -10
        with pytest.warns(Warning):
            c1.rgb.green *= -10
        with pytest.warns(Warning):
            c1.rgb.blue *= -10
        with pytest.warns(Warning):
            c1.alpha *= -10

        assert c1.rgb.red == pytest.approx(0.0)
        assert c1.rgb.green == pytest.approx(0.0)
        assert c1.rgb.blue == pytest.approx(0.0)
        assert c1.alpha == pytest.approx(0.0)
        assert str(c1) == '#00000000'

    def test_set_hsv(self):
        c1 = Color((0.8, 0.7, 0.5), 0.6)

        h, s, v = c1.hsv
        assert repr(c1.hsv) == '<HSVColorProxy hue: 0.111, saturation: 0.375, value: 0.800>'

        assert Color.from_hsv(h, s, v, 0.6) == c1
        assert c1.hsv.hue == pytest.approx(1 / 9)
        assert c1.hsv.saturation == pytest.approx(0.375)
        assert c1.hsv.value == pytest.approx(0.8)
        assert c1.hsv.brightness == pytest.approx(0.8)

        c1.hsv.hue *= 0.6
        c1.hsv.saturation *= 0.7
        c1.hsv.value *= 0.8
        assert tuple(c1.hsv) == pytest.approx((h * 0.6, s * 0.7, v * 0.8))
        h, s, v = c1.hsv

        with pytest.warns(None):
            c1.hsv.hue *= 1000
        with pytest.warns(Warning):
            c1.hsv.saturation *= 10
        with pytest.warns(Warning):
            c1.hsv.brightness *= 10  # should be the same as `c1.hsv.value *= 10`
        assert tuple(c1.hsv) == pytest.approx((h * 1000 - math.floor(h * 1000), 1.0, 1.0))
        h, s, v = c1.hsv

        with pytest.warns(None):
            c1.hsv.hue *= -1000
        assert tuple(c1.hsv) == pytest.approx((h * -1000 - math.floor(h * -1000), s, v))

    def test_set_hls(self):
        c1 = Color((0.8, 0.7, 0.5), 0.6)

        h, l, s = c1.hls
        assert repr(c1.hls) == '<HLSColorProxy hue: 0.111, lightness: 0.650, saturation: 0.429>'

        assert Color.from_hls(h, l, s, 0.6) == c1

        c1.hls.hue *= 0.6
        c1.hls.lightness *= 0.7
        c1.hls.saturation *= 0.8
        assert tuple(c1.hls) == pytest.approx((h * 0.6, l * 0.7, s * 0.8))
        h, l, s = c1.hls

        with pytest.warns(None):
            c1.hls.hue *= 1000
        assert tuple(c1.hls) == pytest.approx((h * 1000 - math.floor(h * 1000), l, s))

        with pytest.warns(Warning):
            c1.hls.lightness += 1000
        assert c1.hls.lightness == pytest.approx(1.0)
        c1.hls.lightness = 0.5

        with pytest.warns(Warning):
            c1.hls.saturation += 1000
        assert c1.hls.saturation == pytest.approx(1.0)

    def test_from_rgb(self):
        assert Color.from_rgb(0.3, 0.4, 0.5) == Color((0.3, 0.4, 0.5))
        assert Color.from_rgb(0.3, 0.4, 0.5, 0.8) == Color((0.3, 0.4, 0.5), 0.8)

    def test_from_hex(self):
        c1 = Color.from_hex('#aabbccdd')
        assert c1.rgb.red == int('aa', 16) / 255
        assert c1.rgb.green == int('bb', 16) / 255
        assert c1.rgb.blue == int('cc', 16) / 255
        assert c1.alpha == int('dd', 16) / 255

    def test_init_with_name(self):
        assert str(Color('red')) == '#ff0000'
        assert str(Color('gold')) == '#ffd700'

        with pytest.raises(ValueError):
            Color('golden')
