"""
This module provides a backport of the `tempfile.TemporaryDirectory` class for Python 3.7 on Windows.
It addresses a PermissionError issue that occurs when using the native TemporaryDirectory on Windows Python 3.7.
The module includes a custom implementation of TemporaryDirectory that mimics the behavior of the Python 3.10 version.

This backport should be used until Python 3.9 reaches end-of-life.
"""

import os
import platform
import shutil
import tempfile
import warnings
import weakref

try:
    from types import GenericAlias
except (ImportError, ModuleNotFoundError):
    GenericAlias = None

__all__ = [
    'TemporaryDirectory',
]

_python_version_tuple = tuple(map(int, platform.python_version_tuple()))

if _python_version_tuple >= (3, 10):
    from tempfile import TemporaryDirectory

else:
    class TemporaryDirectory:
        """
        Create and return a temporary directory that can be used as a context manager.

        This class is a backport of the Python 3.10 tempfile.TemporaryDirectory implementation,
        addressing PermissionError issues on Windows Python 3.7.

        Usage:
            >>> with TemporaryDirectory() as tmpdir:
            >>>     # Use tmpdir as a temporary directory
            >>>     ...

        Upon exiting the context, the directory and its contents are removed.

        :param suffix: Optional suffix for the directory name.
        :type suffix: str or None
        :param prefix: Optional prefix for the directory name.
        :type prefix: str or None
        :param dir: The parent directory to create the temporary directory in.
        :type dir: str or None
        :param ignore_cleanup_errors: If True, ignore errors during cleanup.
        :type ignore_cleanup_errors: bool

        :raises OSError: If there is an error in creating or cleaning up the directory.
        """

        def __init__(self, suffix=None, prefix=None, dir=None,
                     ignore_cleanup_errors=False):
            """
            Initialize the TemporaryDirectory.

            :param suffix: Optional suffix for the directory name.
            :param prefix: Optional prefix for the directory name.
            :param dir: The parent directory to create the temporary directory in.
            :param ignore_cleanup_errors: If True, ignore errors during cleanup.
            """
            self.name = tempfile.mkdtemp(suffix, prefix, dir)
            self._ignore_cleanup_errors = ignore_cleanup_errors
            self._finalizer = weakref.finalize(
                self, self._cleanup, self.name,
                warn_message="Implicitly cleaning up {!r}".format(self),
                ignore_errors=self._ignore_cleanup_errors)

        @classmethod
        def _rmtree(cls, name, ignore_errors=False):
            """
            Recursively delete a directory tree.

            This method handles permission errors by attempting to modify file permissions
            before deletion.

            :param name: The path of the directory to remove.
            :type name: str
            :param ignore_errors: If True, ignore errors during deletion.
            :type ignore_errors: bool
            """

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
                            cls._rmtree(path, ignore_errors=ignore_errors)
                    except FileNotFoundError:
                        pass
                elif issubclass(exc_info[0], FileNotFoundError):
                    pass
                else:
                    if not ignore_errors:
                        raise

            shutil.rmtree(name, onerror=onerror)

        @classmethod
        def _cleanup(cls, name, warn_message, ignore_errors=False):
            """
            Clean up the temporary directory and issue a warning.

            :param name: The path of the directory to clean up.
            :type name: str
            :param warn_message: The warning message to display.
            :type warn_message: str
            :param ignore_errors: If True, ignore errors during cleanup.
            :type ignore_errors: bool
            """
            cls._rmtree(name, ignore_errors=ignore_errors)
            warnings.warn(warn_message, ResourceWarning)

        def __repr__(self):
            """
            Return a string representation of the TemporaryDirectory instance.

            :return: A string representation of the instance.
            :rtype: str
            """
            return "<{} {!r}>".format(self.__class__.__name__, self.name)

        def __enter__(self):
            """
            Enter the context manager.

            :return: The path of the temporary directory.
            :rtype: str
            """
            return self.name

        def __exit__(self, exc, value, tb):
            """
            Exit the context manager and clean up the temporary directory.

            :param exc: The exception type if an exception was raised.
            :param value: The exception value if an exception was raised.
            :param tb: The traceback if an exception was raised.
            """
            self.cleanup()

        def cleanup(self):
            """
            Clean up the temporary directory.

            This method is called automatically when exiting the context manager,
            but can also be called manually if needed.
            """
            if self._finalizer.detach() or os.path.exists(self.name):
                self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)

        if GenericAlias is not None:
            __class_getitem__ = classmethod(GenericAlias)
