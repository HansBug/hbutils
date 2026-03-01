"""
Isolation utilities for standard input streams in tests.

This module provides utilities for isolating and mocking standard input (stdin)
during testing or other scenarios where controlled input is needed. It allows
you to simulate user input by providing predefined strings or lists of strings
as stdin content. The implementation supports both in-memory and file-based
stdin simulation.

The module contains the following main components:

* :func:`isolated_stdin` - Context manager for redirecting ``stdin`` to custom input

Example::

    >>> from hbutils.testing.isolated.input import isolated_stdin
    >>> with isolated_stdin(['123', '456']):
    ...     a = int(input())
    ...     b = int(input())
    ...     print(a, b, a + b)
    123 456 579

    >>> with isolated_stdin('single line input', mem=True):
    ...     line = input()
    ...     print(f'Read: {line}')
    Read: single line input

"""
import io
import os
from contextlib import _RedirectStream, contextmanager
from typing import Iterator, List, Union, ContextManager, TextIO

from ...system import TemporaryDirectory

__all__ = [
    'isolated_stdin',
]


# noinspection PyPep8Naming
class _redirect_stdin(_RedirectStream):
    """
    A context manager for redirecting stdin stream.

    This class extends :class:`contextlib._RedirectStream` to specifically handle
    stdin redirection.

    .. note::
       This class is internal to the module and not exported in :data:`__all__`.
    """
    _stream = 'stdin'


def _to_input_text(v: Union[str, List[str]]) -> str:
    """
    Convert input value to a single text string.

    :param v: Input content, either a string or a list of strings.
    :type v: Union[str, List[str]]
    :return: A single string representing the input text.
    :rtype: str
    :raises TypeError: If the input type is neither string nor list.

    Example::

        >>> _to_input_text('hello')
        'hello'
        >>> _to_input_text(['line1', 'line2'])
        'line1\\nline2'
    """
    if isinstance(v, str):
        return v
    elif isinstance(v, list):
        return '\n'.join(v)
    else:
        raise TypeError(f'Unknown stdin type - {v!r}.')


@contextmanager
def _stdin_via_mem(v: str) -> Iterator[TextIO]:
    """
    Create a stdin stream using in-memory :class:`io.StringIO`.

    :param v: The input text content.
    :type v: str
    :return: A context manager that yields a text stream.
    :rtype: Iterator[TextIO]

    Example::

        >>> with _stdin_via_mem('test input') as f:
        ...     content = f.read()
        >>> content
        'test input'
    """
    with io.StringIO(v) as f:
        yield f


@contextmanager
def _stdin_via_file(v: str) -> Iterator[TextIO]:
    """
    Create a stdin stream using a temporary file.

    This function creates a temporary file, writes the input content to it,
    and then opens it for reading to simulate stdin.

    :param v: The input text content.
    :type v: str
    :return: A context manager that yields a text stream.
    :rtype: Iterator[TextIO]

    Example::

        >>> with _stdin_via_file('test input') as f:
        ...     content = f.read()
        >>> content
        'test input'
    """
    with TemporaryDirectory() as tdir:
        stdin_file = os.path.join(tdir, 'stdin')
        with open(stdin_file, 'w+') as inf:
            inf.write(v)

        with open(stdin_file, 'r') as f:
            yield f


@contextmanager
def isolated_stdin(v: Union[str, List[str]], mem: bool = False) -> Iterator[None]:
    """
    Isolation for stdin stream.

    This context manager allows you to mock stdin with predefined input content,
    useful for testing interactive programs or simulating user input.

    :param v: Input content, either a whole string or a list of strings.
              If a list is provided, each element will be treated as a separate line.
    :type v: Union[str, List[str]]
    :param mem: Use memory-based (StringIO) or file-based approach for stdin.
                Default is ``False`` which means a temporary file will be used as
                a fake input stream. Set to ``True`` to use in-memory
                :class:`io.StringIO` instead.
    :type mem: bool
    :return: A context manager for isolated stdin.
    :rtype: Iterator[None]

    Examples::

        >>> from hbutils.testing import isolated_stdin
        >>> with isolated_stdin(['123', '456']):
        ...     a = int(input())
        ...     b = int(input())
        ...     print(a, b, a + b)
        123 456 579

        >>> with isolated_stdin('single line input', mem=True):
        ...     line = input()
        ...     print(f'Read: {line}')
        Read: single line input
    """
    context = _stdin_via_mem if mem else _stdin_via_file
    with context(_to_input_text(v)) as f:
        with _redirect_stdin(f):
            yield
