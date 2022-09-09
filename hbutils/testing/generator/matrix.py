from typing import Iterator, Mapping, Optional, List, Any

from .base import BaseGenerator, _single_dict_process, _single_to_tuple, _check_keys


class MatrixGenerator(BaseGenerator):
    """
    Full matrix model, all the cases in this matrix will be iterated.
    """

    def __init__(self, values: Mapping[str, Any],
                 names: Optional[List[str]] = None,
                 includes: Optional[List[Mapping[str, Any]]] = None,
                 excludes: Optional[List[Mapping[str, Any]]] = None):
        """
        Constructor of the :class:`hbutils.testing.MatrixGenerator` class.
        It is similar to GitHub Action's matrix.

        :param values: Matrix values, such as ``{'a': [2, 3], 'b': ['b', 'c']}``.
        :param names: Names of the given generator, default is ``None`` which means use the sorted \
            key set of the values.
        :param includes: Include items, such as ``[{'a': 4, 'b': 'b'}]``, \
            default is ``None`` which means no extra inclusions.
        :param excludes: Exclude Items, such as ``[{'a': 2, 'b': 'c'}]``, \
            default is ``None`` which means no extra exclusions.
        """
        BaseGenerator.__init__(self, values, names)
        _name_set = set(self.names)

        self.__includes = [_single_dict_process(inc) for inc in (includes or [])]
        for includes in self.__includes:
            _check_keys(includes, _name_set)

        self.__excludes = [_single_dict_process(exc) for exc in (excludes or [])]
        for excludes in self.__excludes:
            _check_keys(excludes, _name_set)

    @property
    def includes(self) -> List[Mapping[str, Any]]:
        """
        Include items.
        """
        return self.__includes

    @property
    def excludes(self) -> List[Mapping[str, Any]]:
        """
        Exclude items.
        """
        return self.__excludes

    def cases(self) -> Iterator[Mapping[str, Any]]:
        """
        Get the cases in this matrix.

        Examples::
            >>> from hbutils.testing import MatrixGenerator
            >>> for p in MatrixGenerator(
            ...         {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            ...         includes=[{'a': 4, 'r': 7}],
            ...         excludes=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
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
        } for include in self.includes)]
        local_excludes = [*self.excludes]
        for vis in value_items:
            yield from _matrix_recursion(0, {}, vis, local_excludes)
            local_excludes.append(vis)
