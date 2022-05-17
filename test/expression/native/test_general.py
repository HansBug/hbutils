import pytest

from hbutils.expression import GeneralExpression, expr, efunc, keep, CheckExpression
from .test_feature import TestExpressionNativeCheckClass


@pytest.mark.unittest
class TestExpressionNativeGeneralClass(
    TestExpressionNativeCheckClass,
):
    __expcls__ = GeneralExpression


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
