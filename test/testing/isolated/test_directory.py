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
