from unittest import mock

import pytest
from pkg_resources import parse_version

from hbutils.system import package_version
from hbutils.system.python.package import PIP_PACKAGES
from .test_version import _Version


@pytest.mark.unittest
class TestSystemPythonPackage:
    def test_package_version(self):
        assert isinstance(package_version("chardet"), _Version)
        assert package_version("chardet") >= parse_version("3.0.4")
        assert package_version("chardet") < parse_version("5")
        assert package_version("This_is_an_fxxking_name") is None

        with mock.patch.dict(PIP_PACKAGES, {'pip': '19.3.1'}):
            assert package_version('pip') == parse_version('19.3.1')
            assert package_version('PIP') == parse_version('19.3.1')
            assert package_version('pipxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') is None
