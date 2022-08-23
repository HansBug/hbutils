"""
Overview:
    Isolation for directory.
"""
import os
import shutil
import tempfile
import warnings
import weakref
from contextlib import contextmanager
from typing import ContextManager, Dict, Optional

from ...system import copy

__all__ = [
    'isolated_directory',
]


class TemporaryDirectory(object):  # pragma: no cover
    """
    THIS CLASS IS COPIED FROM PYTHON3.8's TEMPFILE.
    Because PermissionError will be raised when use native TemporaryDirectory on Windows python3.7.
    This class should be removed when python3.7 is no longer supported.

    Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.
    """

    def __init__(self, suffix=None, prefix=None, dir=None):
        self.name = tempfile.mkdtemp(suffix, prefix, dir)
        self._finalizer = weakref.finalize(
            self, self._cleanup, self.name,
            warn_message="Implicitly cleaning up {!r}".format(self))

    @classmethod
    def _rmtree(cls, name):
        def onerror(func, path, exc_info):
            if issubclass(exc_info[0], PermissionError):
                def resetperms(path):
                    try:
                        os.chflags(path, 0)
                    except AttributeError:
                        pass
                    os.chmod(path, 0o700)

                try:
                    if path != name:
                        resetperms(os.path.dirname(path))
                    resetperms(path)

                    try:
                        os.unlink(path)
                    # PermissionError is raised on FreeBSD for directories
                    except (IsADirectoryError, PermissionError):
                        cls._rmtree(path)
                except FileNotFoundError:
                    pass
            elif issubclass(exc_info[0], FileNotFoundError):
                pass
            else:
                raise

        shutil.rmtree(name, onerror=onerror)

    @classmethod
    def _cleanup(cls, name, warn_message):
        cls._rmtree(name)
        warnings.warn(warn_message, ResourceWarning)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def cleanup(self):
        if self._finalizer.detach():
            self._rmtree(self.name)


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
