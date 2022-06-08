import pytest

from hbutils.color import visual_distance, Color, rnd_colors


@pytest.mark.unittest
class TestColorUtils:
    def test_visual_distance(self):
        assert visual_distance(
            Color.from_hex('#ff0000'),
            Color.from_hex('#00ff00')
        ) == pytest.approx(2.5495097567963922)

        assert visual_distance(
            Color.from_hex('#778800'),
            Color.from_hex('#887700')
        ) == pytest.approx(0.16996731711975946)

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
