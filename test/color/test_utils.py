import pytest

from hbutils.color import visual_distance, Color, rnd_colors


@pytest.mark.unittest
class TestColorUtils:
    def test_visual_distance(self):
        assert abs(visual_distance(
            Color.from_hex('#ff0000'),
            Color.from_hex('#00ff00')
        ) - 2.5495097567963922) < 1e-6

        assert abs(visual_distance(
            Color.from_hex('#778800'),
            Color.from_hex('#887700')
        ) - 0.16996731711975946) < 1e-6

    def test_rnd_colors(self):
        cs = list(rnd_colors(12))
        assert len(cs) == 12
        assert list(map(str, cs)) == [
            '#ff00ee',
            '#00ff00',
            '#009cff',
            '#ff006c',
            '#c9ff00',
            '#00f3ff',
            '#d100ff',
            '#ffaf00',
            '#00ff6c',
            '#4100ff',
            '#ff5300',
            '#46ff00',
        ]
