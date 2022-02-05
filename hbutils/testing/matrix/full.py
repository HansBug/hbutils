from typing import Iterator, Mapping

from .base import BaseMatrix, _single_to_tuple

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
