from abc import ABCMeta
from typing import Mapping, Optional, List, Tuple, Set, Iterator

__all__ = [
    'BaseMatrix'
]


def _check_keys(item: Mapping[str, object], names: Set[str]):
    for key in item.keys():
        if key not in names:
            raise KeyError(f'Invalid key - {repr(key)}.')


def _single_to_tuple(s: object) -> Tuple:
    if isinstance(s, (list, tuple)):
        return tuple(s)
    else:
        return (s,)


def _single_dict_process(s: Mapping[str, object]) -> Mapping[str, Tuple[object]]:
    return {key: _single_to_tuple(value) for key, value in s.items()}


class BaseMatrix(metaclass=ABCMeta):
    """
    Base class of the matrix model.
    """

    def __init__(self, values: Mapping[str, object],
                 include: Optional[List[Mapping[str, object]]] = None,
                 exclude: Optional[List[Mapping[str, object]]] = None
                 ):
        """
        Constructor of the :class:`hbutils.testing.matrix.base.BaseMatrix` class.
        It is similar to GitHub Action's matrix.

        :param values: Matrix values, such as ``{'a': [2, 3], 'b': ['b', 'c']}``.
        :param include: Include items, such as ``[{'a': 4, 'b': 'b'}]``, \
            default is ``None`` which means no extra inclusions.
        :param exclude: Exclude Items, such as ``[{'a': 2, 'b': 'c'}]``, \
            default is ``None`` which means no extra exclusions.
        """
        self.__values = _single_dict_process(values)
        self.__names = sorted(self.__values.keys())
        _name_set = set(self.__names)

        self.__include = [_single_dict_process(inc) for inc in (include or [])]
        for include in self.__include:
            _check_keys(include, _name_set)

        self.__exclude = [_single_dict_process(exc) for exc in (exclude or [])]
        for exclude in self.__exclude:
            _check_keys(exclude, _name_set)

    @property
    def values(self) -> Mapping[str, Tuple[object]]:
        """
        Matrix values.
        """
        return self.__values

    @property
    def names(self) -> List[str]:
        return self.__names

    @property
    def include(self) -> List[Mapping[str, object]]:
        """
        Include items.
        """
        return self.__include

    @property
    def exclude(self) -> List[Mapping[str, object]]:
        """
        Exclude items.
        """
        return self.__exclude

    def cases(self) -> Iterator[Mapping[str, object]]:
        """
        Get the cases in this matrix.

        .. note::
            This is an abstract class, function ``cases`` only represents an interface.
            The features will be implemented in child classes.
        """
        raise NotImplementedError  # pragma: no cover
