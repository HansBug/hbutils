"""
Test matrix generation utilities for parameterized test cases.

This module provides a compact interface for generating parameter combinations
used in test parameterization. It supports two modes of generation:

* :class:`MatrixMode` - Enumeration of available generation modes.
* :func:`tmatrix` - Generate parameter names and test case tuples for pytest.

The primary entry point is :func:`tmatrix`, which converts a parameter range
specification into a list of parameter names and a list of case tuples. These
results are compatible with ``pytest.mark.parametrize`` and can be used for
both full Cartesian matrix generation and AETG-based combinatorial testing.

.. note::
   The AETG algorithm can reduce the number of test cases while preserving
   combinatorial coverage of parameter interactions.

Example::

    >>> from hbutils.testing.generator.func import tmatrix
    >>> names, cases = tmatrix({
    ...     'a': [1, 2],
    ...     'b': ['x', 'y'],
    ...     ('c', 'd'): [(0, 1), (1, 2)]
    ... }, mode='aetg', level=2)
    >>> names
    ['a', 'b', 'c', 'd']
    >>> cases  # doctest: +ELLIPSIS
    [(1, 'x', 0, 1), ...]
"""

from enum import IntEnum, auto
from typing import List, Mapping, Union, Tuple, Optional, Any

from .aetg import AETGGenerator
from .matrix import MatrixGenerator
from ...model import int_enum_loads
from ...reflection import progressive_for

__all__ = ['tmatrix']


@int_enum_loads(enable_int=False, name_preprocess=str.upper)
class MatrixMode(IntEnum):
    """
    Enumeration of matrix generation modes.

    :cvar AETG: AETG (Automatic Efficient Test Generator) mode for combinatorial testing.
    :cvar MATRIX: Full Cartesian product matrix mode.
    """
    AETG = auto()
    MATRIX = auto()


def tmatrix(ranges: Mapping[Union[str, Tuple[str, ...]], List[Any]],
            mode: Union[str, MatrixMode] = 'aetg',
            seed: Optional[int] = 0,
            level: int = 2) -> Tuple[List[str], List[Tuple[Any, ...]]]:
    """
    Generate test matrix for parameterized testing.

    This function creates a test matrix that can be directly used with pytest's
    parametrize decorator. It supports two generation modes: AETG for efficient
    combinatorial testing and MATRIX for full Cartesian product generation.

    :param ranges: Mapping of parameter names to their possible values. Keys can be either
                   a single string (for one parameter) or a tuple of strings (for multiple
                   parameters that should be varied together). Values are lists of possible
                   values for the parameter(s).
    :type ranges: Mapping[Union[str, Tuple[str, ...]], List[Any]]
    :param mode: Generation mode, accepts ``'aetg'``/``'matrix'`` (case-insensitive) or a
                 :class:`MatrixMode` instance. Default is ``'aetg'``.
    :type mode: Union[str, MatrixMode]
    :param seed: Random seed for AETG mode. Default is ``0`` which produces deterministic results.
                 Set to ``None`` for non-deterministic generation.
    :type seed: Optional[int]
    :param level: Coverage level for AETG algorithm, indicating the strength of combinatorial
                  coverage (e.g., ``2`` for pairwise coverage). Default is ``2``.
    :type level: int
    :return: A tuple containing ``(parameter_names, test_cases)`` where ``parameter_names`` is a list
             of parameter names and ``test_cases`` is a list of tuples, each representing one test case.
    :rtype: Tuple[List[str], List[Tuple[Any, ...]]]
    :raises ValueError: If an invalid mode is specified.

    Examples::
        >>> from hbutils.testing import tmatrix
        >>> names, values = tmatrix(
        ...     {
        ...         'a': [2, 3],
        ...         'e': ['a', 'b', 'c'],
        ...         ('b', 'c'): [(1, 7), (4, 6), (9, 12)],
        ...     }
        ... )
        >>> print(names)
        ['a', 'e', 'b', 'c']
        >>> for i, v in enumerate(values):
        ...     print(i, v)
        0 (2, 'c', 9, 12)
        1 (3, 'c', 4, 6)
        2 (2, 'c', 1, 7)
        3 (3, 'b', 9, 12)
        4 (2, 'b', 4, 6)
        5 (3, 'b', 1, 7)
        6 (3, 'a', 9, 12)
        7 (2, 'a', 4, 6)
        8 (3, 'a', 1, 7)

    .. note::
        This can be directly used in ``pytest.mark.parametrize`` function.

        >>> import pytest
        >>> @pytest.mark.unittest
        ... class TestTestingGeneratorFunc:
        ...     @pytest.mark.parametrize(*tmatrix({
        ...         'a': [2, 3],
        ...         'e': ['a', 'b', 'c'],
        ...         ('b', 'c'): [(1, 7), (4, 6), (9, 12)],
        ...     }))
        ...     def test_tmatrix_usage(self, a, e, b, c):
        ...         print(a, e, b, c)
    """
    mode = MatrixMode.loads(mode)

    # Create internal key mapping for processing
    key_map: Mapping[str, Union[str, Tuple[str, ...]]] = {}
    final_names: List[str] = []
    final_values: Mapping[str, List[Any]] = {}
    for ki, (key, value) in enumerate(ranges.items()):
        kname = f'key-{ki}'
        key_map[kname] = key
        final_names.append(kname)
        final_values[kname] = value

    # Extract all parameter names from the ranges
    names: List[str] = []
    for key in ranges.keys():
        if isinstance(key, str):
            names.append(key)
        elif isinstance(key, tuple):
            for k in key:
                names.append(k)

    # Create appropriate generator based on mode
    if mode == MatrixMode.MATRIX:
        generator = MatrixGenerator(final_values, final_names)
    elif mode == MatrixMode.AETG:
        generator = AETGGenerator(
            final_values, final_names, rnd=seed,
            pairs=list(progressive_for(final_names, min(level, len(names)))),
        )
    else:
        raise ValueError(f'Invalid mode - {mode!r}.')  # pragma: no cover

    # Generate test cases and transform them to final format
    pairs: List[Tuple[Any, ...]] = []
    for case in generator.cases():
        _v_case: Mapping[str, Any] = {}
        for name in final_names:
            key = key_map[name]
            if isinstance(key, str):
                _v_case[key] = case[name]
            elif isinstance(key, tuple):
                for ikey, ivalue in zip(key, case[name]):
                    _v_case[ikey] = ivalue

        pairs.append(tuple(_v_case[name] for name in names))

    return names, pairs
