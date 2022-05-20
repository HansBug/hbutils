from .version import _VersionModel
from ...expression import LogicalExpression, ComparableExpression
from ...expression import raw as raw_expr
from ...system import python_version, package_version, is_windows, is_linux, is_darwin, is_cpython, is_pypy, \
    is_ironpython, is_jython

__all__ = [
    'vpython', 'vpip',
    'OS', 'Impl',
]


class VersionCmpExpression(ComparableExpression, LogicalExpression):
    pass


vpython = raw_expr(_VersionModel(python_version()), cls=VersionCmpExpression)


class PipVersionCmpExpression(VersionCmpExpression):
    def __call__(self, name: str):
        return raw_expr(_VersionModel(package_version(name)), cls=VersionCmpExpression)


vpip = raw_expr(_VersionModel(package_version('pip')), cls=PipVersionCmpExpression)


class OSExpression(LogicalExpression):
    pass


class OS:
    windows = raw_expr(is_windows(), cls=OSExpression)
    linux = raw_expr(is_linux(), cls=OSExpression)
    darwin = raw_expr(is_darwin(), cls=OSExpression)
    macos = darwin


class PythonImplementExpression(LogicalExpression):
    pass


class Impl:
    cpython = raw_expr(is_cpython(), cls=PythonImplementExpression)
    iron_python = raw_expr(is_ironpython(), cls=PythonImplementExpression)
    jython = raw_expr(is_jython(), cls=PythonImplementExpression)
    pypy = raw_expr(is_pypy(), cls=PythonImplementExpression)
