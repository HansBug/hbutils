import os

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
