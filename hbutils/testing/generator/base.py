from types import GeneratorType
from typing import Tuple, Mapping, Optional, List, Iterator, Set


def _single_to_tuple(s: object) -> Tuple[object, ...]:
    if isinstance(s, (list, tuple, GeneratorType, range)):
        return tuple(s)
    else:
        return (s,)


def _single_dict_process(s: Mapping[str, object]) -> Mapping[str, Tuple[object, ...]]:
    return {key: _single_to_tuple(value) for key, value in s.items()}


def _check_keys(item: Mapping[str, object], names: Set[str]):
    for key in item.keys():
        if key not in names:
            raise KeyError(f'Invalid key - {repr(key)}.')


class BaseGenerator:
    """
    Base generator class.
    """

    def __init__(self, values, names: Optional[List[str]] = None):
        """
        Constructor of the :class:`hbutils.testing.BaseGenerator` class.

        :param values: Selection values, such as ``{'a': [2, 3], 'b': ['b', 'c']}``.
        :param names: Names of the given generator, default is ``None`` which means use the sorted \
            key set of the values.
        """
        self.__values = _single_dict_process(values)
        self.__names = list(names or sorted(self.__values.keys()))

    @property
    def values(self) -> Mapping[str, Tuple[object, ...]]:
        """
        Selection values.
        """
        return self.__values

    @property
    def names(self) -> List[str]:
        """
        Name of the given generator.
        """
        return self.__names

    def cases(self) -> Iterator[Mapping[str, object]]:
        """
        Virtual method for cases, will be implemented in child classes.
        """
        raise NotImplementedError  # pragma: no cover

    def tuple_cases(self) -> Iterator[Tuple[object, ...]]:
        """
        Tuple-formatted cases, can be used to iterate.
        """
        for d in self.cases():
            yield tuple(d[name] for name in self.names)
