import pytest

from hbutils.scale import size_to_bytes, size_to_bytes_str


@pytest.mark.unittest
class TestScaleSize:
    def test_size_to_bytes(self):
        from bitmath import MiB, GB

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
        assert size_to_bytes_str('3.54 GB', system='si') == '3.54 GB'
        assert size_to_bytes_str('3.54 GB', system='si', precision=3) == '3.540 GB'

    def test_size_to_bytes_with_int(self):
        assert size_to_bytes(1024) == 1024

    def test_size_to_bytes_with_float(self):
        assert size_to_bytes(1024.0) == 1024

    def test_size_to_bytes_with_str(self):
        assert size_to_bytes('1 KB') == 1000

    def test_size_to_bytes_with_unsupported_type(self):
        with pytest.raises(TypeError):
            size_to_bytes([1024])

    def test_size_to_bytes_str(self):
        assert size_to_bytes_str(1024) == '1.0 KiB'

    def test_size_to_bytes_str_with_precision(self):
        assert size_to_bytes_str(1500, precision=2) == '1.46 KiB'

    def test_size_to_bytes_str_with_sigfigs(self):
        assert size_to_bytes_str(1500, sigfigs=3) == '1.46 KiB'

    def test_size_to_bytes_str_with_system(self):
        assert size_to_bytes_str(1000, system='si') == '1.0 kB'

    def test_size_to_bytes_str_with_invalid_system(self):
        with pytest.raises(ValueError):
            size_to_bytes_str(1000, system='invalid')

    def test_size_to_bytes_str_warning(self):
        with pytest.warns(UserWarning):
            size_to_bytes_str('3.54 GiB')
