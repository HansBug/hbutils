from functools import lru_cache
from typing import Callable, Union

__all__ = [
    'efunc',
    'BaseExpression',
]


@lru_cache()
def _raw_expr_func():
    return getattr(BaseExpression, '_expr')


def _raw_expr(e) -> 'BaseExpression':
    return _raw_expr_func()(e)


def efunc(e: Union[Callable, 'BaseExpression']) -> Callable:
    return getattr(_raw_expr(e), '_call')


class BaseExpression:
    def __init__(self, func):
        self.__func = func

    def _call(self, x):
        return self.__func(x)

    def _func(self, func: Callable, *args, **kwargs):
        _args = tuple(efunc(v) for v in args)
        _kwargs = {k: efunc(v) for k, v in kwargs.items()}

        def _new_func(x):
            return func(
                *(v(x) for v in _args),
                **{k: v(x) for k, v in _kwargs.items()},
            )

        return self.__class__(_new_func)

    @classmethod
    def _expr(cls, v):
        if isinstance(v, BaseExpression):
            return v
        elif callable(v):
            return cls(v)
        else:
            return cls(lambda x: v)
