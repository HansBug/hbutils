import os
import pathlib

import pytest

from hbutils.system import copy
from hbutils.testing import isolated_directory


@pytest.mark.unittest
class TestSystemFilesystemDirectory:
    def test_copy_file(self):
        with isolated_directory():
            with open('file1.txt', 'w') as f1:
                print('File 1', file=f1)

            copy('file1.txt', 'new_file1.txt')
            assert pathlib.Path('new_file1.txt').read_text().strip() == 'File 1'

    def test_copy_directory(self):
        with isolated_directory():
            os.makedirs('1/2', exist_ok=True)
            os.makedirs('1/3', exist_ok=True)
            with open('1/2/file1.txt', 'w') as f1:
                print('File 1', file=f1)
            with open('1/3/file2.txt', 'w') as f1:
                print('File 2', file=f1)
            with open('1/file3.txt', 'w') as f1:
                print('File 3', file=f1)

            copy('1', 'new_1')
            assert pathlib.Path('new_1/2/file1.txt').read_text().strip() == 'File 1'
            assert pathlib.Path('new_1/3/file2.txt').read_text().strip() == 'File 2'
            assert pathlib.Path('new_1/file3.txt').read_text().strip() == 'File 3'