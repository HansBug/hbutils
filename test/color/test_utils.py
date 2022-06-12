import pytest

from hbutils.color import visual_distance, Color, rnd_colors, linear_gradient


@pytest.mark.unittest
class TestColorUtils:
    def test_visual_distance(self):
        assert visual_distance(
            Color.from_hex('#ff0000'),
            Color.from_hex('#00ff00')
        ) == pytest.approx(2.5495097567963922)
        assert visual_distance('#ff0000', '#00ff00') == pytest.approx(2.5495097567963922)

        assert visual_distance(
            Color.from_hex('#778800'),
            Color.from_hex('#887700')
        ) == pytest.approx(0.16996731711975946)
        assert visual_distance('#778800', '#887700') == pytest.approx(0.16996731711975946)

    def test_rnd_colors(self):
        cs = list(rnd_colors(12))
        assert len(cs) == 12
        assert list(map(str, cs)) == [
            '#ff00ee', '#00ff00', '#009cff', '#ff006c', '#c9ff00', '#00f3ff',
            '#d100ff', '#ffaf00', '#00ff6c', '#4100ff', '#ff5300', '#46ff00',
        ]

        cs = list(rnd_colors(12, alpha=0.8))
        assert len(cs) == 12
        assert list(map(str, cs)) == [
            '#ff00eecc', '#00ff00cc', '#009cffcc', '#ff006ccc', '#c9ff00cc', '#00f3ffcc',
            '#d100ffcc', '#ffaf00cc', '#00ff6ccc', '#4100ffcc', '#ff5300cc', '#46ff00cc'
        ]

    def test_linear_gradient_simple(self):
        f = linear_gradient(('red', 'yellow', 'green'))
        assert str(f(0)) == '#ff0000'
        assert str(f(0.25)) == '#ff8000'
        assert str(f(1 / 3)) == '#ffaa00'
        assert str(f(0.5)) == '#ffff00'
        assert str(f(2 / 3)) == '#aad500'
        assert str(f(0.75)) == '#80c000'
        assert str(f(1)) == '#008000'

    def test_linear_gradient_complex(self):
        f = linear_gradient(((-0.2, 'red'), (0.7, '#ffff0044'), (1.1, '#0708f4')))
        assert str(f(-0.2)) == '#ff0000ff'
        assert str(f(0)) == '#ff3900d5'
        assert str(f(0.25)) == '#ff8000a2'
        assert str(f(1 / 3)) == '#ff970090'
        assert str(f(0.5)) == '#ffc6006e'
        assert str(f(2 / 3)) == '#fff6004b'
        assert str(f(0.7)) == '#ffff0044'
        assert str(f(0.75)) == '#e0e01f5b'
        assert str(f(0.8)) == '#c1c13d73'
        assert str(f(1)) == '#4546b7d0'
        assert str(f(1.1)) == '#0708f4ff'
