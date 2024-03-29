import unittest
from contextlib import contextmanager
from dataclasses import dataclass
from unittest import mock

from packaging.utils import canonicalize_name

try:
    import importlib.metadata as importlib_metadata
except (ModuleNotFoundError, ImportError):
    import importlib_metadata
import pytest
from easydict import EasyDict

from hbutils.testing import vpip, disable_output


@dataclass
class _VersionProxy:
    version: str


@contextmanager
def _mock_for_package_version(versions, clear=False):
    try:
        from importlib.metadata import distribution as _origin_dist
    except (ModuleNotFoundError, ImportError):
        from importlib_metadata import distribution as _origin_dist
    versions = {canonicalize_name(name): v for name, v in versions.items()}

    def _callable(name):
        name = canonicalize_name(name)
        if name in versions:
            if versions[name]:
                return _VersionProxy(versions[name])
            else:
                raise importlib_metadata.PackageNotFoundError
        else:
            if clear:
                raise importlib_metadata.PackageNotFoundError
            else:
                return _origin_dist(name)

    with mock.patch('hbutils.system.python.package.importlib_metadata.distribution', _callable):
        yield


def _get_test_class():
    @pytest.mark.ignore
    class _TestPythonPackage(unittest.TestCase):
        # noinspection PyPep8Naming
        def __init__(self, methodName: str, v):
            unittest.TestCase.__init__(self, methodName)
            self.v = v

        @unittest.skipUnless(20 <= vpip < 21, 'pip20 only')
        def test_pip20(self):
            self.v.is_pip20 = True

        @unittest.skipUnless(vpip('setuptools') >= '45' and (vpip('click') < 7 or not vpip), 'complex only')
        def test_complex(self):
            self.v.complex_ok = True

    return _TestPythonPackage


@pytest.mark.unittest
class TestTestingRequiresPackage:
    def test_simple_1(self):
        d = EasyDict({})
        with disable_output(), _mock_for_package_version({'pip': '19.3.1'}, clear=True):
            _TestPythonPackage = _get_test_class()
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonPackage('test_pip20', d))
            runner.run(_TestPythonPackage('test_complex', d))

        assert d == {}

    def test_simple_2(self):
        d = EasyDict({})

        with disable_output(), \
                _mock_for_package_version({'pip': '20.3.1'}, clear=True):
            _TestPythonPackage = _get_test_class()
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonPackage('test_pip20', d))
            runner.run(_TestPythonPackage('test_complex', d))

        assert d == {'is_pip20': True}

    def test_simple_3(self):
        d = EasyDict({})
        with disable_output(), \
                _mock_for_package_version({'pip': '20.3.1', 'setuptools': '46.1.7', 'click': '6.4.2'}, clear=True):
            _TestPythonPackage = _get_test_class()
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonPackage('test_pip20', d))
            runner.run(_TestPythonPackage('test_complex', d))

        assert d == {'is_pip20': True, 'complex_ok': True}

    def test_simple_4(self):
        d = EasyDict({})
        with disable_output(), \
                _mock_for_package_version({'pip': '19.3.1', 'setuptools': '46.1.7', 'click': '6.4.2'}, clear=True):
            _TestPythonPackage = _get_test_class()
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonPackage('test_pip20', d))
            runner.run(_TestPythonPackage('test_complex', d))

        assert d == {'complex_ok': True}

    def test_simple_5(self):
        d = EasyDict({})
        with disable_output(), \
                _mock_for_package_version({'setuptools': '46.1.7', 'click': '7.4.2'}, clear=True):
            _TestPythonPackage = _get_test_class()
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonPackage('test_pip20', d))
            runner.run(_TestPythonPackage('test_complex', d))

        assert d == {'complex_ok': True}
