"""
Temporary directory utilities with Windows-compatible cleanup behavior.

This module provides a backport-compatible :class:`TemporaryDirectory` implementation
for environments where the standard library's behavior can raise
:class:`PermissionError` during cleanup (notably Windows on Python 3.7). For Python
3.10 and newer, the standard library implementation is re-exported directly.

The module exposes the following public component:

* :class:`TemporaryDirectory` - Context manager for creating and cleaning up
  temporary directories with Windows-friendly error handling.

.. note::
   On Python 3.10+, this module transparently re-exports
   :class:`tempfile.TemporaryDirectory`.

Example::

    >>> from hbutils.system.filesystem.tempfile import TemporaryDirectory
    >>> with TemporaryDirectory(prefix='demo_') as tmpdir:
    ...     # Use tmpdir for temporary operations
    ...     pass
    >>> # Directory is automatically cleaned up after exiting the context

"""
import os
import platform
import shutil
import tempfile
import warnings
import weakref
from typing import Optional, Callable, Tuple, Type, Any

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
        Create and return a temporary directory.

        This class mirrors :class:`tempfile.TemporaryDirectory` from Python 3.10
        and adds more resilient cleanup behavior on platforms where permission
        errors can occur during removal (notably Windows on Python 3.7).

        .. note::
           **This class is copied from Python 3.10's tempfile library.**

           Because :class:`PermissionError` will be raised when using native
           :class:`tempfile.TemporaryDirectory` on **Windows Python 3.7**, this
           implementation handles permission reset and retries. It should be
           removed when Python 3.9 is end of life.

           See `tempfile.TemporaryDirectory <https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory>`_
           for more details.

        This has the same behavior as :func:`tempfile.mkdtemp` but can be used
        as a context manager.

        Example::

            >>> with TemporaryDirectory() as tmpdir:
            ...     # Use tmpdir for temporary operations
            ...     pass
            >>> # Directory is automatically cleaned up after exiting the context

        Upon exiting the context, the directory and everything contained
        in it are removed.
        """

        def __init__(
            self,
            suffix: Optional[str] = None,
            prefix: Optional[str] = None,
            dir: Optional[str] = None,
            ignore_cleanup_errors: bool = False
        ) -> None:
            """
            Initialize a temporary directory.

            :param suffix: If specified, the directory name will end with that
                suffix, otherwise there will be no suffix.
            :type suffix: str or None
            :param prefix: If specified, the directory name will begin with that
                prefix, otherwise a default prefix is used.
            :type prefix: str or None
            :param dir: If specified, the directory will be created in that
                directory, otherwise a default directory is used.
            :type dir: str or None
            :param ignore_cleanup_errors: If ``True``, errors during cleanup will
                be ignored.
            :type ignore_cleanup_errors: bool
            """
            self.name: str = tempfile.mkdtemp(suffix, prefix, dir)
            self._ignore_cleanup_errors: bool = ignore_cleanup_errors
            self._finalizer = weakref.finalize(
                self, self._cleanup, self.name,
                warn_message="Implicitly cleaning up {!r}".format(self),
                ignore_errors=self._ignore_cleanup_errors)

        @classmethod
        def _rmtree(cls, name: str, ignore_errors: bool = False) -> None:
            """
            Remove a directory tree with enhanced error handling.

            This method handles permission errors by resetting file permissions
            before attempting to remove files and directories. It's particularly
            useful on Windows where permission issues are common.

            :param name: The path to the directory tree to remove.
            :type name: str
            :param ignore_errors: If ``True``, errors during removal will be
                ignored.
            :type ignore_errors: bool
            """

            def onerror(func: Callable[..., Any], path: str, exc_info: Tuple[Type[BaseException], BaseException, Any]) -> None:
                """
                Error handler for :func:`shutil.rmtree`.

                :param func: The function that raised the exception.
                :type func: callable
                :param path: The path that caused the exception.
                :type path: str
                :param exc_info: Exception information tuple
                    ``(type, value, traceback)``.
                :type exc_info: tuple
                """
                if issubclass(exc_info[0], PermissionError):
                    def resetperms(path: str) -> None:
                        """
                        Reset permissions on a path to allow removal.

                        :param path: The path to reset permissions on.
                        :type path: str
                        """
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
        def _cleanup(cls, name: str, warn_message: str, ignore_errors: bool = False) -> None:
            """
            Clean up the temporary directory and issue a warning.

            :param name: The path to the directory to clean up.
            :type name: str
            :param warn_message: The warning message to display.
            :type warn_message: str
            :param ignore_errors: If ``True``, errors during cleanup will be
                ignored.
            :type ignore_errors: bool
            """
            cls._rmtree(name, ignore_errors=ignore_errors)
            warnings.warn(warn_message, ResourceWarning)

        def __repr__(self) -> str:
            """
            Return a string representation of the TemporaryDirectory instance.

            :return: String representation showing the class name and directory
                path.
            :rtype: str
            """
            return "<{} {!r}>".format(self.__class__.__name__, self.name)

        def __enter__(self) -> str:
            """
            Enter the context manager.

            :return: The path to the temporary directory.
            :rtype: str
            """
            return self.name

        def __exit__(
            self,
            exc: Optional[Type[BaseException]],
            value: Optional[BaseException],
            tb: Optional[Any]
        ) -> None:
            """
            Exit the context manager and clean up the temporary directory.

            :param exc: Exception type if an exception occurred, ``None`` otherwise.
            :type exc: type or None
            :param value: Exception value if an exception occurred, ``None`` otherwise.
            :type value: Exception or None
            :param tb: Traceback if an exception occurred, ``None`` otherwise.
            :type tb: traceback or None
            """
            self.cleanup()

        def cleanup(self) -> None:
            """
            Explicitly clean up the temporary directory.

            This method can be called to manually remove the temporary directory
            before the object is garbage collected. It's safe to call multiple
            times.
            """
            if self._finalizer.detach() or os.path.exists(self.name):
                self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)

        if GenericAlias is not None:
            __class_getitem__ = classmethod(GenericAlias)
