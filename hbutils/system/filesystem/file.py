"""
Overview:
    This module provides functions for file processing, including creating files and performing glob operations.
"""

import glob as gb
import os
import pathlib
from typing import Iterator

__all__ = [
    'touch', 'glob',
]


def touch(file: str, exist_ok: bool = True, makedirs: bool = True):
    """
    Create a file at the specified path, similar to the Unix 'touch' command.

    This function creates an empty file at the given path. If the file already exists,
    it updates the file's access and modification times. It can also create necessary
    parent directories if they don't exist.

    :param file: Path of the file to be created or updated.
    :type file: str
    :param exist_ok: If True, don't raise an error if the file already exists. Default is True.
    :type exist_ok: bool
    :param makedirs: If True, create parent directories when necessary. Default is True.
    :type makedirs: bool

    :raises FileExistsError: If the file already exists and exist_ok is False.
    :raises OSError: If there's an error creating the file or directories.

    .. note::
        This function mimics the behavior of the 'touch' command in Unix systems.

    Examples:
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


def glob(*items) -> Iterator[str]:
    """
    Perform glob operations on the given patterns and return an iterator of matching file paths.

    This function allows for flexible file matching using wildcard patterns. It can handle
    multiple patterns and performs recursive matching by default.

    :param items: One or more glob patterns to match against file paths.
    :type items: str

    :return: An iterator yielding paths of files that match the given patterns.
    :rtype: Iterator[str]

    .. note::
        This function differs from the native `glob.glob` in that it returns a generator
        instead of a list, which can be more memory-efficient for large directory structures.

    Examples:
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
