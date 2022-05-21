from abc import ABCMeta

from .version import VersionInfo
from ...system import python_version, package_version, is_windows, is_linux, is_darwin, is_cpython, is_pypy, \
    is_ironpython, is_jython

__all__ = [
    'vpython', 'vpip',
    'OS', 'Impl',
]

vpython = VersionInfo(lambda: python_version())
vpython.__doc__ = """
Overview:
    Python version expression.

Examples::
    >>> import platform
    >>> import unittest
    >>> from hbutils.testing import vpython
    >>> 
    >>> class TestMyCase(unittest.TestCase):  # on python 3.6
    ...     def test_anytime(self):
    ...         assert 2 + 1 == 3
    ...
    ...     @unittest.skipUnless('3.6' <= vpython < '3.7', 'py36 only')  # will run
    ...     def test_on_python36(self):
    ...         assert platform.python_version_tuple()[:2] == ('3', '6')
    ...
    ...     @unittest.skipUnless('3.7' <= vpython < '3.8', 'py37 only')  # will skip
    ...     def test_on_python37(self):
    ...         assert platform.python_version_tuple()[:2] == ('3', '7')
    ...
    >>> unittest.main()
    ..s
    ----------------------------------------------------------------------
    Ran 3 tests in 0.000s
    OK (skipped=1)
"""


class PipVersionInfo(VersionInfo):
    def __call__(self, name: str) -> VersionInfo:
        return VersionInfo(lambda: package_version(name))


vpip = PipVersionInfo(lambda: package_version('pip'))
vpip.__doc__ = """
Overview:
    Pip version expression

Examples::
    >>> import unittest
    >>> from hbutils.testing import vpip
    >>> 
    >>> class TestMyCase(unittest.TestCase):
    ...     def test_1_anytime(self):
    ...         assert 2 + 1 == 3
    ...
    ...     @unittest.skipUnless(vpip >= '21', 'pip21+ only')  # pip>=21
    ...     def test_2_on_pip21plus(self):
    ...         assert True
    ...
    ...     @unittest.skipUnless(vpip('pip') >= '21', 'pip21+ only')  # the same as above
    ...     def test_3_on_pip21plus2(self):
    ...         assert True
    ...
    ...     @unittest.skipUnless(vpip('setuptools') >= '45' or vpip('build') >= '0.8', '')  # setuptools>=45 or build>=0.8
    ...     def test_4_on_setuptools_or_build(self):
    ...         assert True
    ...
    ...     @unittest.skipUnless(not vpip and vpip('build') >= '0.8', '')  # pip not installed, and build>=0.8
    ...     def test_5_on_nopip_and_build(self):
    ...         assert True
    ... 
    >>> unittest.main()
    ....s
    ----------------------------------------------------------------------
    Ran 5 tests in 0.000s
    OK (skipped=1)
"""


class OS(metaclass=ABCMeta):
    """
    Overview:
        Expressions for operating system.

    Examples::
        >>> import unittest
        >>> from hbutils.testing import OS
        >>>
        >>> class TestMyCase(unittest.TestCase):  # on Linux
        ...     def test_1_anytime(self):
        ...         assert 2 + 1 == 3
        ...
        ...     @unittest.skipUnless(OS.linux, 'linux only')  # only run on Linux
        ...     def test_2_linux(self):
        ...         assert True
        ...
        ...     @unittest.skipUnless(OS.windows, 'windows only')  # only run on Windows
        ...     def test_2_windows(self):
        ...         assert True
        ...
        ...     @unittest.skipUnless(OS.macos, 'macos only')  # only run on macOS
        ...     def test_4_macos(self):
        ...         assert True
        ...
        >>> unittest.main()
        ..ss
        ----------------------------------------------------------------------
        Ran 4 tests in 0.001s
        OK (skipped=2)
    """
    windows = is_windows()
    """
    Is windows system or not, related to your local OS.
    """

    linux = is_linux()
    """
    Is linux system or not, related to your local OS.
    """

    darwin = is_darwin()
    """
    Is darwin (macos) system or not, related to your local OS.
    """
    macos = darwin
    """
    Alias for ``OS.darwin``.
    """


class Impl:
    """
    Overview:
        Expression for python implementation.
        See `platform.python_implementation() \
        <https://docs.python.org/3/library/platform.html#platform.python_implementation>`_ .

    Examples::
        >>> import unittest

from hbutils.testing import Impl
        >>>
        >>> class TestMyCase(unittest.TestCase):  # on CPython
        ...     def test_1_anytime(self):
        ...         assert 2 + 1 == 3
        ...
        ...     @unittest.skipUnless(Impl.cpython, 'cpython only')  # only run on CPython
        ...     def test_2_cpython(self):
        ...         assert True
        ...
        ...     @unittest.skipUnless(Impl.pypy, 'pypy only')  # only run on PyPy
        ...     def test_3_pypy(self):
        ...         assert True
        ...
        ...     @unittest.skipUnless(Impl.iron_python, 'ironpython only')  # only run on IronPython
        ...     def test_4_ironpython(self):
        ...         assert True
        ...
        ...     @unittest.skipUnless(Impl.jython, 'jython only')  # only run on Jython
        ...     def test_5_jython(self):
        ...         assert True
        ...
        >>> unittest.main()
        ..sss
        ----------------------------------------------------------------------
        Ran 5 tests in 0.000s
        OK (skipped=3)
    """
    cpython = is_cpython()
    """
    Is CPython (most-frequently-used python) or not, related to your local python.
    """

    iron_python = is_ironpython()
    """
    Is IronPython or not, related to your local python.
    """

    jython = is_jython()
    """
    Is Jython (java-based python) or not, related to your local python.
    """

    pypy = is_pypy()
    """
    Is PyPy or not, related to your local python.
    """
