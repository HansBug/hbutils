from enum import IntEnum, auto
from typing import List, Mapping, Union, Tuple, Optional

from .aetg import AETGGenerator
from .matrix import MatrixGenerator
from ...model import int_enum_loads
from ...reflection import progressive_for

__all__ = ['tmatrix']


@int_enum_loads(enable_int=False, name_preprocess=str.upper)
class MatrixMode(IntEnum):
    AETG = auto()
    MATRIX = auto()


def tmatrix(ranges: Mapping[Union[str, Tuple[str, ...]], List],
            mode='aetg', seed: Optional[int] = 0, level: int = 2) -> Tuple[List[str], List[Tuple]]:
    """
    Overview:
        Test matrix generator, which can be used in ``pytest.mark.parameterize``.

    :param ranges: Ranges of the values
    :param mode: Mode of the matrix, should be one of the ``aetg`` or ``matrix``. Default is ``aetg``.
    :param seed: Random seed, default is ``0`` which means the result is fixed (recommended).
    :param level: Lavel of AETG generating algorithm, default is ``2``.
    :returns: A tuple - ``(names, values)``.

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

    key_map = {}
    final_names = []
    final_values = {}
    for ki, (key, value) in enumerate(ranges.items()):
        kname = f'key-{ki}'
        key_map[kname] = key
        final_names.append(kname)
        final_values[kname] = value

    names = []
    for key in ranges.keys():
        if isinstance(key, str):
            names.append(key)
        elif isinstance(key, tuple):
            for k in key:
                names.append(k)

    if mode == MatrixMode.MATRIX:
        generator = MatrixGenerator(final_values, final_names)
    elif mode == MatrixMode.AETG:
        generator = AETGGenerator(
            final_values, final_names, rnd=seed,
            pairs=list(progressive_for(final_names, min(level, len(names)))),
        )
    else:
        raise ValueError(f'Invalid mode - {mode!r}.')  # pragma: no cover

    pairs = []
    for case in generator.cases():
        _v_case = {}
        for name in final_names:
            key = key_map[name]
            if isinstance(key, str):
                _v_case[key] = case[name]
            elif isinstance(key, tuple):
                for ikey, ivalue in zip(key, case[name]):
                    _v_case[ikey] = ivalue

        pairs.append(tuple(_v_case[name] for name in names))

    return names, pairs
