import io
import pathlib

import pytest

from hbutils.file import is_eof, getsize, keep_cursor
from hbutils.testing import isolated_directory


@pytest.mark.unittest
class TestFileFile:
    def test_keep_cursor(self):
        with io.BytesIO(b'\x12\x34\x56\x78') as file:
            with keep_cursor(file):
                assert file.read(2) == b'\x12\x34'

            with keep_cursor(file):
                assert file.read() == b'\x12\x34\x56\x78'

            _ = file.read(2)

            with keep_cursor(file):
                assert file.read(1) == b'\x56'
                assert file.read(1) == b'\x78'

            with keep_cursor(file):
                assert file.read() == b'\x56\x78'

    def test_getsize_bytesio(self):
        with io.BytesIO() as file:
            assert getsize(file) == 0

        with io.BytesIO(b'\x12\x34\x56\x78') as file:
            assert getsize(file) == 4
            assert file.tell() == 0

        with io.BytesIO(b'\x12\x34\x56\x78') as file:
            _ = file.read(2)
            assert getsize(file) == 4
            assert file.tell() == 2

    def test_getsize_stringio(self):
        with io.StringIO() as file:
            assert getsize(file) == 0

        with io.StringIO('\x12\x34\x56\x78') as file:
            assert getsize(file) == 4
            assert file.tell() == 0

        with io.StringIO('\x12\x34\x56\x78') as file:
            _ = file.read(2)
            assert getsize(file) == 4
            assert file.tell() == 2

    def test_getsize_bin_file(self):
        with isolated_directory():
            pathlib.Path('binfile').write_bytes(b'\x12\x34\x56\x78')
            with open('binfile', 'rb') as file:
                assert getsize(file) == 4
                assert file.tell() == 0

            with open('binfile', 'rb') as file:
                _ = file.read(2)
                assert getsize(file) == 4
                assert file.tell() == 2

    def test_getsize_str_file(self):
        with isolated_directory():
            pathlib.Path('strfile').write_text('abcd')
            with open('strfile', 'r') as file:
                assert getsize(file) == 4
                assert file.tell() == 0

            with open('strfile', 'r') as file:
                _ = file.read(2)
                assert getsize(file) == 4
                assert file.tell() == 2

    def test_is_eof_io(self):
        with io.BytesIO() as file:
            assert is_eof(file)

        with io.BytesIO(b'\x12\x34\x56\x78') as file:
            assert file.read(2) == b'\x12\x34'
            assert not is_eof(file)

            assert file.read(1) == b'\x56'
            assert not is_eof(file)

            assert file.read(1) == b'\x78'
            assert is_eof(file)

        with io.StringIO() as file:
            assert is_eof(file)

        with io.StringIO('abcd') as file:
            assert file.read(2) == 'ab'
            assert not is_eof(file)

            assert file.read(1) == 'c'
            assert not is_eof(file)

            assert file.read(1) == 'd'
            assert is_eof(file)

    def test_is_eof_file(self):
        with isolated_directory():
            pathlib.Path('binfile').write_bytes(b'\x12\x34\x56\x78')

            with open('binfile', 'rb') as file:
                _ = file.read(2)
                assert not is_eof(file)

                _ = file.read(1)
                assert not is_eof(file)

                _ = file.read(1)
                assert is_eof(file)

        with isolated_directory():
            pathlib.Path('strfile').write_text('abcd')

            with open('strfile', 'r') as file:
                _ = file.read(2)
                assert not is_eof(file)

                _ = file.read(1)
                assert not is_eof(file)

                _ = file.read(1)
                assert is_eof(file)
