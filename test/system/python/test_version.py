import sys

import pytest
from packaging.version import Version

from hbutils.system import python_version


@pytest.mark.unittest
class TestSystemPythonVersion:
    def test_python_version(self):
        _actual_version = sys.version_info
        _get_version = python_version()
        assert isinstance(_get_version, Version)
        assert _get_version.major == _actual_version.major
        assert _get_version.minor == _actual_version.minor
        assert _get_version.micro == _actual_version.micro
