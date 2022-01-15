import pytest

from hbutils.scale import time_to_duration, time_to_delta_str


@pytest.mark.unittest
class TestScaleTime:
    def test_time_to_duration(self):
        assert time_to_duration(2) == 2
        assert time_to_duration(2.3) == 2.3
        assert time_to_duration('2s') == 2
        assert time_to_duration('2min5s') == 125
        assert time_to_duration('1h5.5s') == 3605.5

    def test_time_to_duration_invalid(self):
        with pytest.raises(TypeError):
            time_to_duration([1, 2, 3])

    def test_time_to_delta_str(self):
        assert time_to_delta_str(2) == '0:00:02'
        assert time_to_delta_str(2.3) == '0:00:02.300000'
        assert time_to_delta_str('2s') == '0:00:02'
        assert time_to_delta_str('2min5s') == '0:02:05'
        assert time_to_delta_str('2min170s') == '0:04:50'
        assert time_to_delta_str('1h5.5s') == '1:00:05.500000'
