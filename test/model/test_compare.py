import pytest

from hbutils.model import IComparable


@pytest.mark.unittest
class TestModelCompare:
    def test_icompare(self):
        class MyValue(IComparable):
            def __init__(self, v) -> None:
                self._v = v

            def _cmpkey(self):
                return self._v

        assert MyValue(1) == MyValue(1)
        assert not (MyValue(1) != MyValue(1))
        assert MyValue(1) != MyValue(2)
        assert not (MyValue(1) == MyValue(2))

        v1, v2 = MyValue(1), MyValue(2)
        assert v1 == v1
        assert v1 != v2
        assert not (v1 != v1)

        assert v1 <= v1
        assert not (v1 < v1)
        assert v1 >= v1
        assert not (v1 > v1)

        assert v1 <= v2
        assert v1 < v2
        assert not (v1 >= v2)
        assert not (v1 > v2)

        assert not (v2 <= v1)
        assert not (v2 < v1)
        assert v2 >= v1
        assert v2 > v1

        assert v1 != 1
        assert not (v1 == 1)
        assert not (v1 > 1)
        assert not (v1 >= 1)
        assert not (v1 < 1)
        assert not (v1 <= 1)
