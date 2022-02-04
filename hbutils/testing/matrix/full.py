from typing import Iterator, Mapping

from .base import BaseMatrix

__all__ = [
    'FullMatrix',
]


class FullMatrix(BaseMatrix):
    """
    Full matrix model, all the cases in this matrix will be iterated.
    """

    def cases(self) -> Iterator[Mapping[str, object]]:
        """
        Get the cases in this matrix.

        Examples::
            >>> from hbutils.testing import FullMatrix
            >>> for p in FullMatrix(
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
                if key not in dict_value or dict_value[key] != value:
                    return False

            return True

        def _check_exclude(dict_value):
            for exclude in self.exclude:
                if _check_single_exclude(dict_value, exclude):
                    return True

            return False

        def _matrix_recursion(depth, dict_value):
            if _check_exclude(dict_value):
                return

            if depth < n:
                name = self.names[depth]
                for curitem in self.values[name]:
                    yield from _matrix_recursion(depth + 1, {**dict_value, name: curitem})
            else:
                yield dict_value

        def _include_recursion(depth, dict_value, incs):
            if _check_exclude(dict_value):
                return

            if depth < n:
                name = self.names[depth]
                if name in incs:
                    yield from _include_recursion(depth + 1, {**dict_value, name: incs[name]}, incs)
                else:
                    for curitem in self.values[name]:
                        yield from _include_recursion(depth + 1, {**dict_value, name: curitem}, incs)
            else:
                yield dict_value

        yield from _matrix_recursion(0, {})
        for include in self.include:
            yield from _include_recursion(0, {}, include)
