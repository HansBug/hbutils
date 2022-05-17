import pytest

from hbutils.expression import CheckExpression, efunc, ComparableExpression
from .test_base import TestExpressionNativeBaseClass


@pytest.mark.unittest
class TestExpressionNativeCheckClass(TestExpressionNativeBaseClass):
    __expcls__ = CheckExpression

    def test_check_simple(self):
        e = self.__expcls__(lambda x: x)
        f = efunc(e)
        assert f(1) == 1
        assert f(2) == 2
        assert f(3) == 3

    def test_check_eq(self):
        e = self.__expcls__(lambda x: x)
        f = efunc(e == 1)
        assert f(1) is True
        assert f(2) is False
        assert f(3) is False

        e1 = self.__expcls__(lambda x: x * 2)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f = efunc(e1 == e2)
        assert f(0) is False
        assert f(1) is True
        assert f(2) is True
        assert f(3) is False

    def test_check_ne(self):
        e = self.__expcls__(lambda x: x)
        f = efunc(e != 1)
        assert f(1) is False
        assert f(2) is True
        assert f(3) is True

        e1 = self.__expcls__(lambda x: x * 2)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f = efunc(e1 != e2)
        assert f(0) is True
        assert f(1) is False
        assert f(2) is False
        assert f(3) is True


@pytest.mark.unittest
class TestExpressionNativeComparableClass(TestExpressionNativeCheckClass):
    __expcls__ = ComparableExpression

    def test_check_ge(self):
        e = self.__expcls__(lambda x: x)
        f = efunc(e >= 2)
        assert f(1) is False
        assert f(2) is True
        assert f(3) is True

        e1 = self.__expcls__(lambda x: x * 2)
        e2 = self.__expcls__(lambda x: x + 2)
        f = efunc(e1 >= e2)
        assert f(0) is False
        assert f(1) is False
        assert f(2) is True
        assert f(3) is True

    def test_check_gt(self):
        e = self.__expcls__(lambda x: x)
        f = efunc(e > 2)
        assert f(1) is False
        assert f(2) is False
        assert f(3) is True

        e1 = self.__expcls__(lambda x: x * 2)
        e2 = self.__expcls__(lambda x: x + 2)
        f = efunc(e1 > e2)
        assert f(0) is False
        assert f(1) is False
        assert f(2) is False
        assert f(3) is True

    def test_check_le(self):
        e = self.__expcls__(lambda x: x)
        f = efunc(e <= 2)
        assert f(1) is True
        assert f(2) is True
        assert f(3) is False

        e1 = self.__expcls__(lambda x: x * 2)
        e2 = self.__expcls__(lambda x: x + 2)
        f = efunc(e1 <= e2)
        assert f(0) is True
        assert f(1) is True
        assert f(2) is True
        assert f(3) is False

    def test_check_lt(self):
        e = self.__expcls__(lambda x: x)
        f = efunc(e < 2)
        assert f(1) is True
        assert f(2) is False
        assert f(3) is False

        e1 = self.__expcls__(lambda x: x * 2)
        e2 = self.__expcls__(lambda x: x + 2)
        f = efunc(e1 < e2)
        assert f(0) is True
        assert f(1) is True
        assert f(2) is False
        assert f(3) is False
