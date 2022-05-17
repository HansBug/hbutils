import io

import pytest

from hbutils.binary import c_bool


@pytest.mark.unittest
class TestBinaryBool:
    def test_bool(self):
        assert c_bool.size == 1

        with io.BytesIO(b'\x01\x00\x01\x00\x00') as file:
            assert c_bool.read(file) is True
            assert c_bool.read(file) is False
            assert c_bool.read(file) is True
            assert c_bool.read(file) is False
            assert c_bool.read(file) is False

        with io.BytesIO() as file:
            c_bool.write(file, True)
            c_bool.write(file, False)
            c_bool.write(file, True)
            c_bool.write(file, False)
            c_bool.write(file, False)

            assert file.getvalue() == b'\x01\x00\x01\x00\x00'
