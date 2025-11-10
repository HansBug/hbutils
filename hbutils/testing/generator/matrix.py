"""
Matrix generator module for generating test cases based on matrix combinations.

This module provides a MatrixGenerator class that generates all possible combinations
of parameter values in a matrix, similar to GitHub Actions' matrix strategy. It supports
including additional cases and excluding specific combinations.
"""

from typing import Iterator, Mapping, Optional, List, Any

from .base import BaseGenerator, _single_dict_process, _single_to_tuple, _check_keys


class MatrixGenerator(BaseGenerator):
    """
    Full matrix model, all the cases in this matrix will be iterated.
    
    This generator creates a cartesian product of all provided parameter values,
    with optional inclusions and exclusions to customize the generated test cases.
    """

    def __init__(self, values: Mapping[str, Any],
                 names: Optional[List[str]] = None,
                 includes: Optional[List[Mapping[str, Any]]] = None,
                 excludes: Optional[List[Mapping[str, Any]]] = None):
        """
        Constructor of the :class:`MatrixGenerator` class.
        
        It is similar to GitHub Action's matrix strategy, generating all combinations
        of the provided values with support for custom inclusions and exclusions.

        :param values: Matrix values, such as ``{'a': [2, 3], 'b': ['b', 'c']}``.
        :type values: Mapping[str, Any]
        :param names: Names of the given generator, default is ``None`` which means use the sorted \
            key set of the values.
        :type names: Optional[List[str]]
        :param includes: Include items, such as ``[{'a': 4, 'b': 'b'}]``, \
            default is ``None`` which means no extra inclusions.
        :type includes: Optional[List[Mapping[str, Any]]]
        :param excludes: Exclude Items, such as ``[{'a': 2, 'b': 'c'}]``, \
            default is ``None`` which means no extra exclusions.
        :type excludes: Optional[List[Mapping[str, Any]]]
        
        Example::
            >>> gen = MatrixGenerator(
            ...     {'a': [1, 2], 'b': ['x', 'y']},
            ...     includes=[{'a': 3, 'b': 'z'}],
            ...     excludes=[{'a': 1, 'b': 'x'}]
            ... )
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
        Get the include items.
        
        Include items are additional parameter combinations that will be added
        to the generated cases, even if they don't fit the original matrix values.

        :return: List of include item mappings.
        :rtype: List[Mapping[str, Any]]
        """
        return self.__includes

    @property
    def excludes(self) -> List[Mapping[str, Any]]:
        """
        Get the exclude items.
        
        Exclude items are parameter combinations that will be filtered out
        from the generated cases. A case is excluded if it matches all
        key-value pairs in any exclude item.

        :return: List of exclude item mappings.
        :rtype: List[Mapping[str, Any]]
        """
        return self.__excludes

    def cases(self) -> Iterator[Mapping[str, Any]]:
        """
        Get the cases in this matrix.
        
        Generates all possible combinations of the matrix values, applying
        exclusions and inclusions as specified. The method performs a cartesian
        product of all parameter values, then filters based on exclude rules,
        and finally adds any specified include cases.

        :return: Iterator yielding dictionaries representing each test case.
        :rtype: Iterator[Mapping[str, Any]]

        Examples::
            >>> from hbutils.testing import MatrixGenerator
            >>> for p in MatrixGenerator(
            ...         {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            ...         includes=[{'a': 4, 'r': 7}],
            ...         excludes=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
            ... ).cases():
            ...     print(p)
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

        def _check_single_exclude(dict_value: Mapping[str, Any], exclude: Mapping[str, Any]) -> bool:
            """
            Check if a single case matches an exclude pattern.
            
            :param dict_value: The case dictionary to check.
            :type dict_value: Mapping[str, Any]
            :param exclude: The exclude pattern to match against.
            :type exclude: Mapping[str, Any]
            
            :return: True if the case matches the exclude pattern, False otherwise.
            :rtype: bool
            """
            for key, value in exclude.items():
                if key not in dict_value or dict_value[key] not in value:
                    return False

            return True

        def _check_exclude(dict_value: Mapping[str, Any], excludes: List[Mapping[str, Any]]) -> bool:
            """
            Check if a case should be excluded based on all exclude patterns.
            
            :param dict_value: The case dictionary to check.
            :type dict_value: Mapping[str, Any]
            :param excludes: List of exclude patterns to check against.
            :type excludes: List[Mapping[str, Any]]
            
            :return: True if the case should be excluded, False otherwise.
            :rtype: bool
            """
            for exclude in excludes:
                if _check_single_exclude(dict_value, exclude):
                    return True

            return False

        def _matrix_recursion(depth: int, dict_value: Mapping[str, Any],
                              values: Mapping[str, Any],
                              excludes: List[Mapping[str, Any]]) -> Iterator[Mapping[str, Any]]:
            """
            Recursively generate matrix combinations.
            
            This function performs a depth-first traversal to generate all combinations
            of parameter values, checking exclusions at each level.
            
            :param depth: Current recursion depth (parameter index).
            :type depth: int
            :param dict_value: Current accumulated parameter values.
            :type dict_value: Mapping[str, Any]
            :param values: Available values for each parameter.
            :type values: Mapping[str, Any]
            :param excludes: Exclude patterns to apply.
            :type excludes: List[Mapping[str, Any]]
            
            :return: Iterator yielding valid case dictionaries.
            :rtype: Iterator[Mapping[str, Any]]
            """
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
