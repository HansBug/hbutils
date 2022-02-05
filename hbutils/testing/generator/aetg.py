import random
from functools import reduce
from operator import __mul__, __add__
from typing import Iterator, Mapping, Optional, List, Tuple

from hbutils.model import visual, hasheq, accessor, asitems
from .base import BaseGenerator

__all__ = [
    'AETGGenerator',
]


@hasheq()
@visual()
@accessor(readonly=True)
@asitems(['key', 'value'])
class _KeyValuePair:
    def __init__(self, key, value):
        self.__key = key
        self.__value = value


@hasheq()
@visual()
@accessor(readonly=True)
@asitems(['first', 'second'])
class _AETGPair:
    def __init__(self, akey, avalue, bkey, bvalue):
        apair = _KeyValuePair(akey, avalue)
        bpair = _KeyValuePair(bkey, bvalue)

        if (akey, avalue) < (bkey, bvalue):
            self.__first, self.__second = apair, bpair
        else:
            self.__first, self.__second = bpair, apair


class AETGGenerator(BaseGenerator):
    def __init__(self, values, names: Optional[List[str]] = None,
                 pairs: Optional[List[Tuple[str]]] = None):
        BaseGenerator.__init__(self, values, names)
        _name_set = set(self.names)

        if pairs is None:
            self.__pairs = []
            n = len(self.names)
            for i in range(0, n):
                self.__pairs.append((self.names[i],))

            for i in range(0, n):
                for j in range(i + 1, n):
                    self.__pairs.append((self.names[i], self.names[j]))

        else:
            self.__pairs = [tuple(px) for px in (pairs or [])]
            for pair in self.__pairs:
                for p in pair:
                    if p not in _name_set:
                        raise KeyError(f'Invalid key - {repr(p)}.')

    @property
    def pairs(self) -> List[Tuple[str]]:
        return self.__pairs

    def cases(self) -> Iterator[Mapping[str, object]]:
        n = len(self.names)
        lengths = [len(self.values[name]) for name in self.names]
        total_sum = reduce(__add__, lengths, 0)
        total_sqsum = reduce(__add__, map(lambda x: x ** 2, lengths), 0)
        total_mul = reduce(__mul__, lengths, 1)

        node_cnt = {}
        exist_pairs = set()
        total_pairs_cnt = (total_sum ** 2 - total_sqsum) // 2
        for i in range(0, n):
            iname = self.names[i]
            others_mul = total_mul // len(self.values[iname])
            for ivalue in self.values[iname]:
                ipair = _KeyValuePair(iname, ivalue)
                node_cnt[ipair] = others_mul

        repo = set()
        while len(exist_pairs) < total_pairs_cnt:
            fnode, fxk = None, None
            for pair, cnt in node_cnt.items():
                xk = (cnt, random.random())
                if fxk is None or xk > fxk:
                    fnode = pair
                    fxk = xk

            seqs = [fnode]
            other_names = [name for name in self.names if name != fnode.key]
            random.shuffle(other_names)
            tnames = [fnode.key, *other_names]

            for i in range(1, n):
                lastpair = seqs[i - 1]
                iname = tnames[i]
                curpair, curxk = None, None
                for ivalue in self.values[iname]:
                    ipair = _KeyValuePair(iname, ivalue)
                    now_pair = _AETGPair(lastpair.key, lastpair.value, ipair.key, ipair.value)
                    xk = (0 if now_pair in exist_pairs else 1, node_cnt[ipair], random.random())
                    if curxk is None or xk > curxk:
                        curpair = ipair
                        curxk = xk

                seqs.append(curpair)

            for i in range(0, n):
                for j in range(i + 1, n):
                    kp = _AETGPair(seqs[i].key, seqs[i].value, seqs[j].key, seqs[j].value)
                    if kp not in exist_pairs:
                        exist_pairs.add(kp)
                        node_cnt[kp.first] -= 1
                        node_cnt[kp.second] -= 1

            px = {pair.key: pair.value for pair in seqs}
            feat = tuple((name, px[name]) for name in self.names)
            if feat not in repo:
                yield dict(feat)
                repo.add(feat)
