import pytest

from hbutils.collection import nested_map


@pytest.mark.unittest
class TestCollectionFunctional:
    def test_nested_map(self):
        assert nested_map(lambda x: x + 1, [
            2, 3, (4, {'x': 2, 'y': 4}),
            {'a': 3, 'b': (4, 5)},
        ]) == [
                   3, 4, (5, {'x': 3, 'y': 5}),
                   {'a': 4, 'b': (5, 6)},
               ]
