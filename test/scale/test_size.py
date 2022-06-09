import pytest
from bitmath import MiB, GB

from hbutils.scale import size_to_bytes, size_to_bytes_str


@pytest.mark.unittest
class TestScaleSize:
    def test_size_to_bytes(self):
        assert size_to_bytes(233) == 233
        with pytest.warns(UserWarning):
            assert size_to_bytes(2.3) == 2
        assert size_to_bytes('2KB') == 2000
        assert size_to_bytes('2KiB') == 2048
        assert size_to_bytes('2kb') == 2000
        assert size_to_bytes('2kib') == 2048
        assert size_to_bytes(MiB(512)) == 512 << 20
        assert size_to_bytes(GB(3)) == 3 * 10 ** 9

    def test_size_to_bytes_invalid(self):
        with pytest.raises(TypeError):
            assert size_to_bytes([1, 2, 3])

    def test_size_to_bytes_str(self):
        assert size_to_bytes_str(233) == '233.0 Byte'
        with pytest.warns(UserWarning):
            assert size_to_bytes_str(233.3) == '233.0 Byte'
        assert size_to_bytes_str('200000kib') == '195.3125 MiB'
        assert size_to_bytes_str('3.54 GB', precision=0) == '3 GiB'
        assert size_to_bytes_str('3.54 GB', precision=3) == '3.297 GiB'
