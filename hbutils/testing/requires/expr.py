from .version import VersionInfo
from ...expression import LogicalExpression, ComparableExpression, expr
from ...system import python_version, package_version, is_windows, is_linux, is_darwin, is_cpython, is_pypy, \
    is_ironpython, is_jython

__all__ = [
    'vpython', 'vpip',
    'OS', 'Impl',
]


class VersionCmpExpression(ComparableExpression, LogicalExpression):
    pass


vpython = expr(lambda x: VersionInfo(python_version()), cls=VersionCmpExpression)


class PipVersionCmpExpression(VersionCmpExpression):
    def __call__(self, name: str):
        return expr(lambda x: VersionInfo(package_version(name)), cls=VersionCmpExpression)


vpip = expr(lambda x: VersionInfo(package_version('pip')), cls=PipVersionCmpExpression)


class OSExpression(LogicalExpression):
    pass


class OS:
    windows = expr(lambda x: is_windows(), cls=OSExpression)
    linux = expr(lambda x: is_linux(), cls=OSExpression)
    darwin = expr(lambda x: is_darwin(), cls=OSExpression)
    macos = darwin


class PythonImplementExpression(LogicalExpression):
    pass


class Impl:
    cpython = expr(lambda x: is_cpython(), cls=PythonImplementExpression)
    iron_python = expr(lambda x: is_ironpython(), cls=PythonImplementExpression)
    jython = expr(lambda x: is_jython(), cls=PythonImplementExpression)
    pypy = expr(lambda x: is_pypy(), cls=PythonImplementExpression)
