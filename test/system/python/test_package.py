from unittest import mock, skipUnless

import packaging
import pip as _pip_pkg
import pytest
from pkg_resources import parse_version

from hbutils.system import package_version, load_req_file, check_reqs, check_req_file, pip, pip_install
from hbutils.testing import capture_output, vpip
from .test_version import _Version
from ...testings import get_testfile_path


@pytest.mark.unittest
class TestSystemPythonPackage:
    def test_package_version(self):
        assert isinstance(package_version("chardet"), _Version)
        assert package_version("chardet") >= parse_version("3.0.4")
        assert package_version("chardet") < parse_version("5")
        assert package_version("This_is_an_fxxking_name") is None

        with mock.patch.dict('hbutils.system.python.package.PIP_PACKAGES', {'pip': '19.3.1'}):
            assert package_version('pip') == parse_version('19.3.1')
            assert package_version('PIP') == parse_version('19.3.1')
            assert package_version('pipxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') is None

    def test_load_req_file(self):
        assert load_req_file(get_testfile_path('requirements-1.txt')) == [
            'chardet<5,>=3.0.4', 'bitmath>=1.3.3.1', 'pytimeparse>=1.1.8',
            'inflect>=5.2.0', 'packaging>=21.3', 'setuptools>=50.0'
        ]

    def test_check_reqs(self):
        assert check_reqs(['packaging>=21.3', 'setuptools>=50.0'])
        assert not check_reqs(['packaging>=21.3', 'setuptools<48.0'])

    def test_check_req_file(self):
        assert check_req_file('requirements.txt')
        assert not check_req_file(get_testfile_path('requirements-2.txt'))

    def test_pip(self):
        with capture_output() as co:
            pip('-V')
        assert _pip_pkg.__version__ in co.stdout

        with capture_output() as co:
            pip('-V', silent=True)
        assert not co.stdout
        assert not co.stderr

        with capture_output() as co:
            pip('freeze')
        assert f'packaging=={packaging.__version__}' in co.stdout

    @skipUnless(not vpip('pyquery'), 'No pyquery package required.')
    def test_pip_install(self):
        try:
            pip_install(['pyquery>=1.4'], silent=True)
            assert vpip('pyquery')

            pip('uninstall', '-y', 'pyquery', silent=True)
            assert not vpip('pyquery')
        finally:
            if check_reqs(['pyquery']):
                pip('uninstall', '-y', 'pyquery', silent=True)
