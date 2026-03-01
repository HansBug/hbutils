"""
File system utilities for creating files and performing glob-based searches.

This module provides lightweight helpers that wrap common filesystem operations,
including file creation (similar to the Unix ``touch`` command) and pattern-based
file discovery using glob expressions.

The module contains the following public components:

* :func:`touch` - Create or update files, optionally creating parent directories.
* :func:`glob` - Iterate over file paths that match one or more glob patterns.

.. note::
   The :func:`glob` helper yields results as a generator, which is more
   memory-efficient than :func:`glob.glob` for large result sets.

Example::

    >>> from hbutils.system.filesystem.file import touch, glob
    >>> touch('data/output.txt')
    >>> list(glob('data/*.txt'))
    ['data/output.txt']
"""
import glob as gb
import os
import pathlib
from typing import Iterator

__all__ = [
    'touch', 'glob',
]


def touch(file: str, exist_ok: bool = True, makedirs: bool = True) -> None:
    """
    Touch the file at given path.

    This function creates an empty file if it does not exist, or updates its
    modification time if it does. It can also create parent directories
    automatically.

    :param file: Path of the file to create or update.
    :type file: str
    :param exist_ok: If True, do not raise an error if the file already exists.
    :type exist_ok: bool
    :param makedirs: If True, create parent directories as needed.
    :type makedirs: bool
    :return: This function returns ``None``.
    :rtype: None

    .. note::
       You can use this like the Unix ``touch`` command.

    Example::

        >>> import os
        >>> from hbutils.system import touch
        >>> os.listdir('.')
        []
        >>> touch('simple.txt')  # touch simple file
        >>> touch('1/2/3/simple.txt')  # touch file in nested directory (1/2/3 will be created)
        >>> os.listdir('.')
        ['1', 'simple.txt']
        >>> os.listdir('1/2/3')
        ['simple.txt']
    """
    if makedirs:
        path, _ = os.path.split(file)
        if path:
            os.makedirs(path, exist_ok=exist_ok)
    pathlib.Path(file).touch(exist_ok=exist_ok)


def glob(*items: str) -> Iterator[str]:
    """
    Glob filter by the given ``items``.

    This function performs pattern matching on file paths using glob patterns.
    Unlike the native :func:`glob.glob`, this function returns a generator that
    yields matching paths, making it more memory-efficient for large result sets.

    :param items: One or more glob patterns to match against file paths.
    :type items: str
    :return: Generator yielding paths that match any of the provided patterns.
    :rtype: Iterator[str]

    .. note::
       :func:`glob` is different from native :func:`glob.glob`, for its return
       value is a generator instead of a list.

    Example::

        >>> from hbutils.system import glob
        >>>
        >>> list(glob('*.md'))  # simple filter
        ['CONTRIBUTING.md', 'README.md']
        >>> list(glob('*.md', '*.txt'))  # multiple filter
        ['CONTRIBUTING.md', 'README.md', 'requirements-test.txt', 'requirements-doc.txt', 'requirements.txt']
        >>> print(*glob('hbutils/system/**/*.py'), sep='\\n')  # nested filter
        hbutils/system/__init__.py
        hbutils/system/filesystem/directory.py
        hbutils/system/filesystem/file.py
        hbutils/system/filesystem/__init__.py
        hbutils/system/python/package.py
        hbutils/system/python/implementation.py
        hbutils/system/python/version.py
        hbutils/system/python/__init__.py
        hbutils/system/os/type.py
        hbutils/system/os/__init__.py
    """
    for item in items:
        yield from gb.glob(item, recursive=True)
