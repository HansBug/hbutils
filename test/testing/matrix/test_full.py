import pytest

from hbutils.testing import FullMatrix


@pytest.mark.unittest
class TestTestingMatrixFull:
    def test_accessors(self):
        m = FullMatrix(
            {'a': [1, 2, 3], 'b': ['a', 'b'], 'r': [3, 4, 5]},
            include=[{'a': 4, 'r': 7}],
            exclude=[{'a': 1, 'r': 3}, {'a': 3, 'b': 'b'}, {'a': 4, 'b': 'a', 'r': 7}]
        )
        assert list(m.cases()) == [
            {'a': 1, 'b': 'a', 'r': 4},
            {'a': 1, 'b': 'a', 'r': 5},
            {'a': 1, 'b': 'b', 'r': 4},
            {'a': 1, 'b': 'b', 'r': 5},
            {'a': 2, 'b': 'a', 'r': 3},
            {'a': 2, 'b': 'a', 'r': 4},
            {'a': 2, 'b': 'a', 'r': 5},
            {'a': 2, 'b': 'b', 'r': 3},
            {'a': 2, 'b': 'b', 'r': 4},
            {'a': 2, 'b': 'b', 'r': 5},
            {'a': 3, 'b': 'a', 'r': 3},
            {'a': 3, 'b': 'a', 'r': 4},
            {'a': 3, 'b': 'a', 'r': 5},
            {'a': 4, 'b': 'b', 'r': 7},
        ]
