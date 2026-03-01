"""
Isolated directory execution utilities for tests.

This module provides a single public context manager,
:func:`isolated_directory`, which creates a temporary working directory and
optionally populates it with a mapping of files or directories copied from the
original working directory. The context manager changes the current working
directory to the temporary location for the duration of the context and
restores it afterwards.

The main public component is:

* :func:`isolated_directory` - Execute code within an isolated temporary directory

.. note::
   This utility is typically used in tests to avoid polluting the real working
   directory and to work with a controlled file system layout.

Example::

    >>> import os
    >>> from hbutils.testing.isolated.directory import isolated_directory
    >>>
    >>> with isolated_directory():
    ...     with open('example.txt', 'w') as f:
    ...         _ = f.write('hello')
    ...     os.listdir('.')
    ['example.txt']
    >>> os.path.exists('example.txt')
    False

"""
import os
from contextlib import contextmanager
from typing import ContextManager, Dict, Optional

from ...system import copy, TemporaryDirectory

__all__ = [
    'isolated_directory',
]


@contextmanager
def isolated_directory(mapping: Optional[Dict[str, str]] = None) -> ContextManager[None]:
    """
    Execute code in an isolated temporary directory with optional mappings.

    This context manager creates a temporary directory, optionally copies the
    mapped sources into that directory, changes the working directory to the
    temporary location, and restores the original working directory when the
    context exits.

    :param mapping: Mapping of destination paths (relative to the temporary
        directory) to source paths (relative to the original working directory).
        If ``None``, the isolated directory starts empty.
    :type mapping: Optional[Dict[str, str]]
    :return: A context manager that yields control inside the isolated directory.
    :rtype: ContextManager[None]
    :raises OSError: If directory creation or working directory changes fail.
    :raises FileNotFoundError: If a source path in the mapping does not exist.
    :raises NotADirectoryError: If a copy operation expects a directory but the
        target is not a directory.

    Example::

        >>> import os
        >>> import pathlib
        >>> from hbutils.testing.isolated.directory import isolated_directory
        >>>
        >>> with isolated_directory():
        ...     with open('file.txt', 'w') as f:
        ...         print("Line 1", file=f)
        ...         print("Line 2rd", file=f)
        ...     print(os.listdir('.'))
        ...     print(pathlib.Path('file.txt').read_text())
        ['file.txt']
        Line 1
        Line 2rd

        >>> with isolated_directory({
        ...     'ts': 'hbutils/testing',
        ...     'README.md': 'README.md',
        ... }):
        ...     print(os.listdir('.'))
        ...     print(os.listdir('ts'))
        ['README.md', 'ts']
        ['capture', 'generator', 'isolated', '__init__.py']

    """
    _original_path = os.path.abspath(os.curdir)
    with TemporaryDirectory() as dirname:
        for dst, src in (mapping or {}).items():
            dst_position = os.path.join(dirname, dst)
            os.makedirs(os.path.dirname(dst_position), exist_ok=True)
            copy(
                os.path.join(_original_path, src),
                dst_position,
            )

        try:
            os.chdir(dirname)
            yield
        finally:
            os.chdir(_original_path)
