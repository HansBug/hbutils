import unittest

import pytest
from easydict import EasyDict

from hbutils.testing import vpython, disable_output, Impl
from ...testings import py36_mark, py37_mark, py38_mark, py39_mark, py310_mark, pypy_mark, cpython_mark


@pytest.mark.ignore
class _TestPythonVersion(unittest.TestCase):
    # noinspection PyPep8Naming
    def __init__(self, methodName: str, v):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.v = v

    @unittest.skipUnless('3.6' <= vpython < '3.7', 'py36 only')
    def test_py36(self):
        self.v.is_py36 = True

    @unittest.skipUnless('3.7' <= vpython < '3.8', 'py37 only')
    def test_py37(self):
        self.v.is_py37 = True

    @unittest.skipUnless('3.8' <= vpython < '3.9', 'py38 only')
    def test_py38(self):
        self.v.is_py38 = True

    @unittest.skipUnless('3.9' <= vpython < '3.10', 'py39 only')
    def test_py39(self):
        self.v.is_py39 = True

    @unittest.skipUnless('3.10' <= vpython < '3.11', 'py310 only')
    def test_py310(self):
        self.v.is_py310 = True


@pytest.mark.ignore
class _TestPythonImplement(unittest.TestCase):
    # noinspection PyPep8Naming
    def __init__(self, methodName: str, v):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.v = v

    @unittest.skipUnless(Impl.cpython, 'cpython only')
    def test_cpython(self):
        self.v.is_cpython = True

    @unittest.skipUnless(Impl.pypy, 'pypy only')
    def test_pypy(self):
        self.v.is_pypy = True


# noinspection DuplicatedCode
class TestTestingsRequiresPython:
    @py36_mark
    def test_py36(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonVersion('test_py36', d))
            runner.run(_TestPythonVersion('test_py37', d))
            runner.run(_TestPythonVersion('test_py38', d))
            runner.run(_TestPythonVersion('test_py39', d))
            runner.run(_TestPythonVersion('test_py310', d))

        assert d == {'is_py36': True}

    @py37_mark
    def test_py37(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonVersion('test_py36', d))
            runner.run(_TestPythonVersion('test_py37', d))
            runner.run(_TestPythonVersion('test_py38', d))
            runner.run(_TestPythonVersion('test_py39', d))
            runner.run(_TestPythonVersion('test_py310', d))

        assert d == {'is_py37': True}

    @py38_mark
    def test_py38(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonVersion('test_py36', d))
            runner.run(_TestPythonVersion('test_py37', d))
            runner.run(_TestPythonVersion('test_py38', d))
            runner.run(_TestPythonVersion('test_py39', d))
            runner.run(_TestPythonVersion('test_py310', d))

        assert d == {'is_py38': True}

    @py39_mark
    def test_py39(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonVersion('test_py36', d))
            runner.run(_TestPythonVersion('test_py37', d))
            runner.run(_TestPythonVersion('test_py38', d))
            runner.run(_TestPythonVersion('test_py39', d))
            runner.run(_TestPythonVersion('test_py310', d))

        assert d == {'is_py39': True}

    @py310_mark
    def test_py310(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonVersion('test_py36', d))
            runner.run(_TestPythonVersion('test_py37', d))
            runner.run(_TestPythonVersion('test_py38', d))
            runner.run(_TestPythonVersion('test_py39', d))
            runner.run(_TestPythonVersion('test_py310', d))

        assert d == {'is_py310': True}

    @cpython_mark
    def test_cpython(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonImplement('test_cpython', d))
            runner.run(_TestPythonImplement('test_pypy', d))

        assert d == {'is_cpython': True}

    @pypy_mark
    def test_pypy(self):
        d = EasyDict({})
        with disable_output():
            runner = unittest.TextTestRunner()
            runner.run(_TestPythonImplement('test_cpython', d))
            runner.run(_TestPythonImplement('test_pypy', d))

        assert d == {'is_pypy': True}
