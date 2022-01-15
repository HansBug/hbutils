import pytest

from hbutils.string import truncate


@pytest.mark.unittest
class TestStringTrunc:
    def test_truncate(self):
        assert truncate(
            'this is the first time we do this kind of thing') == 'this is the first time we do this kind of thing'
        assert truncate('this is the first time we do this kind of thing', width=30) == 'this is the first time we ... '
        assert truncate('this is the first time we do this kind of thing', width=40, tail_length=12,
                        show_length=True) == 'this is the ..(47 chars).. ind of thing'
