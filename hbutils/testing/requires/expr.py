from abc import ABCMeta

from .version import VersionInfo
from ...expression import LogicalExpression, ComparableExpression, expr
from ...system import python_version, package_version, is_windows, is_linux, is_darwin, is_cpython, is_pypy, \
    is_ironpython, is_jython

__all__ = [
    'vpython', 'vpip',
    'OS', 'Impl',
]


class VersionCmpExpression(ComparableExpression, LogicalExpression):
    """
    """
    pass


vpython = expr(lambda x: VersionInfo(python_version()), cls=VersionCmpExpression)
vpython.__doc__ = """
Overview:
    Python version expression.

Examples::
    >>> import platform
    >>> import unittest
    >>> from hbutils.testing import pre_condition, vpython
    >>> 
    >>> class TestMyCase(unittest.TestCase):  # on python 3.6
    ...     def test_anytime(self):
    ...         assert 2 + 1 == 3
    ...
    ...     @pre_condition((vpython >= '3.6') & (vpython < '3.7'))  # will run
    ...     def test_on_python36(self):
    ...         assert platform.python_version_tuple()[:2] == ('3', '6')
    ...
    ...     @pre_condition((vpython >= '3.7') & (vpython < '3.8'))  # will skip
    ...     def test_on_python37(self):
    ...         assert platform.python_version_tuple()[:2] == ('3', '7') 
    ...
    >>> unittest.main()
    ..s
    ----------------------------------------------------------------------
    Ran 3 tests in 0.000s
    OK (skipped=1)
"""


class PipVersionCmpExpression(VersionCmpExpression):
    def __call__(self, name: str):
        return expr(lambda x: VersionInfo(package_version(name)), cls=VersionCmpExpression)


vpip = expr(lambda x: VersionInfo(package_version('pip')), cls=PipVersionCmpExpression)
vpip.__doc__ = """
Overview:
    Pip version expression

Examples::
    >>> import unittest
    >>> from hbutils.testing import pre_condition, vpip
    >>> 
    >>> class TestMyCase(unittest.TestCase):
    ...     def test_1_anytime(self):
    ...         assert 2 + 1 == 3
    ...
    ...     @pre_condition(vpip >= '21')  # pip>=21
    ...     def test_2_on_pip21plus(self):
    ...         assert True
    ...
    ...     @pre_condition(vpip('pip') >= '21')  # the same as above
    ...     def test_3_on_pip21plus2(self):
    ...         assert True
    ...
    ...     @pre_condition((vpip('setuptools') >= '45') | (vpip('build') >= '0.8'))  # setuptools>=45 or build>=0.8
    ...     def test_4_on_setuptools_or_build(self):
    ...         assert True
    ...
    ...     @pre_condition(~vpip & (vpip('build') >= '0.8'))  # pip not installed, and build>=0.8
    ...     def test_5_on_nopip_and_build(self):
    ...         assert True
    ... 
    >>> unittest.main()
    ....s
    ----------------------------------------------------------------------
    Ran 5 tests in 0.000s
    OK (skipped=1)
"""


class OSExpression(LogicalExpression):
    pass


class OS(metaclass=ABCMeta):
    """
    Overview:
        Expressions for operating system.

    Examples::
        >>> import unittest
        >>> from hbutils.testing import pre_condition, OS
        >>>
        >>> class TestMyCase(unittest.TestCase):  # on Linux
        ...     def test_1_anytime(self):
        ...         assert 2 + 1 == 3
        ...
        ...     @pre_condition(OS.linux)  # only run on Linux
        ...     def test_2_linux(self):
        ...         assert True
        ...
        ...     @pre_condition(OS.windows)  # only run on Windows
        ...     def test_2_windows(self):
        ...         assert True
        ...
        ...     @pre_condition(OS.macos)  # only run on macOS
        ...     def test_4_macos(self):
        ...         assert True
        ...
        >>> unittest.main()
        ..ss
        ----------------------------------------------------------------------
        Ran 4 tests in 0.001s
        OK (skipped=2)
    """
    windows = expr(lambda x: is_windows(), cls=OSExpression)
    """
    Expression for windows system.
    """

    linux = expr(lambda x: is_linux(), cls=OSExpression)
    """
    Expression for linux system.
    """

    darwin = expr(lambda x: is_darwin(), cls=OSExpression)
    """
    Expression for darwin system (also named ``OS.macos``).
    """
    macos = darwin
    """
    Alias for ``OS.darwin``.
    """


class PythonImplementExpression(LogicalExpression):
    pass


class Impl:
    """
    Overview:
        Expression for python implementation.
        See `platform.python_implementation() \
        <https://docs.python.org/3/library/platform.html#platform.python_implementation>`_ .

    Examples::
        >>> import unittest
        >>> from hbutils.testing import pre_condition, Impl
        >>>
        >>> class TestMyCase(unittest.TestCase):  # on CPython
        ...     def test_1_anytime(self):
        ...         assert 2 + 1 == 3
        ...
        ...     @pre_condition(Impl.cpython)  # only run on CPython
        ...     def test_2_cpython(self):
        ...         assert True
        ...
        ...     @pre_condition(Impl.pypy)  # only run on PyPy
        ...     def test_3_pypy(self):
        ...         assert True
        ...
        ...     @pre_condition(Impl.iron_python)  # only run on IronPython
        ...     def test_4_ironpython(self):
        ...         assert True
        ...
        ...     @pre_condition(Impl.jython)  # only run on Jython
        ...     def test_5_jython(self):
        ...         assert True
        ...
        >>> unittest.main()
        ..sss
        ----------------------------------------------------------------------
        Ran 5 tests in 0.000s
        OK (skipped=3)
    """
    cpython = expr(lambda x: is_cpython(), cls=PythonImplementExpression)
    """
    Expression for CPython (most-frequently-used python).
    """

    iron_python = expr(lambda x: is_ironpython(), cls=PythonImplementExpression)
    """
    Expression for IronPython.
    """

    jython = expr(lambda x: is_jython(), cls=PythonImplementExpression)
    """
    Expression for Jython (java-based python).
    """

    pypy = expr(lambda x: is_pypy(), cls=PythonImplementExpression)
    """
    Expression for PyPy.
    """
