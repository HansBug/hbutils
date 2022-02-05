import pytest

from hbutils.testing import FullMatrix


@pytest.mark.unittest
class TestTestingMatrixBase:
    def test_init(self):
        with pytest.raises(KeyError):
            FullMatrix(
                {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
                include=[{'a': 4, 'r': 7, 't': 3}],
                exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}],
            )
        with pytest.raises(KeyError):
            FullMatrix(
                {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
                include=[{'a': 4, 'r': 7}],
                exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b', 't': 3}],
            )

    def test_accessors(self):
        m = FullMatrix(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            include=[{'a': 4, 'r': 7}],
            exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}],
        )
        assert m.names == ['a', 'b', 'r']
        assert m.values == {'a': (1, 2, 3), 'b': ('a', 'b'), 'r': (3, 4, 5)}
        assert m.include == [{'a': (4,), 'r': (7,)}]
        assert m.exclude == [{'a': (1,), 'r': (3,)}, {'a': (3,), 'b': ('b',)}]
