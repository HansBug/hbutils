from functools import wraps

import pytest

from hbutils.design import decolize
from hbutils.random import shuffle, multiple_choice


@decolize
def repeat(func, *, times=1000):
    @wraps(func)
    def _new_func(*args, **kwargs):
        return tuple([func(*args, **kwargs) for _ in range(times)])

    return _new_func


@pytest.mark.unittest
class TestRandomSequence:
    @repeat
    def test_shuffle(self):
        assert shuffle([]) == []
        assert shuffle(()) == ()
        assert shuffle((1, 2)) in {(1, 2), (2, 1)}

        r1 = shuffle([1, 2])
        assert (r1 == [1, 2]) or (r1 == [2, 1])

        r2 = shuffle([2, 3, 5])
        assert (r2 == [2, 3, 5]) or (r2 == [2, 5, 3]) or \
               (r2 == [3, 2, 5]) or (r2 == [3, 5, 2]) or \
               (r2 == [5, 2, 3]) or (r2 == [5, 3, 2])

    @repeat
    def test_multiple_choice(self):
        r1 = multiple_choice([2, 3, 5, 7], 2)
        assert (r1 == [2, 3]) or (r1 == [2, 5]) or (r1 == [2, 7]) or \
               (r1 == [3, 2]) or (r1 == [3, 5]) or (r1 == [3, 7]) or \
               (r1 == [5, 2]) or (r1 == [5, 3]) or (r1 == [5, 7]) or \
               (r1 == [7, 2]) or (r1 == [7, 3]) or (r1 == [7, 5])

        r2 = multiple_choice([2, 3, 5, 7], 2, put_back=True)
        assert (r2 == [2, 2]) or (r2 == [2, 3]) or (r2 == [2, 5]) or (r2 == [2, 7]) or \
               (r2 == [3, 2]) or (r2 == [3, 3]) or (r2 == [3, 5]) or (r2 == [3, 7]) or \
               (r2 == [5, 2]) or (r2 == [5, 3]) or (r2 == [5, 5]) or (r2 == [5, 7]) or \
               (r2 == [7, 2]) or (r2 == [7, 3]) or (r2 == [7, 5]) or (r2 == [7, 7])

        with pytest.raises(ValueError):
            _ = multiple_choice([2, 3], 3)

        r3 = multiple_choice([2, 3], 3, put_back=True)
        assert (r3 == [2, 2, 2]) or (r3 == [2, 2, 3]) or \
               (r3 == [2, 3, 2]) or (r3 == [2, 3, 3]) or \
               (r3 == [3, 2, 2]) or (r3 == [3, 2, 3]) or \
               (r3 == [3, 3, 2]) or (r3 == [3, 3, 3])
