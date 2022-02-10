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

        assert sum([iv for ik, iv in results.items() if ik >= 7]) >= 10
        assert sum([iv for ik, iv in results.items() if ik >= 9]) <= 3

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

        assert cnt[26] + cnt[27] >= 25
