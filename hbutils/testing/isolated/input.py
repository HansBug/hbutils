"""
Overview:
    Isolation for stdin stream.
"""
import io
import os
from contextlib import _RedirectStream, contextmanager
from typing import List, Union, ContextManager, TextIO

from hbutils.testing._base import TemporaryDirectory

__all__ = [
    'isolated_stdin',
]


# noinspection PyPep8Naming
class _redirect_stdin(_RedirectStream):
    _stream = 'stdin'


def _to_input_text(v: Union[str, List[str]]) -> str:
    if isinstance(v, str):
        return v
    elif isinstance(v, list):
        return '\n'.join(v)
    else:
        raise TypeError(f'Unknown stdin type - {v!r}.')


@contextmanager
def _stdin_via_mem(v: str) -> ContextManager[TextIO]:
    with io.StringIO(v) as f:
        yield f


@contextmanager
def _stdin_via_file(v: str) -> ContextManager[TextIO]:
    with TemporaryDirectory() as tdir:
        stdin_file = os.path.join(tdir, 'stdin')
        with open(stdin_file, 'w+') as inf:
            inf.write(v)

        with open(stdin_file, 'r') as f:
            yield f


@contextmanager
def isolated_stdin(v: Union[str, List[str]], mem: bool = False):
    """
    Overview:
        Isolation for stdin stream.

    :param v: Input content, a whole string or a list of string supported.
    :param mem: Use memory or not. Default is ``False`` which means \
        a temporary file will be used as fake input stream.

    Examples::
        >>> from hbutils.testing import isolated_stdin
        >>> with isolated_stdin(['123', '456']):
        ...     a = int(input())
        ...     b = int(input())
        ...     print(a, b, a + b)
        123 456 579
    """
    context = _stdin_via_mem if mem else _stdin_via_file
    with context(_to_input_text(v)) as f:
        with _redirect_stdin(f):
            yield
