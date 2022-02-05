from typing import Tuple, Mapping, Optional, List, Iterator


def _single_to_tuple(s: object) -> Tuple:
    if isinstance(s, (list, tuple)):
        return tuple(s)
    else:
        return (s,)


def _single_dict_process(s: Mapping[str, object]) -> Mapping[str, Tuple[object]]:
    return {key: _single_to_tuple(value) for key, value in s.items()}


class BaseGenerator:
    def __init__(self, values, names: Optional[List[str]] = None):
        self.__values = _single_dict_process(values)
        self.__names = list(names or sorted(self.__values.keys()))

    @property
    def values(self) -> Mapping[str, Tuple[object]]:
        return self.__values

    @property
    def names(self) -> List[str]:
        return self.__names

    def cases(self) -> Iterator[Mapping[str, object]]:
        raise NotImplementedError  # pragma: no cover

    def tuple_cases(self) -> Iterator[Tuple]:
        for d in self.cases():
            yield tuple(d[name] for name in self.names)
