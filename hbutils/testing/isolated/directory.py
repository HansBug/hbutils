"""
Overview:
    Isolation for directory.
"""
import os
from contextlib import contextmanager
from typing import ContextManager, Dict, Optional

from .._base import TemporaryDirectory
from ...system import copy

__all__ = [
    'isolated_directory',
]


@contextmanager
def isolated_directory(mapping: Optional[Dict[str, str]] = None) -> ContextManager:
    """
    Overview:
        Do something in an isolated directory.

    :param mapping: Mappings for the isolated directory.

    Examples::
        - Simple usage

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


        - Mapping files and directory inside

        >>> import os
        >>> from hbutils.testing import isolated_directory
        >>>
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
