"""
Overview:
    Isolation for directory. This module provides functionality to execute code in an isolated
    temporary directory with optional file/directory mappings from the original location.
"""
import os
from contextlib import contextmanager
from typing import ContextManager, Dict, Optional

from ...system import copy, TemporaryDirectory

__all__ = [
    'isolated_directory',
]


@contextmanager
def isolated_directory(mapping: Optional[Dict[str, str]] = None) -> ContextManager:
    """
    Execute code in an isolated temporary directory with optional file/directory mappings.
    
    This context manager creates a temporary directory, optionally copies specified files
    or directories into it based on the provided mapping, changes the working directory
    to the temporary location, and automatically cleans up and restores the original
    working directory when done.

    :param mapping: Dictionary mapping destination paths (relative to the isolated directory)
                   to source paths (relative to the current directory). If None, creates
                   an empty isolated directory.
    :type mapping: Optional[Dict[str, str]]
    
    :return: A context manager that yields control in the isolated directory.
    :rtype: ContextManager
    
    :raises OSError: If directory operations fail (e.g., permission issues).
    :raises FileNotFoundError: If a source path in the mapping does not exist.

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
