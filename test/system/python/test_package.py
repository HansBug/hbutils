from contextlib import contextmanager
from dataclasses import dataclass
from unittest import mock, skipUnless

try:
    import importlib.metadata as importlib_metadata
except (ModuleNotFoundError, ImportError):
    import importlib_metadata
import packaging
import pip as _pip_pkg
import pytest
from packaging.version import Version

from hbutils.system import package_version, load_req_file, check_reqs, check_req_file, pip, pip_install, which, \
    pip_install_req_file
from hbutils.testing import capture_output, vpip
from ...testings import get_testfile_path, normpath


@dataclass
class _VersionProxy:
    version: str


@contextmanager
def _mock_for_package_version(versions, clear=False):
    try:
        from importlib.metadata import distribution as _origin_dist
    except (ModuleNotFoundError, ImportError):
        from importlib_metadata import distribution as _origin_dist
    versions = {name.lower(): v for name, v in versions.items()}

    def _callable(name):
        if name in versions:
            return _VersionProxy(versions[name])
        else:
            if clear:
                raise importlib_metadata.PackageNotFoundError
            else:
                return _origin_dist(name)

    with mock.patch('hbutils.system.python.package.importlib_metadata.distribution', _callable):
        yield


@pytest.mark.unittest
class TestSystemPythonPackage:
    def test_package_version(self):
        assert isinstance(package_version("chardet"), Version)
        assert package_version("chardet") >= Version("3.0.4")
        assert package_version("chardet") < Version("5")
        assert package_version("This_is_an_fxxking_name") is None

        with _mock_for_package_version({'pip': '19.3.1'}):
            assert package_version('pip') == Version('19.3.1')
            assert package_version('PIP') == Version('19.3.1')
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

    @skipUnless(not vpip('where'), 'No \'where\' package required.')
    def test_pip_install(self):
        try:
            pip_install(['where>=1.0.0'], silent=True)
            assert vpip('where')

            import where  # test the usage
            assert normpath(where.first('python')) == normpath(which('python'))

            pip('uninstall', '-y', 'where', silent=True)
            assert not vpip('where')
        finally:
            if check_reqs(['where']):
                pip('uninstall', '-y', 'where', silent=True)

    @skipUnless(not vpip('where'), 'No \'where\' package required.')
    def test_pip_install_from_file(self):
        try:
            pip_install_req_file(get_testfile_path('requirements-where.txt'), silent=True)
            assert vpip('where')

            import where  # test the usage
            assert normpath(where.first('python')) == normpath(which('python'))

            pip('uninstall', '-y', 'where', silent=True)
            assert not vpip('where')
        finally:
            if check_reqs(['where']):
                pip('uninstall', '-y', 'where', silent=True)
