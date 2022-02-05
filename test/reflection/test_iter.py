import pytest

from hbutils.reflection import nested_for


@pytest.mark.unittest
class TestReflectionIter:
    def test_nested_for(self):
        assert list(nested_for(range(1, 5), range(2, 4))) == [
            (1, 2), (1, 3),
            (2, 2), (2, 3),
            (3, 2), (3, 3),
            (4, 2), (4, 3),
        ]

        assert list(nested_for(range(1, 4), ['a', 'b'], map(lambda x: x ** 2, range(1, 4)))) == [
            (1, 'a', 1), (1, 'a', 4), (1, 'a', 9),
            (1, 'b', 1), (1, 'b', 4), (1, 'b', 9),

            (2, 'a', 1), (2, 'a', 4), (2, 'a', 9),
            (2, 'b', 1), (2, 'b', 4), (2, 'b', 9),

            (3, 'a', 1), (3, 'a', 4), (3, 'a', 9),
            (3, 'b', 1), (3, 'b', 4), (3, 'b', 9),
        ]
