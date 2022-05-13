import io

import pytest

from hbutils.binary import c_uint8, c_uint16, c_uint32, c_uint64, c_byte, c_ushort, c_uint, c_ulong, c_ulonglong
from .base import linux_mark, windows_mark, macos_mark


@pytest.mark.unittest
class TestBinaryUint:
    def test_int8(self):
        assert c_uint8.size == 1
        assert c_uint8.minimum == 0
        assert c_uint8.maximum == 0xff

        with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
            assert c_uint8.read(file) == 0xde
            assert c_uint8.read(file) == 0xad
            assert c_uint8.read(file) == 0xbe
            assert c_uint8.read(file) == 0xef
            assert c_uint8.read(file) == 0x12
            assert c_uint8.read(file) == 0x34
            assert c_uint8.read(file) == 0x56
            assert c_uint8.read(file) == 0x78

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_uint8.write(file, 'dkslf')
            with pytest.raises(ValueError):
                c_uint8.write(file, -1)
            with pytest.raises(ValueError):
                c_uint8.write(file, 0x100)

            c_uint8.write(file, 0xde)
            c_uint8.write(file, 0xad)
            c_uint8.write(file, 0xbe)
            c_uint8.write(file, 0xef)
            c_uint8.write(file, 0x12)
            c_uint8.write(file, 0x34)
            c_uint8.write(file, 0x56)
            c_uint8.write(file, 0x78)

            assert file.getvalue() == b'\xde\xad\xbe\xef\x12\x34\x56\x78'

    def test_uint16(self):
        assert c_uint16.size == 2
        assert c_uint16.minimum == 0
        assert c_uint16.maximum == 0xffff

        with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
            assert c_uint16.read(file) == 0xadde
            assert c_uint16.read(file) == 0xefbe
            assert c_uint16.read(file) == 0x3412
            assert c_uint16.read(file) == 0x7856

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_uint16.write(file, 'dkslf')
            with pytest.raises(ValueError):
                c_uint16.write(file, -1)
            with pytest.raises(ValueError):
                c_uint16.write(file, 0x10000)

            c_uint16.write(file, 0xadde)
            c_uint16.write(file, 0xefbe)
            c_uint16.write(file, 0x3412)
            c_uint16.write(file, 0x7856)

            assert file.getvalue() == b'\xde\xad\xbe\xef\x12\x34\x56\x78'

    def test_uint32(self):
        assert c_uint32.size == 4
        assert c_uint32.minimum == 0
        assert c_uint32.maximum == 0xffffffff

        with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78') as file:
            assert c_uint32.read(file) == 0xefbeadde
            assert c_uint32.read(file) == 0x78563412

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_uint32.write(file, 'dkslf')
            with pytest.raises(ValueError):
                c_uint32.write(file, -1)
            with pytest.raises(ValueError):
                c_uint32.write(file, 0x100000000)

            c_uint32.write(file, 0xefbeadde)
            c_uint32.write(file, 0x78563412)

            assert file.getvalue() == b'\xde\xad\xbe\xef\x12\x34\x56\x78'

    def test_uint64(self):
        assert c_uint64.size == 8
        assert c_uint64.minimum == 0
        assert c_uint64.maximum == 0xffffffffffffffff

        with io.BytesIO(b'\xde\xad\xbe\xef\x12\x34\x56\x78'
                        b'xV4\x12xV4\x12') as file:
            assert c_uint64.read(file) == 0x78563412efbeadde
            assert c_uint64.read(file) == 0x1234567812345678

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_uint64.write(file, 'dkslf')
            with pytest.raises(ValueError):
                c_uint64.write(file, -1)
            with pytest.raises(ValueError):
                c_uint64.write(file, 0x10000000000000000)

            c_uint64.write(file, 0x78563412efbeadde)
            c_uint64.write(file, 0x1234567812345678)

            assert file.getvalue() == b'\xde\xad\xbe\xef\x12\x34\x56\x78' \
                                      b'xV4\x12xV4\x12'

    @linux_mark
    def test_eq_ubuntu_1804(self):
        assert c_byte is c_uint8
        assert c_ushort is c_uint16
        assert c_uint is c_uint32
        assert c_ulong is c_uint64
        assert c_ulonglong is c_uint64

    @windows_mark
    def test_eq_windows_2019(self):
        assert c_byte is c_uint8
        assert c_ushort is c_uint16
        assert c_uint is c_uint32
        assert c_ulong is c_uint32
        assert c_ulonglong is c_uint64

    @macos_mark
    def test_eq_macos_10(self):
        assert c_byte is c_uint8
        assert c_ushort is c_uint16
        assert c_uint is c_uint32
        assert c_ulong is c_uint64
        assert c_ulonglong is c_uint64
