import pytest

from hbutils.collection import sq_flatten, nested_walk, nested_flatten


@pytest.mark.unittest
class TestCollectionStructural:
    def test_sq_flatten(self):
        assert sq_flatten([1, 2, [3, 4], [5, [6, 7], (8, 9, 10)], 11]) == \
               [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def test_nested_walk(self):
        assert list(nested_walk({'a': 1, 'b': ['c', 'd', {'x': (3, 4), 'y': 'f'}]})) == [
            (('a',), 1),
            (('b', 0), 'c'),
            (('b', 1), 'd'),
            (('b', 2, 'x', 0), 3),
            (('b', 2, 'x', 1), 4),
            (('b', 2, 'y'), 'f')
        ]

    def test_nested_flatten(self):
        assert nested_flatten({'a': 1, 'b': ['c', 'd', {'x': (3, 4), 'y': 'f'}]}) == [
            (('a',), 1),
            (('b', 0), 'c'),
            (('b', 1), 'd'),
            (('b', 2, 'x', 0), 3),
            (('b', 2, 'x', 1), 4),
            (('b', 2, 'y'), 'f')
        ]
