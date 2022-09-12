import random
from typing import Iterator, Mapping, Optional, List, Tuple, Union

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
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def _cmpkey(self):
        return self.__name, self.__value


@hasheq()
@visual()
@accessor(readonly=True)
@asitems(['items'])
class _AETGValuePair(IComparable):
    def __init__(self, *pairs):
        self.__items = tuple(sorted(pairs, key=lambda x: (x.name, x.value)))

    def _cmpkey(self):
        return self.__items


def _create_init_pairs(names: List[str]) -> List[Tuple[str, ...]]:
    return list(progressive_for(names, min(2, len(names))))


def _process_pairs(pairs: List[Tuple[str, ...]], names: List[str]) -> List[Tuple[str, ...]]:
    _name_set = set(names)
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


def _to_random(rnd: Optional[Union[random.Random, int]] = None):
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
    Full AETG model, test cases will be generated to make sure the required pairs will be all tested.
    """

    def __init__(self, values, names: Optional[List[str]] = None,
                 pairs: Optional[List[Tuple[str, ...]]] = None,
                 rnd: Optional[Union[random.Random, int]] = None):
        """
        Constructor of the :class:`hbutils.testing.AETGGenerator` class.

        :param values: Selection values, such as ``{'a': [2, 3], 'b': ['b', 'c']}``.
        :param names: Names of the given generator, default is ``None`` which means use the sorted \
            key set of the values.
        :param pairs: Pairs required to be all tested, default is ``None`` which means all the \
            binary pairs will be included.
        :param rnd: Random object or int-formatted random seed, \
            default is ``None`` which means the default random object will be used.
        """
        BaseGenerator.__init__(self, values, names)
        if pairs is None:
            pairs = _create_init_pairs(self.names)
        self.__pairs = _process_pairs(pairs, self.names)
        self.__rnd = _to_random(rnd)

        self.__node_cnt = None
        self.__non_exist_pairs = None

    @property
    def pairs(self) -> List[Tuple[str, ...]]:
        """
        Pairs required to be all tested.
        """
        return self.__pairs

    def __get_init_info(self) -> Tuple[dict, list, set]:
        if self.__node_cnt is None:
            node_cnt = {}
            non_exist_pairs = set()
            for one_pair in self.__pairs:
                for value_items in nested_for(*[self.values[name] for name in one_pair]):
                    pair_items = []
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

            tnames = []
            seqs = []
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
