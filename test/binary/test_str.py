import io

import pytest

from hbutils.binary import c_str, c_sized_str


@pytest.mark.unittest
class TestBinaryStr:
    def test_str(self):
        assert c_str.encoding is None

        with io.BytesIO(
                b'kdsfjldsjflkdsmgds\x00'
                b'\xd0\x94\xd0\xbe\xd0\xb1\xd1\x80\xd1\x8b\xd0\xb9 \xd0'
                b'\xb2\xd0\xb5\xd1\x87\xd0\xb5\xd1\x80\x00'
                b'\xa4\xb3\xa4\xf3\xa4\xd0\xa4\xf3\xa4\xcf\x00'
                b'\xcd\xed\xc9\xcf\xba\xc3\x00'
        ) as file:
            assert c_str.read(file) == "kdsfjldsjflkdsmgds"
            assert c_str.read(file) == "Добрый вечер"
            assert c_str.read(file) == "こんばんは"
            assert c_str.read(file) == "晚上好"

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                c_str.write(file, 1)

            c_str.write(file, "kdsfjldsjflkdsmgds")
            c_str.write(file, "Добрый вечер")
            c_str.write(file, "こんばんは")
            c_str.write(file, "晚上好")

            assert file.getvalue() == b'kdsfjldsjflkdsmgds\x00' \
                                      b'\xd0\x94\xd0\xbe\xd0\xb1\xd1\x80\xd1\x8b\xd0\xb9 ' \
                                      b'\xd0\xb2\xd0\xb5\xd1\x87\xd0\xb5\xd1\x80\x00' \
                                      b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xb0\xe3\x82\x93\xe3\x81\xaf\x00' \
                                      b'\xe6\x99\x9a\xe4\xb8\x8a\xe5\xa5\xbd\x00'

    def test_sized_str(self):
        ss = c_sized_str(10)
        assert ss.encoding is None
        assert ss.size == 10

        with io.BytesIO(
                b'1234567890'
                b'123\x00\x00\x00\x00\x00\x00\x00'
                b'\xe6\x99\x9a\xe4\xb8\x8a\xe5\xa5\xbd\x00'
                b'\xe6\x99\x9a\xe4\xb8\x8a\x00\x00\x00\x00'
        ) as file:
            assert ss.read(file) == '1234567890'
            assert ss.read(file) == '123'
            assert ss.read(file) == "晚上好"
            assert ss.read(file) == "晚上"

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                ss.write(file, 123)

            ss.write(file, '1234567890')
            ss.write(file, '123')
            ss.write(file, "晚上好")
            ss.write(file, "晚上")

            assert file.getvalue() == b'1234567890' \
                                      b'123\x00\x00\x00\x00\x00\x00\x00' \
                                      b'\xe6\x99\x9a\xe4\xb8\x8a\xe5\xa5\xbd\x00' \
                                      b'\xe6\x99\x9a\xe4\xb8\x8a\x00\x00\x00\x00'
