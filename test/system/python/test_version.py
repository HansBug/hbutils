import sys

import pytest
from pkg_resources import parse_version

from hbutils.system import python_version

_Version = type(parse_version("0.0.1"))


@pytest.mark.unittest
class TestSystemPythonVersion:
    def test_python_version(self):
        _actual_version = sys.version_info
        _get_version = python_version()
        assert isinstance(_get_version, _Version)
        assert _get_version.major == _actual_version.major
        assert _get_version.minor == _actual_version.minor
        assert _get_version.micro == _actual_version.micro
