from itertools import tee
from typing import Iterator, Iterable

__all__ = [
    'nested_for',
]


def nested_for(*iters: Iterable) -> Iterator:
    """
    Nested for based on several iterators.

    :param iters: Iterators to build this nested for loop.
    :return: Nested for loop iteration.

    Examples::
        >>> from hbutils.reflection import nested_for
        >>> for a, r, b in nested_for(
        ...         range(1, 3),
        ...         ['a', 'b'],
        ...         map(lambda x: x ** 2, range(1, 4))
        ... ):
        >>>     print(a, r, b)
        1 a 1
        1 a 4
        1 a 9
        1 b 1
        1 b 4
        1 b 9
        2 a 1
        2 a 4
        2 a 9
        2 b 1
        2 b 4
        2 b 9
    """
    iterators = list(iters)
    n = len(iterators)

    def _recursion(deep, selections: list):
        if deep >= n:
            yield tuple(selections)
        else:
            iterators[deep], new_copy = tee(iterators[deep])
            for item in new_copy:
                selections.append(item)
                yield from _recursion(deep + 1, selections)
                selections.pop()

    yield from _recursion(0, [])
