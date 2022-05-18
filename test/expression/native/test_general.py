import pytest

from hbutils.expression import GeneralExpression, expr, efunc, keep, CheckExpression, raw
from .test_feature import TestExpressionNativeComparableClass, TestExpressionNativeIndexedClass, \
    TestExpressionNativeAttredClass, TestExpressionNativeLogicalClass, TestExpressionNativeMathClass, \
    TestExpressionNativeCallableClass


@pytest.mark.unittest
class TestExpressionNativeGeneralClass(
    TestExpressionNativeComparableClass,
    TestExpressionNativeIndexedClass,
    TestExpressionNativeAttredClass,
    TestExpressionNativeCallableClass,
    TestExpressionNativeLogicalClass,
    TestExpressionNativeMathClass,
):
    __expcls__ = GeneralExpression

    def test_general_complex(self):
        e = self.__expcls__()
        f1 = efunc(e.upper())
        assert f1('str') == 'STR'

        f2 = efunc(e.capitalize()[::-1])
        assert f2('str') == 'rtS'


@pytest.mark.unittest
class TestExpressionNativeGeneral:
    def test_expr(self):
        e = expr(lambda x: 2 ** x)
        assert isinstance(e, GeneralExpression)
        f = efunc(e)
        assert f(1) == 2
        assert f(2) == 4
        assert f(3) == 8

    def test_expr_with_cls(self):
        e = expr(lambda x: 2 ** x, CheckExpression)
        assert isinstance(e, CheckExpression)
        f = efunc(e)
        assert f(1) == 2
        assert f(2) == 4
        assert f(3) == 8

    def test_keep(self):
        e = keep()
        assert isinstance(e, GeneralExpression)
        f = efunc(e)
        assert f(1) == 1
        assert f(2) == 2
        assert f(3) == 3

    def test_keep_with_cls(self):
        e = keep(CheckExpression)
        assert isinstance(e, CheckExpression)
        f = efunc(e)
        assert f(1) == 1
        assert f(2) == 2
        assert f(3) == 3

    def test_raw(self):
        def _my_func(x):
            return 1

        e = raw(_my_func)
        assert isinstance(e, GeneralExpression)
        f = efunc(e)
        assert f(1) is _my_func
        assert f(2) is _my_func
        assert f(3) is _my_func

    def test_raw_with_cls(self):
        def _my_func(x):
            return 1

        e = raw(_my_func, CheckExpression)
        assert isinstance(e, CheckExpression)
        f = efunc(e)
        assert f(1) is _my_func
        assert f(2) is _my_func
        assert f(3) is _my_func
