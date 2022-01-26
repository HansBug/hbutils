import pytest

from hbutils.collection import sq_flatten


@pytest.mark.unittest
class TestCollectionStructural:
    def test_sq_flatten(self):
        assert sq_flatten([1, 2, [3, 4], [5, [6, 7], (8, 9, 10)], 11]) == \
               [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
