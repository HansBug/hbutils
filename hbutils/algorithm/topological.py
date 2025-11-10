"""
Overview:
    Implement of topological sorting algorithm.

    This module provides two main functions for performing topological sorting:
    - `topoids`: Performs topological sort on nodes represented by integers
    - `topo`: Performs topological sort on arbitrary objects with custom identifiers

    Wikipedia: `Topological sorting <https://en.wikipedia.org/wiki/Topological_sorting>`_.
"""
from heapq import heappush, heappop
from queue import Queue
from typing import TypeVar, Collection, Tuple, List, Iterable, Hashable, Callable, Set

__all__ = ['topoids', 'topo']


def topoids(n: int, edges: Collection[Tuple[int, int]], sort: bool = False) -> List[int]:
    """
    Topological sort with nodes count and edges.

    This function performs a topological sort on a directed acyclic graph (DAG) represented
    by integer node IDs and edges. It uses Kahn's algorithm for topological sorting.

    :param n: Count of nodes in the graph (nodes are numbered from 0 to n-1).
    :type n: int
    :param edges: Collection of directed edges, where each tuple (x, y) means node x 
        should appear earlier than node y in the final sequence.
    :type edges: Collection[Tuple[int, int]]
    :param sort: Keep the output list in order. When True, the time complexity will 
        increase by an extra :math:`O\\left(\\log{N}\\right)` due to heap maintenance. 
        Default is ``False``, which means no strict order is maintained.
    :type sort: bool

    :return: Sorted sequence of node IDs in topological order.
    :rtype: List[int]
    
    :raises ArithmeticError: If the graph contains a cycle or invalid node references, 
        making topological sorting impossible.
    :raises AssertionError: If edge endpoints are not valid node IDs (not in range [0, n)).

    Examples::

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


def topo(items: Iterable[_ElementType],
         edges: Collection[Tuple[_ElementType, _ElementType]],
         identifier: Callable[[_ElementType], _IdType] = None,
         sort: bool = False) -> List[_ElementType]:
    """
    Topological sort with objects and their edges.

    This function performs topological sorting on arbitrary objects by converting them
    to integer IDs internally and then using the `topoids` function. It allows custom
    identifier functions to determine object uniqueness.

    :param items: Iterable of items to be sorted.
    :type items: Iterable[_ElementType]
    :param edges: Collection of directed edges, where each tuple (x, y) means item x 
        should appear earlier than item y in the final sequence.
    :type edges: Collection[Tuple[_ElementType, _ElementType]]
    :param identifier: Identifier function for the items. Must return a hashable value 
        that uniquely identifies each item. Default is ``None``, which uses Python's 
        built-in ``id()`` function (object identity).
    :type identifier: Callable[[_ElementType], _IdType], optional
    :param sort: Keep the output list in order. When True, the time complexity will 
        increase by an extra :math:`O\\left(\\log{N}\\right)` due to heap maintenance. 
        Default is ``False``, which means no strict order is maintained.
    :type sort: bool

    :return: Sorted sequence of items in topological order.
    :rtype: List[_ElementType]
    
    :raises ArithmeticError: If the graph contains a cycle, making topological sorting impossible.

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
        """
        Convert an item to its corresponding integer ID.

        :param it: The item to convert.
        :type it: _ElementType

        :return: The integer ID corresponding to the item.
        :rtype: int
        """
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
