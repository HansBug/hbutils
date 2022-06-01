import pytest

from hbutils.collection import StackedMapping


@pytest.mark.unittest
class TestCollectionStacked:
    def test_stacked_mapping(self):
        d1 = {'a': 1, 'b': 2}
        d2 = {'b': 3, 'c': 4, 'd': 5}
        d3 = {'c': 6, 'e': 7}
        s = StackedMapping(d1, d2, d3)

        assert s['a'] == 1
        assert s['b'] == 3
        assert s['c'] == 6
        assert s['d'] == 5
        assert s['e'] == 7
        with pytest.raises(KeyError):
            _ = s['f']
        assert len(s) == 5
        assert s == {
            'a': 1, 'b': 3, 'c': 6, 'd': 5, 'e': 7,
        }

        del d2['b']
        del d3['c']
        assert s['a'] == 1
        assert s['b'] == 2
        assert s['c'] == 4
        assert s['d'] == 5
        assert s['e'] == 7
        with pytest.raises(KeyError):
            _ = s['f']
        assert len(s) == 5
        assert s == {
            'a': 1, 'b': 2, 'c': 4, 'd': 5, 'e': 7,
        }

        del d1['b']
        assert s['a'] == 1
        with pytest.raises(KeyError):
            _ = s['b']
        assert s['c'] == 4
        assert s['d'] == 5
        assert s['e'] == 7
        with pytest.raises(KeyError):
            _ = s['f']
        assert len(s) == 4
        assert s == {
            'a': 1, 'c': 4, 'd': 5, 'e': 7,
        }

        assert StackedMapping() == {}
        assert not StackedMapping()
