import os
import platform

import pytest

_is_win = bool(os.environ.get('IS_WIN', None))
_is_macos = bool(os.environ.get('IS_MAC', None))
_is_linux = not _is_macos and not _is_win

windows_mark = pytest.mark.unittest if _is_win else pytest.mark.ignore
macos_mark = pytest.mark.unittest if _is_macos else pytest.mark.ignore
linux_mark = pytest.mark.unittest if _is_linux else pytest.mark.ignore

_is_pypy = bool(os.environ.get('IS_PYPY', None))
_is_cpython = not _is_pypy

pypy_mark = pytest.mark.unittest if _is_pypy else pytest.mark.ignore
cpython_mark = pytest.mark.unittest if _is_cpython else pytest.mark.ignore

vpy_tuple = platform.python_version_tuple()
_is_py36 = vpy_tuple[:2] == ('3', '6')
_is_py37 = vpy_tuple[:2] == ('3', '7')
_is_py38 = vpy_tuple[:2] == ('3', '8')
_is_py39 = vpy_tuple[:2] == ('3', '9')
_is_py310 = vpy_tuple[:2] == ('3', '10')

py36_mark = pytest.mark.unittest if _is_py36 else pytest.mark.ignore
py37_mark = pytest.mark.unittest if _is_py37 else pytest.mark.ignore
py38_mark = pytest.mark.unittest if _is_py38 else pytest.mark.ignore
py39_mark = pytest.mark.unittest if _is_py39 else pytest.mark.ignore
py310_mark = pytest.mark.unittest if _is_py310 else pytest.mark.ignore
