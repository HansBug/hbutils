import pytest

from hbutils.testing import MatrixGenerator


@pytest.mark.unittest
class TestTestingMatrixFull:
    def test_init(self):
        with pytest.raises(KeyError):
            MatrixGenerator(
                {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
                include=[{'a': 4, 'r': 7, 't': 3}],
                exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}],
            )
        with pytest.raises(KeyError):
            MatrixGenerator(
                {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
                include=[{'a': 4, 'r': 7}],
                exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b', 't': 3}],
            )

    def test_accessors(self):
        m = MatrixGenerator(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            include=[{'a': 4, 'r': 7}],
            exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}],
        )
        assert m.names == ['a', 'b', 'r']
        assert m.values == {'a': (1, 2, 3), 'b': ('a', 'b'), 'r': (3, 4, 5)}
        assert m.include == [{'a': (4,), 'r': (7,)}]
        assert m.exclude == [{'a': (1,), 'r': (3,)}, {'a': (3,), 'b': ('b',)}]

    def test_accessors(self):
        m = MatrixGenerator(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            include=[{'a': 4, 'r': 7}],
            exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
        )
        assert list(m.cases()) == [
            {'a': 1, 'b': 'a', 'r': 4},
            {'a': 1, 'b': 'a', 'r': 5},
            {'a': 1, 'b': 'b', 'r': 4},
            {'a': 1, 'b': 'b', 'r': 5},
            {'a': 2, 'b': 'a', 'r': 3},
            {'a': 2, 'b': 'a', 'r': 4},
            {'a': 2, 'b': 'a', 'r': 5},
            {'a': 2, 'b': 'b', 'r': 3},
            {'a': 2, 'b': 'b', 'r': 4},
            {'a': 2, 'b': 'b', 'r': 5},
            {'a': 3, 'b': 'a', 'r': 3},
            {'a': 3, 'b': 'a', 'r': 4},
            {'a': 3, 'b': 'a', 'r': 5},
            {'a': 4, 'b': 'b', 'r': 7},
        ]

    def test_complex_full(self):
        m = MatrixGenerator(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            include=[{'a': 4, 'r': 7}, {'a': [1, 2, 3], 'b': ['a', 'b', 'c']}],
            exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
        )
        assert list(m.cases()) == [
            {'a': 1, 'b': 'a', 'r': 4},
            {'a': 1, 'b': 'a', 'r': 5},
            {'a': 1, 'b': 'b', 'r': 4},
            {'a': 1, 'b': 'b', 'r': 5},
            {'a': 2, 'b': 'a', 'r': 3},
            {'a': 2, 'b': 'a', 'r': 4},
            {'a': 2, 'b': 'a', 'r': 5},
            {'a': 2, 'b': 'b', 'r': 3},
            {'a': 2, 'b': 'b', 'r': 4},
            {'a': 2, 'b': 'b', 'r': 5},
            {'a': 3, 'b': 'a', 'r': 3},
            {'a': 3, 'b': 'a', 'r': 4},
            {'a': 3, 'b': 'a', 'r': 5},
            {'a': 4, 'b': 'b', 'r': 7},
            {'a': 1, 'b': 'c', 'r': 4},
            {'a': 1, 'b': 'c', 'r': 5},
            {'a': 2, 'b': 'c', 'r': 3},
            {'a': 2, 'b': 'c', 'r': 4},
            {'a': 2, 'b': 'c', 'r': 5},
            {'a': 3, 'b': 'c', 'r': 3},
            {'a': 3, 'b': 'c', 'r': 4},
            {'a': 3, 'b': 'c', 'r': 5},
        ]
