import pytest

from hbutils.testing import tmatrix


@pytest.fixture(scope='class')
def tmatrix_check_1():
    _check_id = 0
    expected = [
        (2, 'c', 9, 12), (3, 'c', 4, 6), (2, 'c', 1, 7),
        (3, 'b', 9, 12), (2, 'b', 4, 6), (3, 'b', 1, 7),
        (3, 'a', 9, 12), (2, 'a', 4, 6), (3, 'a', 1, 7),
    ]

    def _func(a, e, t, g):
        nonlocal _check_id
        _check_id += 1
        assert _check_id <= len(expected), f'Check id exceed - max is {len(expected)!r} but {_check_id!r} found.'
        assert (a, e, t, g) == expected[_check_id - 1], \
            f'Values not match - {expected[_check_id - 1]!r} expected but {(a, e, t, g)!r} found.'

    return _func


@pytest.mark.unittest
class TestTestingGeneratorFunc:
    def test_tmatrix_aetg(self):
        for i in range(5):
            assert tmatrix({
                'a': [2, 3],
                'e': ['a', 'b', 'c'],
                ('b', 'c'): [(1, 7), (4, 6), (9, 12)],
            }) == (
                       ['a', 'e', 'b', 'c'],
                       [
                           (2, 'c', 9, 12), (3, 'c', 4, 6), (2, 'c', 1, 7),
                           (3, 'b', 9, 12), (2, 'b', 4, 6), (3, 'b', 1, 7),
                           (3, 'a', 9, 12), (2, 'a', 4, 6), (3, 'a', 1, 7),
                       ]
                   )

    def test_tmatrix_matrix(self):
        for i in range(5):
            assert tmatrix({
                'a': [2, 3],
                'e': ['a', 'b', 'c'],
                ('b', 'c'): [(1, 7), (4, 6), (9, 12)],
            }, mode='matrix') == (
                       ['a', 'e', 'b', 'c'],
                       [
                           (2, 'a', 1, 7), (2, 'a', 4, 6), (2, 'a', 9, 12), (2, 'b', 1, 7),
                           (2, 'b', 4, 6), (2, 'b', 9, 12), (2, 'c', 1, 7), (2, 'c', 4, 6),
                           (2, 'c', 9, 12), (3, 'a', 1, 7), (3, 'a', 4, 6), (3, 'a', 9, 12),
                           (3, 'b', 1, 7), (3, 'b', 4, 6), (3, 'b', 9, 12), (3, 'c', 1, 7),
                           (3, 'c', 4, 6), (3, 'c', 9, 12)
                       ]
                   )

    @pytest.mark.parametrize(*tmatrix({
        'a': [2, 3],
        'e': ['a', 'b', 'c'],
        ('b', 'c'): [(1, 7), (4, 6), (9, 12)],
    }))
    def test_actual_use(self, a, e, b, c, tmatrix_check_1):
        tmatrix_check_1(a, e, b, c)
