import pytest

from hbutils.string import ordinal, ordinalize


@pytest.mark.unittest
class TestStringOrdinal:
    def test_ordinal(self):
        assert ordinal(1) == 'st'
        assert ordinal(2) == 'nd'
        assert ordinal(3) == 'rd'
        assert ordinal(4) == 'th'
        assert ordinal(10) == 'th'
        assert ordinal(11) == 'th'
        assert ordinal(21) == 'st'
        assert ordinal(1001) == 'st'

    def test_ordinalize(self):
        assert ordinalize(1) == '1st'
        assert ordinalize(2) == '2nd'
        assert ordinalize(3) == '3rd'
        assert ordinalize(4) == '4th'
        assert ordinalize(10) == '10th'
        assert ordinalize(11) == '11th'
        assert ordinalize(21) == '21st'
        assert ordinalize(1001) == '1001st'
