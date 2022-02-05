from typing import Iterator, Mapping, Optional, List, Set

from .base import BaseGenerator, _single_dict_process, _single_to_tuple


def _check_keys(item: Mapping[str, object], names: Set[str]):
    for key in item.keys():
        if key not in names:
            raise KeyError(f'Invalid key - {repr(key)}.')


class MatrixGenerator(BaseGenerator):
    """
    Full matrix model, all the cases in this matrix will be iterated.
    """

    def __init__(self, values: Mapping[str, object],
                 names: Optional[List[str]] = None,
                 include: Optional[List[Mapping[str, object]]] = None,
                 exclude: Optional[List[Mapping[str, object]]] = None
                 ):
        """
        Constructor of the :class:`hbutils.testing.matrix.base.BaseMatrix` class.
        It is similar to GitHub Action's matrix.

        :param values: Matrix values, such as ``{'a': [2, 3], 'b': ['b', 'c']}``.
        :param names: Names of the given generator, default is ``None`` which means use the sorted \
            key set of the values.
        :param include: Include items, such as ``[{'a': 4, 'b': 'b'}]``, \
            default is ``None`` which means no extra inclusions.
        :param exclude: Exclude Items, such as ``[{'a': 2, 'b': 'c'}]``, \
            default is ``None`` which means no extra exclusions.
        """
        BaseGenerator.__init__(self, values, names)
        _name_set = set(self.names)

        self.__include = [_single_dict_process(inc) for inc in (include or [])]
        for include in self.__include:
            _check_keys(include, _name_set)

        self.__exclude = [_single_dict_process(exc) for exc in (exclude or [])]
        for exclude in self.__exclude:
            _check_keys(exclude, _name_set)

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

        Examples::
            >>> from hbutils.testing import MatrixGenerator
            >>> for p in MatrixGenerator(
            ...         {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            ...         include=[{'a': 4, 'r': 7}],
            ...         exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
            ... ).cases():
            >>>     print(p)
            {'a': 1, 'b': 'a', 'r': 4}
            {'a': 1, 'b': 'a', 'r': 5}
            {'a': 1, 'b': 'b', 'r': 4}
            {'a': 1, 'b': 'b', 'r': 5}
            {'a': 2, 'b': 'a', 'r': 3}
            {'a': 2, 'b': 'a', 'r': 4}
            {'a': 2, 'b': 'a', 'r': 5}
            {'a': 2, 'b': 'b', 'r': 3}
            {'a': 2, 'b': 'b', 'r': 4}
            {'a': 2, 'b': 'b', 'r': 5}
            {'a': 3, 'b': 'a', 'r': 3}
            {'a': 3, 'b': 'a', 'r': 4}
            {'a': 3, 'b': 'a', 'r': 5}
            {'a': 4, 'b': 'b', 'r': 7}

        """
        n = len(self.names)

        def _check_single_exclude(dict_value, exclude):
            for key, value in exclude.items():
                if key not in dict_value or dict_value[key] not in value:
                    return False

            return True

        def _check_exclude(dict_value, excludes):
            for exclude in excludes:
                if _check_single_exclude(dict_value, exclude):
                    return True

            return False

        def _matrix_recursion(depth, dict_value, values, excludes):
            if _check_exclude(dict_value, excludes):
                return

            if depth < n:
                name = self.names[depth]
                for curitem in values[name]:
                    yield from _matrix_recursion(depth + 1, {**dict_value, name: curitem}, values, excludes)
            else:
                yield dict_value

        value_items = [self.values, *({
            name: _single_to_tuple(include[name]) if name in include else self.values[name]
            for name in self.names
        } for include in self.include)]
        local_excludes = [*self.exclude]
        for vis in value_items:
            yield from _matrix_recursion(0, {}, vis, local_excludes)
            local_excludes.append(vis)
