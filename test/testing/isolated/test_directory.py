import os.path
import pathlib
from textwrap import dedent

import pytest

from hbutils.testing import isolated_directory


@pytest.mark.unittest
class TestLoggingIsolatedDirectory:
    def test_isolated_directory_simple(self):
        _filename = 'this_is_a_very_strange_file_name.txt'
        with isolated_directory():
            with open(_filename, 'w') as f:
                print("Line 1", file=f)
                print("Line 2rd", file=f)

            assert os.path.exists(_filename)
            assert not os.path.exists('README.md')
            assert pathlib.Path(_filename).read_text().strip() == dedent("""
                Line 1
                Line 2rd
            """).strip()

        assert not os.path.exists(_filename)
        assert os.path.exists('README.md')

    def test_isolated_directory_with_mapping(self):
        readme = pathlib.Path('README.md').read_text()
        testing_init = pathlib.Path('hbutils/testing/__init__.py').read_text()
        testing_dirs = os.listdir('hbutils/testing')
        with isolated_directory({
            'README.md': 'README.md',
            'ts': 'hbutils/testing',
        }):
            assert pathlib.Path('README.md').read_text() == readme
            assert pathlib.Path('ts/__init__.py').read_text() == testing_init
            assert os.listdir('ts') == testing_dirs

    def test_isolated_directory_with_nested_dir(self):
        readme = pathlib.Path('README.md').read_text()
        testing_init = pathlib.Path('hbutils/testing/__init__.py').read_text()
        testing_dirs = os.listdir('hbutils/testing')
        with isolated_directory({
            '1/2/3/README.md': 'README.md',
            '1/3/ts': 'hbutils/testing',
        }):
            assert os.path.exists('1/2/3/README.md')
            assert pathlib.Path('1/2/3/README.md').read_text() == readme

            assert os.path.exists('1/3/ts')
            assert pathlib.Path('1/3/ts/__init__.py').read_text() == testing_init
            assert os.listdir('1/3/ts') == testing_dirs
