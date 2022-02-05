import random
from typing import Iterator, Mapping, Optional, List, Tuple

from hbutils.model import visual, hasheq, accessor, asitems
from .base import BaseGenerator
from ...reflection import nested_for

__all__ = [
    'AETGGenerator',
]


@hasheq()
@visual()
@accessor(readonly=True)
@asitems(['name', 'value'])
class _NameValueTuple:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value


@hasheq()
@visual()
@accessor(readonly=True)
@asitems(['items'])
class _AETGValuePair:
    def __init__(self, *pairs):
        self.__items = tuple(sorted(pairs, key=lambda x: (x.name, x.value)))


def _generate_pairs(names: List[str]) -> List[Tuple[str, ...]]:
    _pairs = []
    n = len(names)
    for i in range(0, n):
        for j in range(i + 1, n):
            _pairs.append((names[i], names[j]))

    return _pairs


def _process_pairs(pairs: List[Tuple[str, ...]], names: List[str]) -> List[Tuple[str, ...]]:
    _name_set = set(names)
    _name_id_dict = {name: i for i, name in enumerate(names)}

    _init_pairs = []
    for pair in pairs:
        actual_pair_ids = sorted(set(map(lambda x: _name_id_dict[x], pair)))
        actual_pair = tuple(names[i] for i in actual_pair_ids)
        _init_pairs.append(actual_pair)
    _init_pairs = [x[1] for x in sorted((len(v), v) for v in set(_init_pairs))]
    n = len(_init_pairs)

    _final_pairs = []
    for i in range(0, n):
        iset = set(_init_pairs[i])
        ok_flag = True
        for j in range(i + 1, n):
            jset = set(_init_pairs[j])
            if len(iset & jset) == len(iset):
                ok_flag = False
                break

        if ok_flag:
            _final_pairs.append(_init_pairs[i])

    return _final_pairs


class AETGGenerator(BaseGenerator):
    def __init__(self, values, names: Optional[List[str]] = None,
                 pairs: Optional[List[Tuple[str]]] = None):
        BaseGenerator.__init__(self, values, names)
        if pairs is None:
            self.__pairs = _generate_pairs(self.names)
        else:
            self.__pairs = _process_pairs(pairs or [], self.names)

    @property
    def pairs(self) -> List[Tuple[str]]:
        return self.__pairs

    def cases(self) -> Iterator[Mapping[str, object]]:
        n = len(self.names)
        m = len(self.__pairs[-1])

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

        repo = set()
        while non_exist_pairs:
            tnames = list(self.names)
            random.shuffle(tnames)

            seqs = []
            for i in range(0, n):
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
                        if now_pair in non_exist_pairs:
                            non_exists += 1

                    xk = (1 if non_exists else 0, node_cnt[ituple], random.random())
                    if curxk is None or xk > curxk:
                        curpair = ituple
                        curxk = xk

                seqs.append(curpair)

            px = {pair.name: pair.value for pair in seqs}
            for one_pair in self.__pairs:
                new_pair = _AETGValuePair(*(_NameValueTuple(name, px[name]) for name in one_pair))
                if new_pair in non_exist_pairs:
                    non_exist_pairs.remove(new_pair)
                    for np in new_pair.items:
                        node_cnt[np] -= 1

            feat = tuple((name, px[name]) for name in self.names)
            if feat not in repo:
                yield dict(feat)
                repo.add(feat)
