import pytest

from hbutils.random import random_bytes


@pytest.mark.unittest
class TestRandomBinary:
    def test_random_bytes(self):
        for _ in range(1000):
            b1 = random_bytes()
            assert len(b1) == 32
            assert b'\0' not in b1

        for _ in range(1000):
            b1 = random_bytes(128)
            assert len(b1) == 128
            assert b'\0' not in b1

        once = False
        for _ in range(1000):
            b1 = random_bytes(allow_zero=True)
            assert len(b1) == 32
            once = once or (b'\0' in b1)
        assert once, f'Zero should appear at least once.'
