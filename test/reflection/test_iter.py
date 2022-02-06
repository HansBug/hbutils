import pytest

from hbutils.reflection import nested_for, progressive_for


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

    def test_progressive_for(self):
        assert list(progressive_for(map(lambda x: x ** 2, range(1, 6)), 3)) == [
            (1, 4, 9), (1, 4, 16), (1, 4, 25), (1, 9, 16), (1, 9, 25), (1, 16, 25),
            (4, 9, 16), (4, 9, 25), (4, 16, 25),
            (9, 16, 25),
        ]
        assert list(progressive_for(map(lambda x: x ** 2, range(1, 6)), 3, 1)) == [
            (1, 4, 9), (1, 4, 16), (1, 4, 25), (1, 9, 16), (1, 9, 25), (1, 16, 25),
            (4, 9, 16), (4, 9, 25), (4, 16, 25),
            (9, 16, 25),
        ]
        assert list(progressive_for(map(lambda x: x ** 2, range(1, 6)), 3, 0)) == [
            (1, 1, 1), (1, 1, 4), (1, 1, 9), (1, 1, 16), (1, 1, 25),
            (1, 4, 4), (1, 4, 9), (1, 4, 16), (1, 4, 25),
            (1, 9, 9), (1, 9, 16), (1, 9, 25),
            (1, 16, 16), (1, 16, 25),
            (1, 25, 25),

            (4, 4, 4), (4, 4, 9), (4, 4, 16), (4, 4, 25),
            (4, 9, 9), (4, 9, 16), (4, 9, 25),
            (4, 16, 16), (4, 16, 25),
            (4, 25, 25),

            (9, 9, 9), (9, 9, 16), (9, 9, 25),
            (9, 16, 16), (9, 16, 25),
            (9, 25, 25),

            (16, 16, 16), (16, 16, 25),
            (16, 25, 25),

            (25, 25, 25),
        ]
        assert list(progressive_for(map(lambda x: x ** 2, range(1, 6)), 3, 2)) == [
            (1, 9, 25)
        ]

        with pytest.raises(ValueError):
            progressive_for(map(lambda x: x ** 2, range(1, 6)), 3, -1)
