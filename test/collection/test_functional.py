import pytest

from hbutils.collection import nested_map


@pytest.mark.unittest
class TestCollectionFunctional:
    def test_nested_map(self):
        assert nested_map(lambda x: x + 1, [
            2, 3, (4, {'x': 2, 'y': 4}),
            {'a': 3, 'b': (4, 5)},
        ]) == [3, 4, (5, {'x': 3, 'y': 5}), {'a': 4, 'b': (5, 6)}]

        assert nested_map(lambda x, p: (x + 1) * len(p), [
            2, 3, (4, {'x': 2, 'y': 4}),
            {'a': 3, 'b': (4, 5)},
        ]) == [3, 4, (10, {'x': 9, 'y': 15}), {'a': 8, 'b': (15, 18)}]

        assert nested_map(lambda: 233, [
            2, 3, (4, {'x': 2, 'y': 4}),
            {'a': 3, 'b': (4, 5)},
        ]) == [233, 233, (233, {'x': 233, 'y': 233}), {'a': 233, 'b': (233, 233)}]
