import random

import pytest

from hbutils.reflection import nested_for, progressive_for
from hbutils.testing import AETGGenerator


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestTestingGeneratorAETG:
    def test_accessors(self):
        m = AETGGenerator({'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]})
        assert m.names == ['a', 'b', 'r']
        assert m.values == {'a': (1, 2, 3), 'b': ('a', 'b'), 'r': (3, 4, 5)}
        assert m.pairs == [('a', 'b'), ('a', 'r'), ('b', 'r')]

        m1 = AETGGenerator({
            'a': range(1, 3),
            'b': range(3, 5),
            'c': range(5, 7),
            'd': range(7, 9),
            'e': range(9, 11),
        }, pairs=[('a', 'b', 'e'), ('b', 'c'), ('d',), ('a', 'e'), ('b',)])
        assert m1.names == ['a', 'b', 'c', 'd', 'e']
        assert m1.values == {
            'a': (1, 2),
            'b': (3, 4),
            'c': (5, 6),
            'd': (7, 8),
            'e': (9, 10),
        }
        assert m1.pairs == [('d',), ('b', 'c'), ('a', 'b', 'e')]

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_tuple_cases(self):
        ds = {
            'a': range(1, 3),
            'b': range(3, 5),
            'c': range(5, 7),
            'd': range(7, 9),
            'e': range(9, 11),
        }
        m = AETGGenerator(ds)

        results = {}
        for i in range(50):
            pairset = set()
            for iname, jname in progressive_for(m.names, 2):
                for ivalue, jvalue in nested_for(ds[iname], ds[jname]):
                    pairset.add((ivalue, jvalue))

            cnt = 0
            for vs in m.tuple_cases():
                cnt += 1
                for ii, jj in progressive_for(range(5), 2):
                    pair = (vs[ii], vs[jj])
                    if pair in pairset:
                        pairset.remove(pair)

            assert not pairset
            results[cnt] = results.get(cnt, 0) + 1

        assert sum([iv for ik, iv in results.items() if ik >= 9]) <= 3

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_tuple_cases_simple_pairs(self):
        ds = {
            'a': range(1, 3),
            'b': range(3, 5),
            'c': range(5, 7),
            'd': range(7, 9),
            'e': range(9, 11),
        }
        m = AETGGenerator(ds, pairs=[('a', 'c',), ('b', 'd'), ('e',)])

        results = {}
        for i in range(50):
            pairset = set()
            for a, c in nested_for(ds['a'], ds['c']):
                pairset.add((a, c))
            for b, d in nested_for(ds['b'], ds['d']):
                pairset.add((b, d))
            for e in ds['e']:
                pairset.add((e,))

            cnt = 0
            for a, b, c, d, e in m.tuple_cases():
                cnt += 1
                if (a, c) in pairset:
                    pairset.remove((a, c))
                if (b, d) in pairset:
                    pairset.remove((b, d))
                if (e,) in pairset:
                    pairset.remove((e,))

            assert not pairset
            results[cnt] = results.get(cnt, 0) + 1

        assert sum([iv for ik, iv in results.items() if ik >= 6]) <= 4

    def test_full_pair(self):
        m = AETGGenerator(
            {
                'a': (11, 12, 13, 14, 15),
                'b': (21, 22, 23, 24, 25),
                'c': (31, 32, 33, 34, 35),
                'd': (41, 42, 43, 44, 45),
                'e': (51, 52, 53, 54, 55),
            },
            pairs=[('a', 'b', 'c', 'd', 'e')]
        )
        cases = list(m.tuple_cases())
        assert len(cases) == 5 ** 5
        assert len(set(cases)) == 5 ** 5

    def test_actual_pair(self):
        m = AETGGenerator(
            {
                'a': (11, 12, 13, 14, 15),
                'b': (21, 22, 23, 24, 25),
                'c': (31, 32, 33, 34, 35),
                'd': (41, 42, 43, 44, 45),
                'e': (51, 52, 53, 54, 55),
            },
            pairs=[('a', 'c'), ('b', 'd'), ('e',)]
        )

        cnt = {}
        for i in range(50):
            cases = list(m.tuple_cases())
            assert len(cases) == len(set(cases))

            n = len(cases)
            cnt[n] = cnt.get(n, 0) + 1

    def test_fixed_seed(self):
        for i in range(10):
            m = AETGGenerator(
                {
                    'a': (11, 12, 13, 14, 15),
                    'b': (21, 22, 23, 24, 25),
                    'c': (31, 32, 33, 34, 35),
                    'd': (41, 42, 43, 44, 45),
                    'e': (51, 52, 53, 54, 55),
                },
                pairs=[('a', 'c'), ('b', 'd'), ('e',)],
                rnd=0,
            )

            cases = list(m.tuple_cases())
            assert cases == [(13, 25, 34, 42, 55), (14, 22, 32, 43, 54), (11, 23, 33, 45, 53), (15, 24, 35, 41, 52),
                             (12, 21, 31, 44, 51), (15, 25, 32, 45, 52), (13, 25, 35, 44, 52), (14, 25, 34, 43, 55),
                             (12, 25, 33, 41, 55), (11, 24, 31, 45, 51), (11, 24, 34, 44, 55), (14, 24, 31, 43, 51),
                             (13, 24, 32, 42, 53), (12, 23, 33, 44, 52), (15, 23, 33, 43, 53), (12, 23, 35, 42, 53),
                             (12, 23, 32, 41, 52), (14, 22, 33, 45, 53), (15, 22, 31, 44, 52), (11, 22, 35, 42, 53),
                             (13, 22, 34, 41, 53), (12, 21, 34, 45, 51), (13, 21, 31, 43, 52), (11, 21, 32, 42, 53),
                             (15, 21, 34, 41, 55), (14, 23, 35, 42, 52), (13, 23, 33, 43, 55)]

    def test_fixed_random_seed(self):
        for i in range(10):
            m = AETGGenerator(
                {
                    'a': (11, 12, 13, 14, 15),
                    'b': (21, 22, 23, 24, 25),
                    'c': (31, 32, 33, 34, 35),
                    'd': (41, 42, 43, 44, 45),
                    'e': (51, 52, 53, 54, 55),
                },
                pairs=[('a', 'c'), ('b', 'd'), ('e',)],
                rnd=random.Random(0),
            )

            cases = list(m.tuple_cases())
            assert cases == [(13, 25, 34, 42, 55), (14, 22, 32, 43, 54), (11, 23, 33, 45, 53), (15, 24, 35, 41, 52),
                             (12, 21, 31, 44, 51), (15, 25, 32, 45, 52), (13, 25, 35, 44, 52), (14, 25, 34, 43, 55),
                             (12, 25, 33, 41, 55), (11, 24, 31, 45, 51), (11, 24, 34, 44, 55), (14, 24, 31, 43, 51),
                             (13, 24, 32, 42, 53), (12, 23, 33, 44, 52), (15, 23, 33, 43, 53), (12, 23, 35, 42, 53),
                             (12, 23, 32, 41, 52), (14, 22, 33, 45, 53), (15, 22, 31, 44, 52), (11, 22, 35, 42, 53),
                             (13, 22, 34, 41, 53), (12, 21, 34, 45, 51), (13, 21, 31, 43, 52), (11, 21, 32, 42, 53),
                             (15, 21, 34, 41, 55), (14, 23, 35, 42, 52), (13, 23, 33, 43, 55)]

    def test_fixed_invalid(self):
        with pytest.raises(TypeError):
            AETGGenerator(
                {
                    'a': (11, 12, 13, 14, 15),
                    'b': (21, 22, 23, 24, 25),
                    'c': (31, 32, 33, 34, 35),
                    'd': (41, 42, 43, 44, 45),
                    'e': (51, 52, 53, 54, 55),
                },
                pairs=[('a', 'c'), ('b', 'd'), ('e',)],
                rnd='random.Random(0)',
            )
