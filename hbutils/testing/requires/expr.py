"""
Environment and version expressions for conditional testing.

This module provides utilities for expressing runtime requirements in a
comparison-friendly form. The exported objects are intended for use with
``unittest.skipUnless`` or other conditional execution mechanisms. It includes
version expressions for the Python interpreter and pip or third-party packages,
along with boolean indicators for the current operating system and Python
implementation.

The module contains the following main components:

* :data:`vpython` - Version expression bound to the current Python interpreter
* :data:`vpip` - Version expression bound to pip and package versions
* :class:`OS` - Operating system detection attributes
* :class:`Impl` - Python implementation detection attributes

Example::

    >>> import unittest
    >>> from hbutils.testing import vpython, vpip, OS, Impl
    >>>
    >>> class TestMyCase(unittest.TestCase):
    ...     @unittest.skipUnless('3.8' <= vpython, 'Python 3.8+ only')
    ...     def test_python_version(self):
    ...         assert True
    ...
    ...     @unittest.skipUnless(vpip >= '21', 'pip 21+ only')
    ...     def test_pip_version(self):
    ...         assert True
    ...
    ...     @unittest.skipUnless(OS.linux and Impl.cpython, 'CPython on Linux only')
    ...     def test_runtime(self):
    ...         assert True

.. note::
   All version expressions are dynamic and read the current environment when
   compared or evaluated.

"""

from abc import ABCMeta

from .version import VersionInfo
from ...system import python_version, package_version, is_windows, is_linux, is_darwin, is_cpython, is_pypy, \
    is_ironpython, is_jython

__all__ = [
    'vpython', 'vpip',
    'OS', 'Impl',
]

vpython: VersionInfo = VersionInfo(lambda: python_version())
vpython.__doc__ = """
Python version expression.

This object represents the current Python interpreter version and supports
comparison operations against version strings, tuples, or integers.

Examples::

    >>> import platform
    >>> import unittest
    >>> from hbutils.testing import vpython
    >>>
    >>> class TestMyCase(unittest.TestCase):  # on Python 3.6
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
    """
    Version expression for pip and installed packages.

    This class extends :class:`~hbutils.testing.requires.version.VersionInfo`
    to provide version expressions for arbitrary installed packages. The
    base instance is bound to the current ``pip`` version, while calling the
    instance returns a version expression for another package name.
    """

    def __call__(self, name: str) -> VersionInfo:
        """
        Get version information for a specific package.

        :param name: The name of the package to check.
        :type name: str
        :return: A :class:`~hbutils.testing.requires.version.VersionInfo` object
            for the specified package.
        :rtype: VersionInfo

        Example::

            >>> from hbutils.testing import vpip
            >>> vpip('setuptools')  # Get setuptools version info
            <VersionInfo ...>
        """
        return VersionInfo(lambda: package_version(name))


vpip: PipVersionInfo = PipVersionInfo(lambda: package_version('pip'))
vpip.__doc__ = """
Pip and package version expression.

This object represents the current ``pip`` version and supports comparisons.
Calling the object with a package name returns a version expression for that
package.

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
    Operating system detection expressions.

    The attributes of this class are boolean values evaluated at import time,
    indicating the current operating system.

    :cvar windows: Whether the current OS is Windows.
    :vartype windows: bool
    :cvar linux: Whether the current OS is Linux.
    :vartype linux: bool
    :cvar darwin: Whether the current OS is macOS (Darwin).
    :vartype darwin: bool
    :cvar macos: Alias for :attr:`darwin`.
    :vartype macos: bool

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
    windows: bool = is_windows()
    """
    Whether the current operating system is Windows.
    """

    linux: bool = is_linux()
    """
    Whether the current operating system is Linux.
    """

    darwin: bool = is_darwin()
    """
    Whether the current operating system is Darwin (macOS).
    """
    macos: bool = darwin
    """
    Alias for :attr:`OS.darwin`.
    """


class Impl:
    """
    Python implementation detection expressions.

    The attributes of this class are boolean values evaluated at import time,
    indicating the current Python implementation. See
    `platform.python_implementation()
    <https://docs.python.org/3/library/platform.html#platform.python_implementation>`_
    for details.

    :cvar cpython: Whether the current implementation is CPython.
    :vartype cpython: bool
    :cvar iron_python: Whether the current implementation is IronPython.
    :vartype iron_python: bool
    :cvar jython: Whether the current implementation is Jython.
    :vartype jython: bool
    :cvar pypy: Whether the current implementation is PyPy.
    :vartype pypy: bool

    Examples::

        >>> import unittest
        >>> from hbutils.testing import Impl
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
    cpython: bool = is_cpython()
    """
    Whether the current Python implementation is CPython.
    """

    iron_python: bool = is_ironpython()
    """
    Whether the current Python implementation is IronPython.
    """

    jython: bool = is_jython()
    """
    Whether the current Python implementation is Jython.
    """

    pypy: bool = is_pypy()
    """
    Whether the current Python implementation is PyPy.
    """
