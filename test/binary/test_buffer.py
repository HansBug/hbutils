import io

import pytest

from hbutils.binary import c_buffer


@pytest.mark.unittest
class TestBinaryBuffer:
    def test_buffer(self):
        cb = c_buffer(10)
        assert cb.size == 10

        with io.BytesIO(b'1234567890abcdef\xde\xad\xbe\xef') as file:
            assert cb.read(file) == b'1234567890'
            assert cb.read(file) == b'abcdef\xde\xad\xbe\xef'

        with io.BytesIO() as file:
            with pytest.raises(TypeError):
                cb.write(file, 123)
            with pytest.raises(ValueError):
                cb.write(file, b'1' * 20)

            cb.write(file, b'1234567890')
            cb.write(file, b'123')
            cb.write(file, b'abcdef\xde\xad\xbe\xef')
            cb.write(file, b'abcdef')

            assert file.getvalue() == b'1234567890' \
                                      b'123\x00\x00\x00\x00\x00\x00\x00' \
                                      b'abcdef\xde\xad\xbe\xef' \
                                      b'abcdef\x00\x00\x00\x00'
