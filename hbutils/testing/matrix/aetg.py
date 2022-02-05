import random
from typing import Iterator, Mapping

from .base import BaseMatrix
from .full import FullMatrix
from ...model import visual, hasheq, accessor, asitems

__all__ = [
    'AETGMatrix',
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

    def another(self, pair):
        if pair == self.__first:
            return self.__second
        elif pair == self.__second:
            return self.__first
        else:
            raise ValueError(f'Key-value pair not found in this AETG pair - {repr(pair)}.')


class AETGMatrix(BaseMatrix):
    def __init__(self, values: Mapping[str, object]):
        super().__init__(values)

    def cases(self) -> Iterator[Mapping[str, object]]:
        fm = FullMatrix(self.values, self.include, self.exclude)
        n = len(self.names)

        node_cnt = {}
        pair_index = {}
        non_exist_pairs = set()
        for p in fm.cases():
            all_items = list(p.items())
            for i in range(0, n):
                for j in range(i + 1, n):
                    pair = _AETGPair(*all_items[i], *all_items[j])
                    if pair not in non_exist_pairs:
                        non_exist_pairs.add(pair)
                        node_cnt[pair.first] = node_cnt.get(pair.first, 0) + 1
                        node_cnt[pair.second] = node_cnt.get(pair.second, 0) + 1

                    if pair.first not in pair_index:
                        pair_index[pair.first] = set()
                    pair_index[pair.first].add(pair.second)

                    if pair.second not in pair_index:
                        pair_index[pair.second] = set()
                    pair_index[pair.second].add(pair.first)

        repo = set()
        while non_exist_pairs:
            fnode, fcnt = None, None
            sss = list(node_cnt.items())
            # random.shuffle(sss)
            for pair, cnt in sss:
                if fcnt is None or cnt > fcnt:
                    fnode = pair
                    fcnt = cnt

            seqs = [fnode]
            for i in range(1, n):
                pairset = None
                for j in range(0, i):
                    curset = pair_index[seqs[j]]
                    if pairset is None:
                        pairset = set(curset)
                    else:
                        pairset &= curset

                assert pairset

                sss = list(pairset)
                # random.shuffle(sss)
                curpair, curcnt = None, None
                for pair in sss:
                    cnt = node_cnt[pair]
                    if curcnt is None or cnt > curcnt:
                        curpair = pair
                        curcnt = cnt

                assert curpair is not None
                seqs.append(curpair)

            for i in range(0, n):
                for j in range(i + 1, n):
                    kp = _AETGPair(seqs[i].key, seqs[i].value, seqs[j].key, seqs[j].value)
                    if kp in non_exist_pairs:
                        non_exist_pairs.remove(kp)
                        node_cnt[kp.first] -= 1
                        node_cnt[kp.second] -= 1

            px = {pair.key: pair.value for pair in seqs}
            feat = tuple((name, px[name]) for name in self.names)
            # if feat not in repo:
            if True:
                yield dict(feat)
                repo.add(feat)

        assert not non_exist_pairs

        for f in sorted(repo):
            print(f)
