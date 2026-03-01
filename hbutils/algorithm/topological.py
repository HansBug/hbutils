"""
Topological sorting utilities for integer identifiers and arbitrary objects.

This module implements Kahn's algorithm for topological sorting and provides two
public helper functions:

* :func:`topoids` - Topological sorting for graphs with integer node identifiers.
* :func:`topo` - Topological sorting for graphs composed of arbitrary Python objects.

The implementation supports deterministic output ordering when ``sort=True`` by
using a heap-based queue; otherwise a FIFO queue is used and the order may vary
due to set iteration in adjacency storage.

.. note::
   Duplicate edges are removed before processing. Nodes or items are considered
   unique by their integer ID (for :func:`topoids`) or by their identifier
   function (for :func:`topo`).

Example::

    >>> # Integer-based nodes
    >>> topoids(3, [(0, 1), (2, 1)])
    [0, 2, 1]

    >>> # Object-based nodes with explicit identifiers
    >>> items = ["a", "b", "c"]
    >>> edges = [("a", "c"), ("b", "c")]
    >>> topo(items, edges, identifier=str, sort=True)
    ['a', 'b', 'c']

"""

from heapq import heappush, heappop
from queue import Queue
from typing import (
    TypeVar,
    Collection,
    Tuple,
    List,
    Iterable,
    Hashable,
    Callable,
    Set,
    Optional,
    Dict,
)

__all__ = ['topoids', 'topo']


def topoids(n: int, edges: Collection[Tuple[int, int]], sort: bool = False) -> List[int]:
    """
    Perform a topological sort on integer-identified nodes.

    This function performs a topological sort on a directed acyclic graph (DAG)
    represented by integer node IDs and edges. It uses Kahn's algorithm for
    topological sorting. When ``sort=True``, a heap is used to always pick the
    smallest available node ID, yielding deterministic ordering; otherwise a
    FIFO queue is used and order may depend on adjacency iteration.

    :param n: Count of nodes in the graph (nodes are numbered from ``0`` to ``n - 1``).
    :type n: int
    :param edges: Collection of directed edges, where each tuple ``(x, y)`` means
        node ``x`` must appear before node ``y`` in the final sequence.
    :type edges: Collection[Tuple[int, int]]
    :param sort: Whether to enforce sorted output order by smallest available ID.
        When ``True``, the time complexity increases by an extra
        :math:`O\\left(\\log{N}\\right)` due to heap maintenance. Defaults to ``False``.
    :type sort: bool

    :return: Sorted sequence of node IDs in topological order.
    :rtype: List[int]

    :raises ArithmeticError: If the graph contains a cycle or not all nodes are reachable.
    :raises AssertionError: If edge endpoints are not valid node IDs (not in range ``[0, n)``).

    Example::

        >>> topoids(3, [])
        [0, 1, 2]
        >>> topoids(3, [(0, 1), (2, 1)])
        [0, 2, 1]
        >>> topoids(4, [(0, 2), (0, 1), (2, 3), (1, 3)])
        [0, 1, 2, 3]
        >>> topoids(4, [(0, 2), (0, 1), (2, 3), (1, 3)], sort=True)
        [0, 1, 2, 3]

    .. warning::
       The output order is not deterministic when ``sort=False`` due to unordered
       set iteration in adjacency lists.

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
         identifier: Optional[Callable[[_ElementType], _IdType]] = None,
         sort: bool = False) -> List[_ElementType]:
    """
    Perform a topological sort on arbitrary objects.

    This function performs topological sorting on arbitrary objects by mapping
    each item to an integer ID and delegating sorting to :func:`topoids`. Items
    with the same identifier are treated as a single node; only the first
    occurrence is kept in the output mapping.

    :param items: Iterable of items to be sorted.
    :type items: Iterable[_ElementType]
    :param edges: Collection of directed edges, where each tuple ``(x, y)`` means
        item ``x`` must appear before item ``y`` in the final sequence.
    :type edges: Collection[Tuple[_ElementType, _ElementType]]
    :param identifier: Identifier function for the items. It must return a
        hashable value that uniquely identifies each item. Defaults to ``None``,
        which uses Python's built-in :func:`id` function (object identity).
    :type identifier: Callable[[_ElementType], _IdType], optional
    :param sort: Whether to enforce sorted output order by the integer IDs that
        are assigned based on first appearance. Defaults to ``False``.
    :type sort: bool

    :return: Sorted sequence of unique items in topological order.
    :rtype: List[_ElementType]

    :raises ArithmeticError: If the graph contains a cycle or not all nodes are reachable.
    :raises KeyError: If an edge references an item whose identifier is not present in
        the ``items`` iterable.

    Example::

        >>> items = ["a", "b", "c"]
        >>> edges = [("a", "c"), ("b", "c")]
        >>> topo(items, edges, identifier=str, sort=True)
        ['a', 'b', 'c']
        >>> topo(items, [("a", "b"), ("b", "a")], identifier=str)
        Traceback (most recent call last):
            ...
        ArithmeticError: ('Invalid topological graph, for some items not accessible - (\\'a\\', \\'b\\').', ('a', 'b'))

    .. note::
       Duplicate items are removed based on their identifiers; only the first
       occurrence is retained in the output.

    """
    identifier = identifier or id
    items = list(items)
    id_map: Dict[_IdType, int] = {}
    item_map: List[_ElementType] = []
    n = 0
    for index, item in enumerate(items):
        idf = identifier(item)
        if idf not in id_map.keys():
            id_map[idf] = n
            item_map.append(item)
            n += 1

    def item_to_id(it: _ElementType) -> int:
        """
        Convert an item to its corresponding integer ID.

        :param it: The item to convert.
        :type it: _ElementType
        :return: The integer ID corresponding to the item.
        :rtype: int
        :raises KeyError: If the item's identifier does not exist in the mapping.

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
