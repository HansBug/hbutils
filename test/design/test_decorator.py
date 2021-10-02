from functools import wraps

import pytest

from hbutils.design import decolize


@pytest.mark.unittest
class TestDesignDecorator:
    def test_decolize(self):
        @decolize
        def deco(func, a=1, b=2):
            @wraps(func)
            def _new_func(*args, **kwargs):
                return func(*args, **kwargs) * a + b

            return _new_func

        @deco  # used as simple decorator
        def _func_1(a, b, c):
            return (a + b * 2) * c

        @deco(a=2)  # used as parameterized decorator
        def _func_2(a, b, c):
            return (a + b * 2) * c

        assert _func_1(1, 2, 3) == 17
        assert _func_2(1, 2, 3) == 32
        assert deco(lambda a, b: a + b)(1, 2) == 5
        assert deco(lambda a, b: a + b, a=3, b=4)(1, 2) == 13
        assert deco()(lambda a, b: a + b)(1, 2) == 5
        assert deco(a=3, b=4)(lambda a, b: a + b)(1, 2) == 13
