import io
import math

import pytest

from hbutils.binary import c_float32, c_uint32, c_float64, c_uint64


@pytest.mark.unittest
class TestBinaryFloat:
    def test_c_float32_basic(self):
        assert c_float32.size == 4
        assert c_float32.mark == 'f'

    def test_c_float32_read(self):
        with io.BytesIO() as file:
            c_uint32.write(file, 0x7f900000)
            c_uint32.write(file, 0x7f800000)
            c_uint32.write(file, 0xff800000)

            file.seek(0, io.SEEK_SET)
            assert math.isnan(c_float32.read(file))
            assert c_float32.read(file) == +math.inf
            assert c_float32.read(file) == -math.inf

        with io.BytesIO() as file:
            c_uint32.write(file, 0x41440000)
            c_uint32.write(file, 0xc13ea000)

            file.seek(0, io.SEEK_SET)
            assert c_float32.read(file) == pytest.approx(12.25)
            assert c_float32.read(file) == pytest.approx(-11.9140625)

        with io.BytesIO() as file:
            c_uint32.write(file, 0x00000000)
            c_uint32.write(file, 0x00f00000)
            c_uint32.write(file, 0x00700000)
            c_uint32.write(file, 0x00000001)
            c_uint32.write(file, 0x80700000)
            c_uint32.write(file, 0x80000001)

            file.seek(0, io.SEEK_SET)
            assert c_float32.read(file) == pytest.approx(0.0)
            assert c_float32.read(file) == pytest.approx(2.204051907791789e-38, abs=0.0, rel=1e-6)
            assert c_float32.read(file) == pytest.approx(1.0285575569695016e-38, abs=0.0, rel=1e-6)
            assert c_float32.read(file) == pytest.approx(1.401298464324817e-45, abs=0.0, rel=1e-6)
            assert c_float32.read(file) == pytest.approx(-1.0285575569695016e-38, abs=0.0, rel=1e-6)
            assert c_float32.read(file) == pytest.approx(-1.401298464324817e-45, abs=0.0, rel=1e-6)

        with io.BytesIO() as file:
            c_uint32.write(file, 0x453153d1)
            c_uint32.write(file, 0xc53153d1)
            c_uint32.write(file, 0x985b854c)

            file.seek(0, io.SEEK_SET)
            assert c_float32.read(file) == pytest.approx(2837.23847928394827394)
            assert c_float32.read(file) == pytest.approx(-2837.23847928394827394)
            assert c_float32.read(file) == pytest.approx(-2.837238430962332e-24, abs=0.0, rel=1e-6)

    def test_c_float32_write(self):
        with io.BytesIO() as file:
            c_float32.write(file, math.nan)
            c_float32.write(file, +math.inf)
            c_float32.write(file, -math.inf)
            c_float32.write(file, +1e300)
            c_float32.write(file, -1e300)

            assert file.getvalue() == b'\x00\x00\xc0\x7f' \
                                      b'\x00\x00\x80\x7f' \
                                      b'\x00\x00\x80\xff' \
                                      b'\x00\x00\x80\x7f' \
                                      b'\x00\x00\x80\xff'

        with io.BytesIO() as file:
            c_float32.write(file, 12.25)
            c_float32.write(file, -11.9140625)

            assert file.getvalue() == b'\x00\x00\x44\x41' \
                                      b'\x00\xa0\x3e\xc1'

        with io.BytesIO() as file:
            c_float32.write(file, 0.0)
            c_float32.write(file, 3e-300)
            c_float32.write(file, -3e-300)
            c_float32.write(file, 2.204051907791789e-38)
            c_float32.write(file, 1.0285575569695016e-38)
            c_float32.write(file, 1.401298464324817e-45)
            c_float32.write(file, -1.0285575569695016e-38)
            c_float32.write(file, -1.401298464324817e-45)

            assert file.getvalue() == b'\x00\x00\x00\x00' \
                                      b'\x00\x00\x00\x00' \
                                      b'\x00\x00\x00\x80' \
                                      b'\x00\x00\xf0\x00' \
                                      b'\x00\x00\x70\x00' \
                                      b'\x01\x00\x00\x00' \
                                      b'\x00\x00\x70\x80' \
                                      b'\x01\x00\x00\x80'

        with io.BytesIO() as file:
            c_float32.write(file, 2837.23847928394827394)
            c_float32.write(file, -2837.23847928394827394)
            c_float32.write(file, -2.837238430962332e-24)

            assert file.getvalue() == b'\xd1\x53\x31\x45' \
                                      b'\xd1\x53\x31\xc5' \
                                      b'\x4c\x85\x5b\x98'

    def test_c_float64_basic(self):
        assert c_float64.size == 8
        assert c_float64.mark == 'd'

    def test_c_float64_read(self):
        with io.BytesIO() as file:
            c_uint64.write(file, 0x7ff8000000000000)
            c_uint64.write(file, 0x7ff0000000000000)
            c_uint64.write(file, 0xfff0000000000000)

            file.seek(0, io.SEEK_SET)
            assert math.isnan(c_float64.read(file))
            assert c_float64.read(file) == +math.inf
            assert c_float64.read(file) == -math.inf

        with io.BytesIO() as file:
            c_uint64.write(file, 0x4028800000000000)
            c_uint64.write(file, 0xc027d40000000000)

            file.seek(0, io.SEEK_SET)
            assert c_float64.read(file) == pytest.approx(12.25)
            assert c_float64.read(file) == pytest.approx(-11.9140625)

        with io.BytesIO() as file:
            c_uint64.write(file, 0x0000000000000000)
            c_uint64.write(file, 0x001f000000000000)
            c_uint64.write(file, 0x000e000000000000)
            c_uint64.write(file, 0x0000000000000001)
            c_uint64.write(file, 0x800e000000000000)
            c_uint64.write(file, 0x8000000000000001)

            file.seek(0, io.SEEK_SET)
            assert c_float64.read(file) == pytest.approx(0.0)
            assert c_float64.read(file) == pytest.approx(4.31108e-308, abs=0.0, rel=1e-6)
            assert c_float64.read(file) == pytest.approx(1.94694e-308, abs=0.0, rel=1e-6)
            assert c_float64.read(file) == pytest.approx(4.94066e-324, abs=0.0, rel=1e-6)
            assert c_float64.read(file) == pytest.approx(-1.94694e-308, abs=0.0, rel=1e-6)
            assert c_float64.read(file) == pytest.approx(-4.94066e-324, abs=0.0, rel=1e-6)

        with io.BytesIO() as file:
            c_uint64.write(file, 0x40a62a7a19f4eaaa)
            c_uint64.write(file, 0xc0a62a7a19f4eaaa)
            c_uint64.write(file, 0xbb0b70a980000000)

            file.seek(0, io.SEEK_SET)
            assert c_float64.read(file) == pytest.approx(2837.23847928394827394)
            assert c_float64.read(file) == pytest.approx(-2837.23847928394827394)
            assert c_float64.read(file) == pytest.approx(-2.837238430962332e-24, abs=0.0, rel=1e-6)

    def test_c_float64_write(self):
        with io.BytesIO() as file:
            c_float64.write(file, math.nan)
            c_float64.write(file, +math.inf)
            c_float64.write(file, -math.inf)

            assert file.getvalue() == b'\x00\x00\x00\x00\x00\x00\xf8\x7f' \
                                      b'\x00\x00\x00\x00\x00\x00\xf0\x7f' \
                                      b'\x00\x00\x00\x00\x00\x00\xf0\xff'

        with io.BytesIO() as file:
            c_float64.write(file, 12.25)
            c_float64.write(file, -11.9140625)

            assert file.getvalue() == b'\x00\x00\x00\x00\x00\x80\x28\x40' \
                                      b'\x00\x00\x00\x00\x00\xd4\x27\xc0'

        with io.BytesIO() as file:
            c_float64.write(file, 0.0)
            c_float64.write(file, 3e-300)
            c_float64.write(file, -3e-300)
            c_float64.write(file, 2.204051907791789e-38)
            c_float64.write(file, 1.0285575569695016e-38)
            c_float64.write(file, 1.401298464324817e-45)
            c_float64.write(file, -1.0285575569695016e-38)
            c_float64.write(file, -1.401298464324817e-45)

            assert file.getvalue() == b'\x00\x00\x00\x00\x00\x00\x00\x00' \
                                      b'\x83\xb6:\xd2\x97\x12\xc0\x01' \
                                      b'\x83\xb6:\xd2\x97\x12\xc0\x81' \
                                      b'\x00\x00\x00\x00\x00\x00\x1e8' \
                                      b'\x00\x00\x00\x00\x00\x00\x0c8' \
                                      b'\x00\x00\x00\x00\x00\x00\xa06' \
                                      b'\x00\x00\x00\x00\x00\x00\x0c\xb8' \
                                      b'\x00\x00\x00\x00\x00\x00\xa0\xb6'
