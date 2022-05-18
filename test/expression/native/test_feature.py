import pytest
from easydict import EasyDict

from hbutils.expression import CheckExpression, efunc, ComparableExpression, IndexedExpression, AttredExpression, \
    CallableExpression, LogicalExpression, MathExpression, BitwiseExpression
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


@pytest.mark.unittest
class TestExpressionNativeIndexedClass(TestExpressionNativeBaseClass):
    __expcls__ = IndexedExpression

    def test_indexed(self):
        e = self.__expcls__(lambda x: x)
        f = efunc(e['a'])
        assert f({'a': 1}) == 1
        assert f({'a': 100, 'b': 2}) == 100


@pytest.mark.unittest
class TestExpressionNativeAttredClass(TestExpressionNativeBaseClass):
    __expcls__ = AttredExpression

    def test_attr(self):
        class _MyContainer:
            def __init__(self, x):
                self.__x = x

            @property
            def a(self):
                return self.__x

        e = self.__expcls__(lambda x: x)
        f = efunc(e.a)
        assert f(EasyDict({'a': 1})) == 1
        assert f(EasyDict({'a': 100, 'b': 2})) == 100
        assert f(_MyContainer('str')) == 'str'


@pytest.mark.unittest
class TestExpressionNativeCallableClass(TestExpressionNativeBaseClass):
    __expcls__ = CallableExpression

    def test_callable(self):
        def _my_func(*args, **kwargs):
            return tuple(args), dict(kwargs)

        e = self.__expcls__(lambda x: _my_func)
        f = efunc(e(
            self.__expcls__(lambda x: x),
            self.__expcls__(lambda x: x + 1),
            a=self.__expcls__(lambda x: x * 2),
            b=self.__expcls__(lambda x: 2 ** x),
        ))

        assert f(2) == ((2, 3), {'a': 4, 'b': 4})
        assert f(3) == ((3, 4), {'a': 6, 'b': 8})


@pytest.mark.unittest
class TestExpressionNativeLogicalClass(TestExpressionNativeBaseClass):
    __expcls__ = LogicalExpression

    def test_logical_and(self):
        e1 = self.__expcls__(lambda x: x > 1)
        e2 = self.__expcls__(lambda x: x % 2 == 1)
        f1 = efunc(e1 & e2)
        assert f1(1) is False
        assert f1(2) is False
        assert f1(3) is True
        assert f1(4) is False
        assert f1(5) is True

        f2 = efunc(e1 & True)
        assert f2(1) is False
        assert f2(2) is True
        assert f2(3) is True
        assert f2(4) is True
        assert f2(5) is True

        f3 = efunc(e1 & False)
        assert f3(1) is False
        assert f3(2) is False
        assert f3(3) is False
        assert f3(4) is False
        assert f3(5) is False

    def test_logical_rand(self):
        e1 = self.__expcls__(lambda x: x > 1)
        e2 = self.__expcls__(lambda x: x % 2 == 1)

        f1 = efunc((lambda x: x <= 3) & e2)
        assert f1(1) is True
        assert f1(2) is False
        assert f1(3) is True
        assert f1(4) is False
        assert f1(5) is False

        f2 = efunc(True & e1)
        assert f2(1) is False
        assert f2(2) is True
        assert f2(3) is True
        assert f2(4) is True
        assert f2(5) is True

        f3 = efunc(False & e1)
        assert f3(1) is False
        assert f3(2) is False
        assert f3(3) is False
        assert f3(4) is False
        assert f3(5) is False

    def test_logical_or(self):
        e1 = self.__expcls__(lambda x: x > 1)
        e2 = self.__expcls__(lambda x: x % 2 == 1)
        f1 = efunc(e1 | e2)
        assert f1(0) is False
        assert f1(1) is True
        assert f1(2) is True
        assert f1(3) is True
        assert f1(4) is True
        assert f1(5) is True

        f2 = efunc(e2 | True)
        assert f2(0) is True
        assert f2(1) is True
        assert f2(2) is True
        assert f2(3) is True
        assert f2(4) is True
        assert f2(5) is True

        f3 = efunc(e2 | False)
        assert f3(0) is False
        assert f3(1) is True
        assert f3(2) is False
        assert f3(3) is True
        assert f3(4) is False
        assert f3(5) is True

    def test_logical_ror(self):
        e = self.__expcls__(lambda x: x % 2 == 1)
        f1 = efunc((lambda x: x % 4 == 0) | e)
        assert f1(0) is True
        assert f1(1) is True
        assert f1(2) is False
        assert f1(3) is True
        assert f1(4) is True
        assert f1(5) is True

        f2 = efunc(True | e)
        assert f2(0) is True
        assert f2(1) is True
        assert f2(2) is True
        assert f2(3) is True
        assert f2(4) is True
        assert f2(5) is True

        f3 = efunc(False | e)
        assert f3(0) is False
        assert f3(1) is True
        assert f3(2) is False
        assert f3(3) is True
        assert f3(4) is False
        assert f3(5) is True

    def test_logical_invert(self):
        e = self.__expcls__(lambda x: x % 2 == 1)
        f1 = efunc(~e)
        assert f1(0) is True
        assert f1(1) is False
        assert f1(2) is True
        assert f1(3) is False
        assert f1(4) is True
        assert f1(5) is False


@pytest.mark.unittest
class TestExpressionNativeMathClass(TestExpressionNativeBaseClass):
    __expcls__ = MathExpression

    def test_math_add(self):
        e1 = self.__expcls__(lambda x: x + 1)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f1 = efunc(e1 + e2)
        assert f1(0) == 2
        assert f1(1) == 4
        assert f1(2) == 7
        assert f1(3) == 12
        assert f1(4) == 21
        assert f1(5) == 38

        f2 = efunc(e1 + 2)
        assert f2(0) == 3
        assert f2(1) == 4
        assert f2(2) == 5
        assert f2(3) == 6
        assert f2(4) == 7
        assert f2(5) == 8

        f3 = efunc(e1 + (lambda x: 2 ** x))
        assert f3(0) == 2
        assert f3(1) == 4
        assert f3(2) == 7
        assert f3(3) == 12
        assert f3(4) == 21
        assert f3(5) == 38

    def test_math_radd(self):
        e = self.__expcls__(lambda x: x + 1)
        f2 = efunc(2 + e)
        assert f2(0) == 3
        assert f2(1) == 4
        assert f2(2) == 5
        assert f2(3) == 6
        assert f2(4) == 7
        assert f2(5) == 8

        f3 = efunc((lambda x: 2 ** x) + e)
        assert f3(0) == 2
        assert f3(1) == 4
        assert f3(2) == 7
        assert f3(3) == 12
        assert f3(4) == 21
        assert f3(5) == 38

    def test_math_sub(self):
        e1 = self.__expcls__(lambda x: x + 1)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f1 = efunc(e1 - e2)
        assert f1(0) == 0
        assert f1(1) == 0
        assert f1(2) == -1
        assert f1(3) == -4
        assert f1(4) == -11
        assert f1(5) == -26

        f2 = efunc(e1 - 2)
        assert f2(0) == -1
        assert f2(1) == 0
        assert f2(2) == 1
        assert f2(3) == 2
        assert f2(4) == 3
        assert f2(5) == 4

        f3 = efunc(e1 - (lambda x: 2 ** x))
        assert f3(0) == 0
        assert f3(1) == 0
        assert f3(2) == -1
        assert f3(3) == -4
        assert f3(4) == -11
        assert f3(5) == -26

    def test_math_rsub(self):
        e = self.__expcls__(lambda x: x + 1)
        f2 = efunc(2 - e)
        assert f2(0) == 1
        assert f2(1) == 0
        assert f2(2) == -1
        assert f2(3) == -2
        assert f2(4) == -3
        assert f2(5) == -4

        f3 = efunc((lambda x: 2 ** x) - e)
        assert f3(0) == 0
        assert f3(1) == 0
        assert f3(2) == 1
        assert f3(3) == 4
        assert f3(4) == 11
        assert f3(5) == 26

    def test_math_mul(self):
        e1 = self.__expcls__(lambda x: x + 1)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f1 = efunc(e1 * e2)
        assert f1(0) == 1
        assert f1(1) == 4
        assert f1(2) == 12
        assert f1(3) == 32
        assert f1(4) == 80
        assert f1(5) == 192

        f2 = efunc(e1 * 2)
        assert f2(0) == 2
        assert f2(1) == 4
        assert f2(2) == 6
        assert f2(3) == 8
        assert f2(4) == 10
        assert f2(5) == 12

        f3 = efunc(e1 * (lambda x: 2 ** x))
        assert f3(0) == 1
        assert f3(1) == 4
        assert f3(2) == 12
        assert f3(3) == 32
        assert f3(4) == 80
        assert f3(5) == 192

    def test_math_rmul(self):
        e = self.__expcls__(lambda x: x + 1)
        f2 = efunc(2 * e)
        assert f2(0) == 2
        assert f2(1) == 4
        assert f2(2) == 6
        assert f2(3) == 8
        assert f2(4) == 10
        assert f2(5) == 12

        f3 = efunc((lambda x: 2 ** x) * e)
        assert f3(0) == 1
        assert f3(1) == 4
        assert f3(2) == 12
        assert f3(3) == 32
        assert f3(4) == 80
        assert f3(5) == 192

    def test_math_truediv(self):
        e1 = self.__expcls__(lambda x: x + 1)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f1 = efunc(e1 / e2)
        assert f1(0) == pytest.approx(1.0)
        assert f1(1) == pytest.approx(1.0)
        assert f1(2) == pytest.approx(0.75)
        assert f1(3) == pytest.approx(0.5)
        assert f1(4) == pytest.approx(0.3125)
        assert f1(5) == pytest.approx(0.1875)

        f2 = efunc(e1 / 2)
        assert f2(0) == pytest.approx(0.5)
        assert f2(1) == pytest.approx(1.0)
        assert f2(2) == pytest.approx(1.5)
        assert f2(3) == pytest.approx(2.0)
        assert f2(4) == pytest.approx(2.5)
        assert f2(5) == pytest.approx(3.0)

        f3 = efunc(e1 / (lambda x: 2 ** x))
        assert f3(0) == pytest.approx(1.0)
        assert f3(1) == pytest.approx(1.0)
        assert f3(2) == pytest.approx(0.75)
        assert f3(3) == pytest.approx(0.5)
        assert f3(4) == pytest.approx(0.3125)
        assert f3(5) == pytest.approx(0.1875)

    def test_math_rtruediv(self):
        e = self.__expcls__(lambda x: x + 1)
        f2 = efunc(2 / e)
        assert f2(0) == pytest.approx(2.0)
        assert f2(1) == pytest.approx(1.0)
        assert f2(2) == pytest.approx(2 / 3)
        assert f2(3) == pytest.approx(0.5)
        assert f2(4) == pytest.approx(0.4)
        assert f2(5) == pytest.approx(1 / 3)

        f3 = efunc((lambda x: 2 ** x) / e)
        assert f3(0) == pytest.approx(1.0)
        assert f3(1) == pytest.approx(1.0)
        assert f3(2) == pytest.approx(4 / 3)
        assert f3(3) == pytest.approx(2.0)
        assert f3(4) == pytest.approx(3.2)
        assert f3(5) == pytest.approx(16 / 3)

    def test_math_floordiv(self):
        e1 = self.__expcls__(lambda x: x + 1)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f1 = efunc(e1 // e2)
        assert f1(0) == pytest.approx(1.0)
        assert f1(1) == pytest.approx(1.0)
        assert f1(2) == pytest.approx(0.0)
        assert f1(3) == pytest.approx(0.0)
        assert f1(4) == pytest.approx(0.0)
        assert f1(5) == pytest.approx(0.0)

        f2 = efunc(e1 // 2)
        assert f2(0) == pytest.approx(0.0)
        assert f2(1) == pytest.approx(1.0)
        assert f2(2) == pytest.approx(1.0)
        assert f2(3) == pytest.approx(2.0)
        assert f2(4) == pytest.approx(2.0)
        assert f2(5) == pytest.approx(3.0)

        f3 = efunc(e1 // (lambda x: 2 ** x))
        assert f3(0) == pytest.approx(1.0)
        assert f3(1) == pytest.approx(1.0)
        assert f3(2) == pytest.approx(0.0)
        assert f3(3) == pytest.approx(0.0)
        assert f3(4) == pytest.approx(0.0)
        assert f3(5) == pytest.approx(0.0)

    def test_math_rfloordiv(self):
        e = self.__expcls__(lambda x: x + 1)
        f2 = efunc(2 // e)
        assert f2(0) == pytest.approx(2.0)
        assert f2(1) == pytest.approx(1.0)
        assert f2(2) == pytest.approx(0.0)
        assert f2(3) == pytest.approx(0.0)
        assert f2(4) == pytest.approx(0.0)
        assert f2(5) == pytest.approx(0.0)

        f3 = efunc((lambda x: 2 ** x) // e)
        assert f3(0) == pytest.approx(1.0)
        assert f3(1) == pytest.approx(1.0)
        assert f3(2) == pytest.approx(1.0)
        assert f3(3) == pytest.approx(2.0)
        assert f3(4) == pytest.approx(3.0)
        assert f3(5) == pytest.approx(5.0)

    def test_math_mod(self):
        e1 = self.__expcls__(lambda x: x + 1)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f1 = efunc(e2 % e1)
        assert f1(0) == 0
        assert f1(1) == 0
        assert f1(2) == 1
        assert f1(3) == 0
        assert f1(4) == 1
        assert f1(5) == 2

        f2 = efunc(e1 % 2)
        assert f2(0) == 1
        assert f2(1) == 0
        assert f2(2) == 1
        assert f2(3) == 0
        assert f2(4) == 1
        assert f2(5) == 0

        f3 = efunc(e2 % (lambda x: x + 1))
        assert f3(0) == 0
        assert f3(1) == 0
        assert f3(2) == 1
        assert f3(3) == 0
        assert f3(4) == 1
        assert f3(5) == 2

    def test_math_rmod(self):
        e = self.__expcls__(lambda x: x + 1)
        f2 = efunc(123489 % e)
        assert f2(0) == 0
        assert f2(1) == 1
        assert f2(2) == 0
        assert f2(3) == 1
        assert f2(4) == 4
        assert f2(5) == 3

        f3 = efunc((lambda x: 2 ** x) % e)
        assert f3(0) == 0
        assert f3(1) == 0
        assert f3(2) == 1
        assert f3(3) == 0
        assert f3(4) == 1
        assert f3(5) == 2

    def test_math_pow(self):
        e1 = self.__expcls__(lambda x: x + 1)
        e2 = self.__expcls__(lambda x: 2 ** x)
        f1 = efunc(e2 ** e1)
        assert f1(0) == 1
        assert f1(1) == 4
        assert f1(2) == 64
        assert f1(3) == 4096
        assert f1(4) == 1048576
        assert f1(5) == 1073741824

        f2 = efunc(e1 ** 2)
        assert f2(0) == 1
        assert f2(1) == 4
        assert f2(2) == 9
        assert f2(3) == 16
        assert f2(4) == 25
        assert f2(5) == 36

        f3 = efunc(e2 ** (lambda x: x + 1))
        assert f3(0) == 1
        assert f3(1) == 4
        assert f3(2) == 64
        assert f3(3) == 4096
        assert f3(4) == 1048576
        assert f3(5) == 1073741824

    def test_math_rpow(self):
        e = self.__expcls__(lambda x: x + 1)
        f2 = efunc(2 ** e)
        assert f2(0) == 2
        assert f2(1) == 4
        assert f2(2) == 8
        assert f2(3) == 16
        assert f2(4) == 32
        assert f2(5) == 64

        f3 = efunc((lambda x: 2 ** x) ** e)
        assert f3(0) == 1
        assert f3(1) == 4
        assert f3(2) == 64
        assert f3(3) == 4096
        assert f3(4) == 1048576
        assert f3(5) == 1073741824

    def test_math_pos(self):
        e = self.__expcls__(lambda x: x + 1)
        f1 = efunc(+e)
        assert f1(-3) == -2
        assert f1(-2) == -1
        assert f1(-1) == 0
        assert f1(0) == 1
        assert f1(1) == 2
        assert f1(2) == 3

    def test_math_neg(self):
        e = self.__expcls__(lambda x: x + 1)
        f1 = efunc(-e)
        assert f1(-3) == 2
        assert f1(-2) == 1
        assert f1(-1) == 0
        assert f1(0) == -1
        assert f1(1) == -2
        assert f1(2) == -3


@pytest.mark.unittest
class TestExpressionNativeBitwiseClass(TestExpressionNativeBaseClass):
    __expcls__ = BitwiseExpression

    def test_bit_or(self):
        e1 = self.__expcls__(lambda x: x + 13)
        e2 = self.__expcls__(lambda x: x * 7)
        f1 = efunc(e1 | e2)
        assert f1(0) == 13
        assert f1(1) == 15
        assert f1(2) == 15
        assert f1(3) == 21
        assert f1(4) == 29
        assert f1(5) == 51

        f2 = efunc(e1 | 7)
        assert f2(0) == 15
        assert f2(1) == 15
        assert f2(2) == 15
        assert f2(3) == 23
        assert f2(4) == 23
        assert f2(5) == 23

        f3 = efunc(e1 | (lambda x: x * 7))
        assert f3(0) == 13
        assert f3(1) == 15
        assert f3(2) == 15
        assert f3(3) == 21
        assert f3(4) == 29
        assert f3(5) == 51

    def test_bit_ror(self):
        e = self.__expcls__(lambda x: x + 13)
        f2 = efunc(7 | e)
        assert f2(0) == 15
        assert f2(1) == 15
        assert f2(2) == 15
        assert f2(3) == 23
        assert f2(4) == 23
        assert f2(5) == 23

        f3 = efunc((lambda x: x * 7) | e)
        assert f3(0) == 13
        assert f3(1) == 15
        assert f3(2) == 15
        assert f3(3) == 21
        assert f3(4) == 29
        assert f3(5) == 51

    def test_bit_xor(self):
        e1 = self.__expcls__(lambda x: x + 13)
        e2 = self.__expcls__(lambda x: x * 7)
        f1 = efunc(e1 ^ e2)
        assert f1(0) == 13
        assert f1(1) == 9
        assert f1(2) == 1
        assert f1(3) == 5
        assert f1(4) == 13
        assert f1(5) == 49

        f2 = efunc(e1 ^ 7)
        assert f2(0) == 10
        assert f2(1) == 9
        assert f2(2) == 8
        assert f2(3) == 23
        assert f2(4) == 22
        assert f2(5) == 21

        f3 = efunc(e1 ^ (lambda x: x * 7))
        assert f3(0) == 13
        assert f3(1) == 9
        assert f3(2) == 1
        assert f3(3) == 5
        assert f3(4) == 13
        assert f3(5) == 49

    def test_bit_rxor(self):
        e = self.__expcls__(lambda x: x + 13)
        f2 = efunc(7 ^ e)
        assert f2(0) == 10
        assert f2(1) == 9
        assert f2(2) == 8
        assert f2(3) == 23
        assert f2(4) == 22
        assert f2(5) == 21

        f3 = efunc((lambda x: x * 7) ^ e)
        assert f3(0) == 13
        assert f3(1) == 9
        assert f3(2) == 1
        assert f3(3) == 5
        assert f3(4) == 13
        assert f3(5) == 49

    def test_bit_and(self):
        e1 = self.__expcls__(lambda x: x + 13)
        e2 = self.__expcls__(lambda x: x * 7)
        f1 = efunc(e1 & e2)
        assert f1(0) == 0
        assert f1(1) == 6
        assert f1(2) == 14
        assert f1(3) == 16
        assert f1(4) == 16
        assert f1(5) == 2

        f2 = efunc(e1 & 7)
        assert f2(0) == 5
        assert f2(1) == 6
        assert f2(2) == 7
        assert f2(3) == 0
        assert f2(4) == 1
        assert f2(5) == 2

        f3 = efunc(e1 & (lambda x: x * 7))
        assert f3(0) == 0
        assert f3(1) == 6
        assert f3(2) == 14
        assert f3(3) == 16
        assert f3(4) == 16
        assert f3(5) == 2

    def test_bit_rand(self):
        e = self.__expcls__(lambda x: x + 13)
        f2 = efunc(7 & e)
        assert f2(0) == 5
        assert f2(1) == 6
        assert f2(2) == 7
        assert f2(3) == 0
        assert f2(4) == 1
        assert f2(5) == 2

        f3 = efunc((lambda x: x * 7) & e)
        assert f3(0) == 0
        assert f3(1) == 6
        assert f3(2) == 14
        assert f3(3) == 16
        assert f3(4) == 16
        assert f3(5) == 2

    def test_bit_invert(self):
        e = self.__expcls__(lambda x: x + 13)
        f1 = efunc(~e)
        assert f1(-52) == 38
        assert f1(-39) == 25
        assert f1(-26) == 12
        assert f1(-13) == -1
        assert f1(0) == -14
        assert f1(13) == -27
        assert f1(26) == -40

    def test_bit_lshift(self):
        e = self.__expcls__(lambda x: x + 1)
        f1 = efunc(e << 2)
        assert f1(0) == 4
        assert f1(1) == 8
        assert f1(2) == 12
        assert f1(3) == 16
        assert f1(4) == 20
        assert f1(5) == 24

    def test_bit_rlshift(self):
        e = self.__expcls__(lambda x: x + 1)
        f1 = efunc(3 << e)
        assert f1(0) == 6
        assert f1(1) == 12
        assert f1(2) == 24
        assert f1(3) == 48
        assert f1(4) == 96
        assert f1(5) == 192

    def test_bit_rshift(self):
        e = self.__expcls__(lambda x: x + 20)
        f1 = efunc(e >> 2)
        assert f1(0) == 5
        assert f1(1) == 5
        assert f1(2) == 5
        assert f1(3) == 5
        assert f1(4) == 6
        assert f1(5) == 6

    def test_bit_rrshift(self):
        e = self.__expcls__(lambda x: x + 1)
        f1 = efunc(3923 >> e)
        assert f1(0) == 1961
        assert f1(1) == 980
        assert f1(2) == 490
        assert f1(3) == 245
        assert f1(4) == 122
        assert f1(5) == 61
