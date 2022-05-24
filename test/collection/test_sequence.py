import pytest

from hbutils.collection import unique, group_by


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

    def test_group_by(self):
        foods = [
            'apple',
            'orange',
            'pear',
            'banana',
            'fish',
            'pork',
            'milk'
        ]
        assert group_by(foods, len) == {
            4: ['pear', 'fish', 'pork', 'milk'],
            5: ['apple'],
            6: ['orange', 'banana']
        }
        assert group_by(foods, len, len) == {4: 4, 5: 1, 6: 2}

        assert group_by(foods, lambda x: x[0]) == {
            'a': ['apple'],
            'b': ['banana'],
            'f': ['fish'],
            'm': ['milk'],
            'o': ['orange'],
            'p': ['pear', 'pork']
        }
        assert group_by(foods, lambda x: x[0], len) == {
            'a': 1, 'b': 1, 'f': 1,
            'm': 1, 'o': 1, 'p': 2,
        }
