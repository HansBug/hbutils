from itertools import tee, chain, islice
from typing import Iterator, Iterable, Tuple, TypeVar

__all__ = [
    'nested_for', 'progressive_for',
]

_ItemType = TypeVar('_ItemType')


def nested_for(*iters: Iterable[_ItemType]) -> Iterator[Tuple[_ItemType, ...]]:
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


def _yield_progressive_for(iterable: Iterable[_ItemType], n: int, offset: int) -> Iterator[Tuple[_ItemType, ...]]:
    def _recursion(deep, iters, selections: list):
        if deep >= n:
            yield tuple(selections)
        else:
            iters[0], new_iter = tee(iters[0])
            if deep > 0:
                actual_iter = islice(chain(selections[-1:], new_iter), offset, None)
            else:
                actual_iter = new_iter

            while True:
                try:
                    item = next(actual_iter)
                except (StopIteration, StopAsyncIteration):
                    break

                selections.append(item)
                iter_proxy = [actual_iter]
                yield from _recursion(deep + 1, iter_proxy, selections)
                (actual_iter,) = iter_proxy
                selections.pop()

    yield from _recursion(0, [iterable], [])


def progressive_for(iterable: Iterable[_ItemType], n: int, offset: int = 1) -> Iterator[Tuple[_ItemType, ...]]:
    """
    Progressive for based on one given ``iterable``.

    :param iterable: Iterable object for this loop.
    :param n: Depth of this loop.
    :param offset: Offset of this loop, default is ``1`` which means the first value \
        in the next level will be the one after the above level.
    :returns: Progressive for loop iteration.

    Examples::
        >>> from hbutils.reflection import progressive_for
        >>> for a, b in progressive_for(range(4), 2):
        ...     print(a, b)
        0 1
        0 2
        0 3
        1 2
        1 3
        2 3
        >>> for a, b in progressive_for(range(4), 2, 0):
        ...     print(a, b)
        0 0
        0 1
        0 2
        0 3
        1 1
        1 2
        1 3
        2 2
        2 3
        3 3
        >>> for a, b, c in progressive_for(range(5), 3):
        ...     print(a, b, c)
        0 1 2
        0 1 3
        0 1 4
        0 2 3
        0 2 4
        0 3 4
        1 2 3
        1 2 4
        1 3 4
        2 3 4
        >>> for a, b, c in progressive_for(range(5), 3, 2):
        ...     print(a, b, c)
        0 2 4
    """
    if offset < 0:
        raise ValueError(f'Offset for progressive_for should not be lower than 0, but {repr(offset)} found.')

    return _yield_progressive_for(iterable, n, offset)
