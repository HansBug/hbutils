"""
Module for generating test cases with different combinations of values.

This module provides base functionality for creating test case generators that can produce
various combinations of input values. It includes utilities for converting single values
to tuples and processing dictionaries of values for test case generation.

The main class :class:`BaseGenerator` serves as a foundation for implementing specific
test case generation strategies in derived classes.
"""

from types import GeneratorType
from typing import Tuple, Mapping, Optional, List, Iterator, Set


def _single_to_tuple(s: object) -> Tuple[object, ...]:
    """
    Convert a single value or iterable to a tuple.

    :param s: The value to convert. Can be a single value, list, tuple, generator, or range.
    :type s: object

    :return: A tuple containing the value(s). If input is already iterable (list, tuple, 
        generator, or range), returns it as a tuple. Otherwise, wraps the single value in a tuple.
    :rtype: Tuple[object, ...]

    Example::
        >>> _single_to_tuple(5)
        (5,)
        >>> _single_to_tuple([1, 2, 3])
        (1, 2, 3)
        >>> _single_to_tuple((4, 5))
        (4, 5)
    """
    if isinstance(s, (list, tuple, GeneratorType, range)):
        return tuple(s)
    else:
        return (s,)


def _single_dict_process(s: Mapping[str, object]) -> Mapping[str, Tuple[object, ...]]:
    """
    Process a dictionary by converting all values to tuples.

    :param s: A dictionary with string keys and arbitrary values.
    :type s: Mapping[str, object]

    :return: A new dictionary with the same keys, but all values converted to tuples.
    :rtype: Mapping[str, Tuple[object, ...]]

    Example::
        >>> _single_dict_process({'a': 1, 'b': [2, 3]})
        {'a': (1,), 'b': (2, 3)}
    """
    return {key: _single_to_tuple(value) for key, value in s.items()}


def _check_keys(item: Mapping[str, object], names: Set[str]):
    """
    Validate that all keys in the item exist in the allowed names set.

    :param item: A dictionary to validate.
    :type item: Mapping[str, object]
    :param names: A set of valid key names.
    :type names: Set[str]

    :raises KeyError: If any key in item is not present in the names set.

    Example::
        >>> _check_keys({'a': 1, 'b': 2}, {'a', 'b', 'c'})  # No error
        >>> _check_keys({'a': 1, 'd': 2}, {'a', 'b', 'c'})  # Raises KeyError
        Traceback (most recent call last):
            ...
        KeyError: "Invalid key - 'd'."
    """
    for key in item.keys():
        if key not in names:
            raise KeyError(f'Invalid key - {repr(key)}.')


class BaseGenerator:
    """
    Base generator class for creating test case combinations.

    This class provides the foundation for generating test cases with different combinations
    of input values. It stores a mapping of parameter names to their possible values and
    provides methods to iterate over test cases in different formats.

    Subclasses should implement the :meth:`cases` method to define the specific strategy
    for generating test case combinations.
    """

    def __init__(self, values: Mapping[str, object], names: Optional[List[str]] = None):
        """
        Initialize the BaseGenerator with values and optional names.

        :param values: A mapping of parameter names to their possible values. Each value can be
            a single item or an iterable (list, tuple, generator, range). Single values will be
            automatically converted to tuples. For example: ``{'a': [2, 3], 'b': ['x', 'y']}``.
        :type values: Mapping[str, object]
        :param names: Optional list of parameter names to define the order of parameters.
            If not provided, uses the sorted keys from values. Default is ``None``.
        :type names: Optional[List[str]]

        Example::
            >>> gen = BaseGenerator({'a': [1, 2], 'b': ['x', 'y']})
            >>> gen.names
            ['a', 'b']
            >>> gen.values
            {'a': (1, 2), 'b': ('x', 'y')}
        """
        self.__values = _single_dict_process(values)
        self.__names = list(names or sorted(self.__values.keys()))

    @property
    def values(self) -> Mapping[str, Tuple[object, ...]]:
        """
        Get the selection values for test case generation.

        :return: A mapping of parameter names to tuples of possible values.
        :rtype: Mapping[str, Tuple[object, ...]]

        Example::
            >>> gen = BaseGenerator({'a': [1, 2], 'b': 'x'})
            >>> gen.values
            {'a': (1, 2), 'b': ('x',)}
        """
        return self.__values

    @property
    def names(self) -> List[str]:
        """
        Get the ordered list of parameter names.

        :return: A list of parameter names in the order they should be used.
        :rtype: List[str]

        Example::
            >>> gen = BaseGenerator({'b': [1, 2], 'a': [3, 4]})
            >>> gen.names
            ['a', 'b']
        """
        return self.__names

    def cases(self) -> Iterator[Mapping[str, object]]:
        """
        Generate test cases as dictionaries.

        This is a virtual method that must be implemented in subclasses to define
        the specific strategy for generating test case combinations.

        :return: An iterator yielding dictionaries where keys are parameter names
            and values are the selected values for that test case.
        :rtype: Iterator[Mapping[str, object]]

        :raises NotImplementedError: This method must be implemented by subclasses.

        Example::
            >>> # In a subclass implementation:
            >>> for case in generator.cases():
            ...     print(case)
            {'a': 1, 'b': 'x'}
            {'a': 2, 'b': 'y'}
        """
        raise NotImplementedError  # pragma: no cover

    def tuple_cases(self) -> Iterator[Tuple[object, ...]]:
        """
        Generate test cases as tuples.

        This method converts the dictionary-based cases from :meth:`cases` into tuples,
        with values ordered according to :attr:`names`. This format is convenient for
        use with testing frameworks that expect tuple arguments.

        :return: An iterator yielding tuples of test case values in the order defined by names.
        :rtype: Iterator[Tuple[object, ...]]

        Example::
            >>> # Assuming cases() yields {'a': 1, 'b': 'x'} and {'a': 2, 'b': 'y'}
            >>> # and names is ['a', 'b']
            >>> for case in generator.tuple_cases():
            ...     print(case)
            (1, 'x')
            (2, 'y')
        """
        for d in self.cases():
            yield tuple(d[name] for name in self.names)
