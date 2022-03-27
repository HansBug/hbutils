from typing import Union, Iterator

from .grammar import _build_syntax
from ..model import asitems, hasheq


@hasheq()
@asitems(['name'])
class EnvVar:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    def __repr__(self):
        return self.__name


@hasheq()
@asitems(['first', 'second', 'op'])
class MarkerExpr:
    def __init__(self, first, second, op):
        self.__first = first
        self.__second = second
        self.__op = op

    @property
    def first(self) -> Union[str, EnvVar]:
        return self.__first

    @property
    def second(self) -> Union[str, EnvVar]:
        return self.__second

    @property
    def op(self) -> str:
        return self.__op

    def __repr__(self):
        return f'{repr(self.__first)} {self.__op} {repr(self.__second)}'

    def __and__(self, other) -> 'MarkerAnd':
        return MarkerAnd(self, other)

    def __or__(self, other) -> 'MarkerOr':
        return MarkerOr(self, other)


class _MarkerChain:
    def __init__(self, *exprs):
        self._exprs = tuple(exprs)

    def __len__(self) -> int:
        return len(self._exprs)

    def __getitem__(self, item) -> Union[MarkerExpr, 'MarkerAnd', 'MarkerOr']:
        return self._exprs[item]

    def __iter__(self) -> Iterator[Union[MarkerExpr, 'MarkerAnd', 'MarkerOr']]:
        return iter(self._exprs)

    def __hash__(self):
        return hash((type(self), self._exprs))

    def __eq__(self, other):
        if self is other:
            return True
        elif type(self) == type(other):
            # noinspection PyProtectedMember
            return self._exprs == other._exprs
        else:
            return False


class MarkerAnd(_MarkerChain):
    @classmethod
    def _try_wrap(cls, x):
        if isinstance(x, (MarkerAnd, MarkerOr)):
            return f'({repr(x)})'
        else:
            return repr(x)

    def __repr__(self):
        return ' and '.join(map(self._try_wrap, self._exprs))

    def __and__(self, other) -> 'MarkerAnd':
        return MarkerAnd(*self._exprs, other)

    def __or__(self, other) -> 'MarkerOr':
        return MarkerOr(self, other)


class MarkerOr(_MarkerChain):
    @classmethod
    def _try_wrap(cls, x):
        if isinstance(x, MarkerOr):
            return f'({repr(x)})'
        else:
            return repr(x)

    def __repr__(self):
        return ' or '.join(map(self._try_wrap, self._exprs))

    def __or__(self, other) -> 'MarkerOr':
        return MarkerOr(*self._exprs, other)

    def __and__(self, other) -> 'MarkerAnd':
        return MarkerAnd(self, other)


def _load_marker_from_data(data):
    mark, *_ = data
    if mark == 'and':
        return _load_marker_from_data(data[1]) & _load_marker_from_data(data[2])
    elif mark == 'or':
        return _load_marker_from_data(data[1]) | _load_marker_from_data(data[2])
    elif mark == 'env':
        return EnvVar(data[1])
    elif mark == 'val':
        return data[1]
    else:
        return MarkerExpr(_load_marker_from_data(data[1]), _load_marker_from_data(data[2]), data[0])


def load_marker(data) -> Union[MarkerExpr, MarkerOr, MarkerAnd]:
    if isinstance(data, (MarkerExpr, MarkerAnd, MarkerOr)):
        return data
    elif isinstance(data, tuple):
        return _load_marker_from_data(data)
    elif isinstance(data, str):
        return load_marker(_build_syntax(data).marker())
    else:
        raise TypeError(f'Unknown marker type - {repr(type(data))}.')
