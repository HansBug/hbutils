"""
Overview:
    Implement of topological sorting algorithm.

    Wikipedia: `Topological sorting <https://en.wikipedia.org/wiki/Topological_sorting>`_.
"""
from heapq import heappush, heappop
from queue import Queue
from typing import TypeVar, Collection, Tuple, List, Iterable, Hashable, Callable, Set

__all__ = ['topoids', 'topo']


def topoids(n: int, edges: Collection[Tuple[int, int]], sort: bool = False) -> List[int]:
    """
    Overview:
        Topological sort with nodes count and edges.

    Arguments:
        - n (:obj:`int`): Count of nodes.
        - edges (:obj:`Collection[Tuple[int, int]]`): Collection of edges, \
            in each tuple (x, y), means x should be earlier appeared than y in the final sequence.
        - sort (:obj:`bool`): Keep the output list in order. When open, the time complexity will \
            increase an extra :math:`O\\left(\\log{N}\\right)` because of the maintenance of heap. \
            Default is ``False``, which means no not keep the strict order.

    Returns:
        - sequence (:obj:`List[int]`): Sorted sequence.

    Example:
        >>> topoids(3, [])
        [0, 1, 2]
        >>> topoids(3, [(0, 1), (2, 1)])
        [0, 2, 1]
        >>> topoids(3, [(0, 1), (2, 1), (1, 0)])
        ArithmeticError: ('Invalid topological graph, for some node ids not accessible - (0, 1).', (0, 1))

        >>> topoids(4, [(0, 2), (0, 1), (2, 3), (1, 3)])
        [0, 1, 2, 3]  # [0, 2, 1, 3] is also possible
        >>> topoids(4, [(0, 2), (0, 1), (2, 3), (1, 3)], sort=True)
        [0, 1, 2, 3]  # only [0, 1, 2, 3] is possible
    """
    if sort:
        queue_init = lambda: []
        queue_push = heappush
        queue_pop = heappop
        queue_empty = lambda q: not q
    else:
        queue_init = lambda: Queue()
        queue_push = lambda q, x: q.put(x)
        queue_pop = lambda q: q.get()
        queue_empty = lambda q: q.empty()

    if n == 0:
        return []

    in_degree: List[int] = [0] * n
    goings: List[Set[int]] = [set() for _ in range(n)]
    for arrow_tail, arrow_head, in list(set(edges)):
        assert isinstance(arrow_tail, int) and 0 <= arrow_tail < n, \
            f'Tail should be in [0, {n}) but {arrow_tail} found.'
        assert isinstance(arrow_head, int) and 0 <= arrow_head < n, \
            f'Head should be in [0, {n}) but {arrow_head} found.'
        in_degree[arrow_head] += 1
        goings[arrow_tail].add(arrow_head)

    queue = queue_init()
    visited = []
    for i in range(n):
        if in_degree[i] == 0:
            queue_push(queue, i)

    while not queue_empty(queue):
        arrow_tail = queue_pop(queue)
        visited.append(arrow_tail)
        for arrow_head in goings[arrow_tail]:
            assert in_degree[arrow_head] > 0
            in_degree[arrow_head] -= 1
            if in_degree[arrow_head] == 0:
                queue_push(queue, arrow_head)

    if len(visited) < n:
        missing = tuple(sorted(set(range(n)) - set(visited)))
        raise ArithmeticError(f'Invalid topological graph, '
                              f'for some node ids not accessible - {repr(missing)}.', missing)

    return visited


_ElementType = TypeVar('_ElementType')
_IdType = TypeVar('_IdType', bound=Hashable)


# noinspection PyUnresolvedReferences
def topo(items: Iterable[_ElementType],
         edges: Collection[Tuple[_ElementType, _ElementType]],
         identifier: Callable[[_ElementType], _IdType] = None,
         sort: bool = False) -> List[_ElementType]:
    """
    Overview:
        Topological sort with objects and their edges.

    Arguments:
        - items (:obj:`Iterable[_ElementType]`): List of the items.
        - edges (:obj:`Collection[Tuple[_ElementType, _ElementType]]`): Collection of edges, \
            in each tuple (x, y), means x should be earlier appeared than y in the final sequence.
        - identifier (:obj:`Callable[[_ElementType], _IdType]`): Identifier function for the items, \
            need to make sure the output id value is hashable. Default is ``None``, which means \
            use the id value of the objects.
        - sort (:obj:`bool`): Keep the output list in order. When open, the time complexity will \
            increase an extra :math:`O\\left(\\log{N}\\right)` because of the maintenance of heap. \
            Default is ``False``, which means no not keep the strict order.

    Returns:
        - sequence (:obj:`List[_ElementType]`): Sorted sequence.

    Examples::

        >>> n1 = _Container(1)  # _Container is a hashable wrapper class
        >>> n2 = _Container('sdfklj')
        >>> n3 = _Container((2, 3))
        >>> n4 = _Container((3, 'sdj'))
        >>> n5 = _Container(1)
        >>> topo([n1, n2, n3], [], sort=True)
        [n1, n2, n3]
        >>> topo([n1, n2, n5], [(n1, n2), (n5, n2)], sort=True)
        [n1, n5, n2]
        >>> topo([n1, n2, n5], [(n1, n2), (n5, n2)], identifier=lambda x: x.v, sort=True)
        [n1, n2]
        >>> topo([n1, n2, n3, n4], [(n1, n3), (n3, n1), (n2, n3), (n4, n1)])
        ArithmeticError: ('Invalid topological graph, for some items not accessible - (n1, n3).', (n1, n3))
    """
    identifier = identifier or id
    items = list(items)
    id_map, item_map, n = {}, [], 0
    for index, item in enumerate(items):
        idf = identifier(item)
        if idf not in id_map.keys():
            id_map[idf] = n
            item_map.append(item)
            n += 1

    def item_to_id(it):
        return id_map[identifier(it)]

    edges = [
        (item_to_id(tail), item_to_id(head))
        for tail, head in edges
    ]

    try:
        visited_ids = topoids(n, edges, sort=sort)
    except ArithmeticError as err:
        _, missing_ids = err.args
        missing_items = tuple([item_map[i] for i in sorted(missing_ids)])
        raise ArithmeticError(f'Invalid topological graph, '
                              f'for some items not accessible - {repr(missing_items)}.', missing_items)
    else:
        return [item_map[i] for i in visited_ids]
