import pytest

from hbutils.expression import BaseExpression, efunc


@pytest.mark.unittest
class TestExpressionNativeBase:
    def test_func(self):
        e = BaseExpression(lambda x: x + 1)

        f = efunc(e)
        assert f(1) == 2
        assert f(2) == 3

    def test_inherit(self):
        class MyInheritExpression(BaseExpression):
            def add(self, v):
                return self._func(lambda x, y: x + y, self, v)

        e = MyInheritExpression(lambda x: x).add(MyInheritExpression(lambda x: 2 ** x))
        f = efunc(e)
        assert f(1) == 3
        assert f(2) == 6
        assert f(3) == 11


@pytest.mark.unittest
class TestExpressionNativeBaseClass:
    __expcls__ = BaseExpression

    def test_basic(self):
        e = self.__expcls__(lambda x: x)

        f = efunc(e)
        assert f(1) == 1
        assert f(2) == 2
        assert f('str') == 'str'
        assert f(None) is None

    def test_expr(self):
        class MyExprExpression(self.__expcls__):
            @classmethod
            def expr(cls, v):
                return cls._expr(v)

        e1 = MyExprExpression.expr(1)
        assert isinstance(e1, MyExprExpression)
        f1 = efunc(e1)
        assert f1(1) == 1
        assert f1(2) == 1
        assert f1(3) == 1

        e2 = MyExprExpression.expr(lambda x: x + 1)
        assert isinstance(e2, MyExprExpression)
        f2 = efunc(e2)
        assert f2(1) == 2
        assert f2(2) == 3
        assert f2(3) == 4

        e3 = MyExprExpression.expr(e2)
        assert isinstance(e3, MyExprExpression)
        f3 = efunc(e3)
        assert f3(1) == 2
        assert f3(2) == 3
        assert f3(3) == 4
