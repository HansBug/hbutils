import pytest

from hbutils.testing import AETGGenerator


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestTestingGeneratorAETG:
    def test_accessors(self):
        m = AETGGenerator({'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]})
        assert m.names == ['a', 'b', 'r']
        assert m.values == {'a': (1, 2, 3), 'b': ('a', 'b'), 'r': (3, 4, 5)}

    def test_tuple_cases(self):
        ds = {'a': [1, 2, 3], 'b': [4, 5], 'r': [6, 7, 8]}
        m = AETGGenerator(ds)

        n = 3
        ids = sorted(ds.items())
        pairset = set()
        for i in range(0, n):
            _, ivalues = ids[i]
            for j in range(i + 1, n):
                _, jvalues = ids[j]
                for ivalue in ivalues:
                    for jvalue in jvalues:
                        pairset.add((ivalue, jvalue))

        assert len(pairset) == 21
        cnt = 0
        for a, b, r in m.tuple_cases():
            if (a, b) in pairset:
                pairset.remove((a, b))
            if (a, r) in pairset:
                pairset.remove((a, r))
            if (b, r) in pairset:
                pairset.remove((b, r))
            cnt += 1

        assert len(pairset) == 0
        assert cnt <= 12
