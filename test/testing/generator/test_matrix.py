import pytest

from hbutils.testing import MatrixGenerator


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestTestingGeneratorMatrix:
    def test_init(self):
        with pytest.raises(KeyError):
            MatrixGenerator(
                {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
                includes=[{'a': 4, 'r': 7, 't': 3}],
                excludes=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}],
            )
        with pytest.raises(KeyError):
            MatrixGenerator(
                {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
                includes=[{'a': 4, 'r': 7}],
                excludes=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b', 't': 3}],
            )

    def test_accessors(self):
        m = MatrixGenerator(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            includes=[{'a': 4, 'r': 7}],
            excludes=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}],
        )
        assert m.names == ['a', 'b', 'r']
        assert m.values == {'a': (1, 2, 3), 'b': ('a', 'b'), 'r': (3, 4, 5)}
        assert m.includes == [{'a': (4,), 'r': (7,)}]
        assert m.excludes == [{'a': (1,), 'r': (3,)}, {'a': (3,), 'b': ('b',)}]

    def test_cases(self):
        m = MatrixGenerator(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            includes=[{'a': 4, 'r': 7}],
            excludes=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
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

    def test_tuple_cases(self):
        m = MatrixGenerator(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            includes=[{'a': 4, 'r': 7}],
            excludes=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
        )
        assert list(m.tuple_cases()) == [
            (1, 'a', 4),
            (1, 'a', 5),
            (1, 'b', 4),
            (1, 'b', 5),
            (2, 'a', 3),
            (2, 'a', 4),
            (2, 'a', 5),
            (2, 'b', 3),
            (2, 'b', 4),
            (2, 'b', 5),
            (3, 'a', 3),
            (3, 'a', 4),
            (3, 'a', 5),
            (4, 'b', 7),
        ]

    def test_complex_full(self):
        m = MatrixGenerator(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            includes=[{'a': 4, 'r': 7}, {'a': [1, 2, 3], 'b': ['a', 'b', 'c']}],
            excludes=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
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
