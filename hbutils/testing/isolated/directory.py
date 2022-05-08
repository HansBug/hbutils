"""
Overview:
    Isolation for directory.
"""
import os
import tempfile
from contextlib import contextmanager
from typing import ContextManager

__all__ = [
    'isolated_directory',
]


@contextmanager
def isolated_directory() -> ContextManager:
    """
    Overview:
        Do something in an isolated directory.

    Examples::
        >>> import os
        >>> import pathlib
        >>> from hbutils.testing import isolated_directory
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
        >>> print(os.listdir('.'))
        ['hbutils', 'README.md', 'requirements.txt', ...]

    """
    _original_path = os.path.abspath(os.curdir)
    with tempfile.TemporaryDirectory() as dirname:
        try:
            os.chdir(dirname)
            yield
        finally:
            os.chdir(_original_path)
