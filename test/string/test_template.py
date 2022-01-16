import pytest

from hbutils.string import env_template


@pytest.mark.unittest
class TestStringTemplate:
    def test_env_template(self):
        assert env_template('sdkjflsd') == 'sdkjflsd'
        assert env_template('this is the ${number} day.', dict(number='1st')) == 'this is the 1st day.'
        with pytest.raises(KeyError):
            env_template('this is the ${number} day')
