import random

import pytest

from hbutils.collection import swap_2d, cube_shape, dimension_switch


def _create_cube(*size):
    if size:
        return [
            _create_cube(*size[1:])
            for _ in range(size[0])
        ]
    else:
        return random.randint(-5, 15)


@pytest.mark.unittest
class TestCollectionDimension:
    def test_cube_shape(self):
        a = _create_cube(3, 5, 7, 9)
        assert cube_shape(a) == (3, 5, 7, 9)
        assert cube_shape([[], [], []]) == (3, 0)

        with pytest.raises(ValueError):
            cube_shape([[1, 2], 3])

    def test_dimension_switch(self):
        a = _create_cube(3, 5, 7, 9)
        assert cube_shape(dimension_switch(a, (3, 0, 2, 1))) == (9, 3, 7, 5)

        with pytest.raises(ValueError):
            cube_shape(dimension_switch(a, (3, 0, 2, 4)))
        with pytest.raises(ValueError):
            cube_shape(dimension_switch(a, (3, 0, 2,)))

    def test_swap_2d(self):
        assert swap_2d([
            [9, 6, 4, 11, 5, -2, 1],
            [0, 0, 11, 5, 8, -4, 9],
            [0, 2, 13, 7, 0, 13, 0]
        ]) == [
                   [9, 0, 0],
                   [6, 0, 2],
                   [4, 11, 13],
                   [11, 5, 7],
                   [5, 8, 0],
                   [-2, -4, 13],
                   [1, 9, 0]
               ]
