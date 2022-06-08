"""
Overview:
    Functions for file processing.
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
    Overview:
        Touch the file at given path.
        Just like the ``touch`` command in unix system.

    :param file: Path of the file.
    :param exist_ok: Exist is okay or not.
    :param makedirs: Create directories when necessary.

    .. note::
        You can use this like ``touch`` command on unix.

    Examples::
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
    Overview:
        Glob filter by the given ``items``.

    :param items: Filter items.
    :return: Filtered existing paths.

    .. note::
        :func:`glob` is different from native ``glob.glob``, for its return value is a generator instead of list.

    Examples::
        >>> from hbutils.system import glob
        >>>
        >>> list(glob('*.md'))  # simple filter
        ['CONTRIBUTING.md', 'README.md']
        >>> list(glob('*.md', '*.txt'))  # multiple filter
        ['CONTRIBUTING.md', 'README.md', 'requirements-test.txt', 'requirements-doc.txt', 'requirements.txt']
        >>> print(*glob('hbutils/system/**/*.py'), sep=\'\\n\')  # nested filter
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
