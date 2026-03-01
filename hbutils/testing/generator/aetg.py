"""
AETG (Automatic Efficient Test Generator) implementation for combinatorial testing.

This module provides a greedy AETG-based generator that constructs test cases to
cover required parameter combinations (pairs or higher-order tuples). The generator
iteratively selects parameter values that maximize coverage of uncovered combinations,
yielding a compact suite of test cases.

The main public component is:

* :class:`AETGGenerator` - Generator that yields test cases covering required pairs

.. note::
   The algorithm includes randomized selection for tie-breaking. For reproducible
   results, provide a deterministic random seed or a :class:`random.Random` instance
   to :class:`AETGGenerator`.

Example::

    >>> from hbutils.testing import AETGGenerator
    >>> generator = AETGGenerator({'a': (1, 2), 'b': (3, 4), 'c': (5, 6)}, rnd=123)
    >>> for case in generator.cases():
    ...     print(case)
    {'a': 1, 'b': 3, 'c': 5}
    {'a': 2, 'b': 4, 'c': 6}
    ...

"""

import random
from typing import Iterator, Mapping, Optional, List, Tuple, Union, Dict, Set

from hbutils.model import visual, hasheq, accessor, asitems, IComparable
from .base import BaseGenerator
from ...reflection import nested_for, progressive_for

__all__ = [
    'AETGGenerator',
]


@hasheq()
@visual()
@accessor(readonly=True)
@asitems(['name', 'value'])
class _NameValueTuple(IComparable):
    """
    Internal class representing a name-value tuple for AETG algorithm.

    This class is used to store and compare parameter name-value pairs
    during test case generation.

    .. note::
        This class is internal and not part of the public API.
    """

    def __init__(self, name: str, value: object) -> None:
        """
        Initialize a name-value tuple.

        :param name: The parameter name.
        :type name: str
        :param value: The parameter value.
        :type value: object
        """
        self.__name = name
        self.__value = value

    def _cmpkey(self) -> Tuple[str, object]:
        """
        Get the comparison key for this tuple.

        :return: A tuple containing name and value for comparison.
        :rtype: tuple
        """
        return self.__name, self.__value


@hasheq()
@visual()
@accessor(readonly=True)
@asitems(['items'])
class _AETGValuePair(IComparable):
    """
    Internal class representing a collection of name-value pairs for AETG algorithm.

    This class is used to represent and compare combinations of parameter values
    that need to be covered in test cases.

    .. note::
        This class is internal and not part of the public API.
    """

    def __init__(self, *pairs: _NameValueTuple) -> None:
        """
        Initialize an AETG value pair.

        :param pairs: Variable number of :class:`_NameValueTuple` objects.
        :type pairs: _NameValueTuple
        """
        self.__items = tuple(sorted(pairs, key=lambda x: (x.name, x.value)))

    def _cmpkey(self) -> Tuple[_NameValueTuple, ...]:
        """
        Get the comparison key for this pair.

        :return: A tuple of items for comparison.
        :rtype: tuple
        """
        return self.__items


def _create_init_pairs(names: List[str]) -> List[Tuple[str, ...]]:
    """
    Create initial pairs for AETG algorithm.

    Generates all progressive combinations of parameter names with a length of
    ``min(2, len(names))``. This means binary pairs for two or more parameters,
    and singletons when only one parameter is present.

    :param names: List of parameter names.
    :type names: List[str]

    :return: List of tuples representing parameter combinations.
    :rtype: List[Tuple[str, ...]]
    """
    return list(progressive_for(names, min(2, len(names))))


def _process_pairs(pairs: List[Tuple[str, ...]], names: List[str]) -> List[Tuple[str, ...]]:
    """
    Process and validate pairs for AETG algorithm.

    This function normalizes pairs based on the order of ``names`` and removes
    redundant combinations where one pair is a subset of another. The resulting
    list is ordered from lower to higher arity.

    :param pairs: List of parameter name tuples to process.
    :type pairs: List[Tuple[str, ...]]
    :param names: List of all valid parameter names.
    :type names: List[str]

    :return: Processed list of parameter combinations.
    :rtype: List[Tuple[str, ...]]
    """
    _name_id_dict = {name: i for i, name in enumerate(names)}

    _init_pairs = []
    for pair in pairs:
        actual_pair_ids = sorted(set(map(lambda x: _name_id_dict[x], pair)))
        actual_pair = tuple(names[i] for i in actual_pair_ids)
        _init_pairs.append(actual_pair)

    _init_pairs = sorted(_init_pairs, key=lambda x: (len(x), x), reverse=True)
    _final_pairs = []
    for pair in _init_pairs:
        sp = set(pair)
        is_included = False
        for exist_pair in _final_pairs:
            sep = set(exist_pair)
            if sp & sep == sp:
                is_included = True
                break

        if not is_included:
            _final_pairs.append(pair)

    return _final_pairs[::-1]


# noinspection PyProtectedMember
_DEFAULT_RANDOM = random._inst


def _to_random(rnd: Optional[Union[random.Random, int]] = None) -> random.Random:
    """
    Convert various random input types to a :class:`random.Random` object.

    :param rnd: Random object, seed integer, or ``None`` for default random.
    :type rnd: Optional[Union[random.Random, int]]

    :return: A :class:`random.Random` object for generating random numbers.
    :rtype: random.Random

    :raises TypeError: If ``rnd`` is not a valid type.
    """
    if isinstance(rnd, random.Random):
        return rnd
    elif isinstance(rnd, int):
        return random.Random(rnd)
    elif rnd is None:
        return _DEFAULT_RANDOM
    else:
        raise TypeError(f'Unknown random type - {repr(rnd)}.')


class AETGGenerator(BaseGenerator):
    """
    AETG generator that ensures all required parameter combinations are covered.

    The AETG (Automatic Efficient Test Generator) algorithm generates test cases
    that cover required parameter combinations. It uses a greedy strategy that
    attempts to maximize coverage of currently uncovered combinations, with a
    randomized tie-breaking mechanism.

    Example::
        >>> from hbutils.testing import AETGGenerator
        >>> gene = AETGGenerator({'a': (1, 2), 'b': (3, 4), 'c': (5, 6)}, rnd=0)
        >>> for case in gene.cases():
        ...     print(case)
        {'a': 1, 'b': 3, 'c': 5}
        {'a': 2, 'b': 4, 'c': 6}
        ...
    """

    def __init__(self, values: Mapping[str, object], names: Optional[List[str]] = None,
                 pairs: Optional[List[Tuple[str, ...]]] = None,
                 rnd: Optional[Union[random.Random, int]] = None) -> None:
        """
        Constructor of the :class:`hbutils.testing.AETGGenerator` class.

        :param values: Selection values, such as ``{'a': [2, 3], 'b': ['b', 'c']}``.
        :type values: Mapping[str, object]
        :param names: Names of the given generator, default is ``None`` which means use the sorted \
            key set of the values.
        :type names: Optional[List[str]]
        :param pairs: Pairs required to be all tested, default is ``None`` which means all the \
            binary pairs will be included.
        :type pairs: Optional[List[Tuple[str, ...]]]
        :param rnd: Random object or int-formatted random seed, \
            default is ``None`` which means the default random object will be used.
        :type rnd: Optional[Union[random.Random, int]]
        """
        BaseGenerator.__init__(self, values, names)
        if pairs is None:
            pairs = _create_init_pairs(self.names)
        self.__pairs = _process_pairs(pairs, self.names)
        self.__rnd = _to_random(rnd)

        self.__node_cnt: Optional[Dict[_NameValueTuple, int]] = None
        self.__non_exist_pairs: Optional[List[_AETGValuePair]] = None

    @property
    def pairs(self) -> List[Tuple[str, ...]]:
        """
        Pairs required to be all tested.

        :return: List of parameter name tuples that must be covered.
        :rtype: List[Tuple[str, ...]]
        """
        return self.__pairs

    def __get_init_info(self) -> Tuple[Dict[_NameValueTuple, int], List[_AETGValuePair], Set[_AETGValuePair]]:
        """
        Get initialization information for the AETG algorithm.

        This method calculates the frequency of each parameter value in uncovered
        pairs and creates the initial set of pairs that need to be covered. The
        results are cached on the generator instance and returned as copies to
        avoid external mutation.

        :return: A tuple containing:

            - dict: Count of occurrences for each name-value tuple
            - list: List of uncovered pairs (sorted)
            - set: Set of uncovered pairs for fast lookup
        :rtype: Tuple[Dict[_NameValueTuple, int], List[_AETGValuePair], Set[_AETGValuePair]]
        """
        if self.__node_cnt is None:
            node_cnt: Dict[_NameValueTuple, int] = {}
            non_exist_pairs: Set[_AETGValuePair] = set()
            for one_pair in self.__pairs:
                for value_items in nested_for(*[self.values[name] for name in one_pair]):
                    pair_items: List[_NameValueTuple] = []
                    for name, value in zip(one_pair, value_items):
                        tp = _NameValueTuple(name, value)
                        pair_items.append(tp)
                        node_cnt[tp] = node_cnt.get(tp, 0) + 1
                    non_exist_pairs.add(_AETGValuePair(*pair_items))

            self.__node_cnt = node_cnt
            self.__non_exist_pairs = sorted(non_exist_pairs)

        return dict(self.__node_cnt), list(self.__non_exist_pairs), set(self.__non_exist_pairs)

    def cases(self) -> Iterator[Mapping[str, object]]:
        """
        Get the cases in this AETG model.

        Generates test cases using the AETG algorithm, ensuring all required parameter
        combinations are covered. The algorithm uses a greedy approach to select values
        that cover the most uncovered pairs. The order of generated cases can vary due
        to random tie-breaking.

        :return: Iterator yielding test case dictionaries.
        :rtype: Iterator[Mapping[str, object]]

        Examples::
            >>> from hbutils.testing import AETGGenerator
            >>> gene = AETGGenerator({'a': (1, 2), 'b': (3, 4), 'c': (5, 6), 'd': (7, 8), 'e': (9, 10)})
            >>> for p in gene.cases():
            ...     print(p)
            {'a': 1, 'b': 3, 'c': 6, 'd': 8, 'e': 10}
            {'a': 2, 'b': 4, 'c': 5, 'd': 7, 'e': 9}
            {'a': 2, 'b': 3, 'c': 6, 'd': 7, 'e': 9}
            {'a': 2, 'b': 4, 'c': 6, 'd': 8, 'e': 10}
            {'a': 1, 'b': 3, 'c': 5, 'd': 7, 'e': 10}
            {'a': 1, 'b': 4, 'c': 5, 'd': 8, 'e': 9}
            >>> gene = AETGGenerator(
            ...     {'a': (1, 2), 'b': (3, 4), 'c': (5, 6), 'd': (7, 8), 'e': (9, 10)},
            ...     pairs=[('a', 'c'), ('b', 'd'), ('e',)]
            ... )
            >>> for p in gene.cases():
            ...     print(p)
            {'a': 2, 'b': 3, 'c': 6, 'd': 8, 'e': 9}
            {'a': 1, 'b': 4, 'c': 5, 'd': 7, 'e': 10}
            {'a': 2, 'b': 4, 'c': 5, 'd': 8, 'e': 9}
            {'a': 1, 'b': 3, 'c': 6, 'd': 7, 'e': 10}
        """
        n = len(self.names)
        m = len(self.__pairs[-1]) if self.__pairs else 0
        node_cnt, non_exist_pairs_list, non_exist_pairs_set = self.__get_init_info()

        while non_exist_pairs_set:
            first_pair = None
            while non_exist_pairs_list:
                _pair = non_exist_pairs_list.pop()
                if _pair in non_exist_pairs_set:
                    non_exist_pairs_list.append(_pair)
                    first_pair = _pair
                    break

            tnames: List[str] = []
            seqs: List[_NameValueTuple] = []
            for pair_item in first_pair.items:
                tnames.append(pair_item.name)
                seqs.append(pair_item)

            _tname_set = set(tnames)
            other_names = [name for name in self.names if name not in _tname_set]
            self.__rnd.shuffle(other_names)
            tnames += other_names

            for i in range(len(seqs), n):
                iname = tnames[i]
                curpair, curxk = None, None
                for ivalue in self.values[iname]:
                    ituple = _NameValueTuple(iname, ivalue)

                    litems = [ituple]
                    non_exists = 0
                    for j in range(0, min(m, i + 1)):
                        if j > 0:
                            litems.append(seqs[i - j])
                        now_pair = _AETGValuePair(*litems)
                        if now_pair in non_exist_pairs_set:
                            non_exists += 1

                    xk = (non_exists, node_cnt.get(ituple, 0), self.__rnd.random())
                    if curxk is None or xk > curxk:
                        curpair = ituple
                        curxk = xk

                seqs.append(curpair)

            px = {pair.name: pair.value for pair in seqs}
            for one_pair in self.__pairs:
                new_pair = _AETGValuePair(*(_NameValueTuple(name, px[name]) for name in one_pair))
                if new_pair in non_exist_pairs_set:
                    non_exist_pairs_set.remove(new_pair)
                    for np in new_pair.items:
                        node_cnt[np] -= 1

            yield {name: px[name] for name in self.names}
