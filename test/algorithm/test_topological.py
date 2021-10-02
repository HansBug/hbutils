import pytest

from hbutils.algorithm import topoids, topo


class _Container:
    def __init__(self, v):
        self.v = v

    def __key(self):
        return self.v,

    def __eq__(self, o: object) -> bool:
        if type(o) == type(self):
            return o.__key() == self.__key()
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.__key())


@pytest.mark.unittest
class TestAlgorithmTopological:
    def test_topoids_unsorted(self):
        assert topoids(0, []) == []
        r2 = topoids(3, [])
        assert (r2 == [0, 1, 2]) or (r2 == [0, 2, 1]) \
               or (r2 == [1, 0, 2]) or (r2 == [1, 2, 0]) \
               or (r2 == [2, 0, 1]) or (r2 == [2, 1, 0])
        r3 = topoids(3, [(0, 1), (2, 1)])
        assert (r3 == [0, 2, 1]) or (r3 == [2, 0, 1])
        r4 = topoids(4, [(0, 2), (0, 1), (2, 3), (1, 3)])
        assert (r4 == [0, 1, 2, 3]) or (r4 == [0, 2, 1, 3])

        with pytest.raises(ArithmeticError):
            topoids(3, [(0, 1), (2, 1), (1, 0)])

    def test_topoids_sorted(self):
        assert topoids(0, [], sort=True) == []
        assert topoids(3, [], sort=True) == [0, 1, 2]
        assert topoids(3, [(0, 1), (2, 1)], sort=True) == [0, 2, 1]
        assert topoids(4, [(0, 2), (0, 1), (2, 3), (1, 3)], sort=True) == [0, 1, 2, 3]

        with pytest.raises(ArithmeticError) as ei:
            topoids(3, [(0, 1), (2, 1), (1, 0)], sort=True)
        _, missing_ids = ei.value.args
        assert missing_ids == (0, 1)

    def test_topo_sorted(self):
        assert topo([], []) == []

        n1 = _Container(1)
        n2 = _Container('sdfklj')
        n3 = _Container((2, 3))
        n4 = _Container((3, 'sdj'))
        n5 = _Container(1)
        assert topo([n1, n2, n3], [], sort=True) == [n1, n2, n3]
        assert topo([n1, n2, n5], [(n1, n2), (n5, n2)], sort=True) == [n1, n5, n2]
        assert topo([n1, n2, n5], [(n1, n2), (n5, n2)], identifier=lambda x: x.v, sort=True) == [n1, n2]

        with pytest.raises(ArithmeticError) as ei:
            topo([n1, n2, n3, n4], [(n1, n3), (n3, n1), (n2, n3), (n4, n1)])
        _, missing_items = ei.value.args
        assert missing_items == (n1, n3)
