import pytest

from hbutils.collection import unique


@pytest.mark.unittest
class TestCollectionSequence:
    def test_unique(self):
        r1 = unique([1, 2, 3, 1])
        assert type(r1) == list
        assert r1 == [1, 2, 3]

        r2 = unique(('a', 'b', 'a', 'c', 'd', 'e', 'b'))
        assert type(r2) == tuple
        assert r2 == ('a', 'b', 'c', 'd', 'e')

        r3 = unique([3, 1, 2, 1, 4, 3])
        assert type(r3) == list
        assert r3 == [3, 1, 2, 4]

        class MyList(list):
            pass

        r4 = unique(MyList([3, 1, 2, 1, 4, 3]))
        assert type(r4) == MyList
        assert r4 == MyList([3, 1, 2, 4])
