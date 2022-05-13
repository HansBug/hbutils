import io

import pytest

from hbutils.binary import c_int8, c_int16, c_int32, c_int64, c_short, c_int, c_long, c_longlong
from .base import linux_mark, windows_mark, macos_mark


class TestBinaryUint:
    @pytest.mark.unittest
    def test_int8(self):
        assert c_int8.size == 1
        assert c_int8.minimum == -128
        assert c_int8.maximum == 127

        with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
            assert c_int8.read(file) == -34
            assert c_int8.read(file) == -83
            assert c_int8.read(file) == -66
            assert c_int8.read(file) == -17
            assert c_int8.read(file) == 18
            assert c_int8.read(file) == 52
            assert c_int8.read(file) == 86
            assert c_int8.read(file) == 120

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_int8.write(file, 'dkslf')
            with pytest.raises(ValueError):
                c_int8.write(file, -129)
            with pytest.raises(ValueError):
                c_int8.write(file, 128)

            c_int8.write(file, -34)
            c_int8.write(file, -83)
            c_int8.write(file, -66)
            c_int8.write(file, -17)
            c_int8.write(file, 18)
            c_int8.write(file, 52)
            c_int8.write(file, 86)
            c_int8.write(file, 120)

            assert file.getvalue() == b'\xde\xad\xbe\xef\x12\x34\x56\x78'

    @pytest.mark.unittest
    def test_int16(self):
        assert c_int16.size == 2
        assert c_int16.minimum == -32768
        assert c_int16.maximum == 32767

        with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
            assert c_int16.read(file) == -21026
            assert c_int16.read(file) == -4162
            assert c_int16.read(file) == 13330
            assert c_int16.read(file) == 30806

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_int16.write(file, 'dkslf')
            with pytest.raises(ValueError):
                c_int16.write(file, -32769)
            with pytest.raises(ValueError):
                c_int16.write(file, 32768)

            c_int16.write(file, -21026)
            c_int16.write(file, -4162)
            c_int16.write(file, 13330)
            c_int16.write(file, 30806)

            assert file.getvalue() == b'\xde\xad\xbe\xef\x12\x34\x56\x78'

    @pytest.mark.unittest
    def test_int32(self):
        assert c_int32.size == 4
        assert c_int32.minimum == -2147483648
        assert c_int32.maximum == 2147483647

        with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
            assert c_int32.read(file) == -272716322
            assert c_int32.read(file) == 2018915346

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_int32.write(file, 'dkslf')
            with pytest.raises(ValueError):
                c_int32.write(file, -2147483649)
            with pytest.raises(ValueError):
                c_int32.write(file, 2147483648)

            c_int32.write(file, -272716322)
            c_int32.write(file, 2018915346)

            assert file.getvalue() == b'\xde\xad\xbe\xef\x12\x34\x56\x78'

    @pytest.mark.unittest
    def test_int64(self):
        assert c_int64.size == 8
        assert c_int64.minimum == -(1 << 63)
        assert c_int64.maximum == (1 << 63) - 1

        with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78'
                        b'xV4\x12xV4\x12') as file:
            assert c_int64.read(file) == 8671175388484775390
            assert c_int64.read(file) == 1311768465173141112

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_int64.write(file, 'dkslf')
            with pytest.raises(ValueError):
                c_int64.write(file, -(1 << 63) - 1)
            with pytest.raises(ValueError):
                c_int64.write(file, 1 << 63)

            c_int64.write(file, 8671175388484775390)
            c_int64.write(file, 1311768465173141112)

            assert file.getvalue() == b'\xde\xad\xbe\xef\x12\x34\x56\x78' \
                                      b'xV4\x12xV4\x12'

    @linux_mark
    def test_eq_ubuntu_1804(self):
        assert c_short is c_int16
        assert c_int is c_int32
        assert c_long is c_int64
        assert c_longlong is c_int64

    @windows_mark
    def test_eq_windows_2019(self):
        assert c_short is c_int16
        assert c_int is c_int32
        assert c_long is c_int32
        assert c_longlong is c_int64

    @macos_mark
    def test_eq_macos_10(self):
        assert c_short is c_int16
        assert c_int is c_int32
        assert c_long is c_int64
        assert c_longlong is c_int64
