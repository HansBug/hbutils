"""
Utilities for temporarily modifying Python's import environment.

This module provides context-managed helpers for mounting custom ``PYTHONPATH``
entries and isolating ``sys.modules`` state. It enables predictable import
behavior by allowing you to activate a snapshot of paths and modules, then
restore the original environment when the context exits.

The module exposes the following public components:

* :func:`mount_pythonpath` - Context manager to temporarily prepend import paths
* :class:`PythonPathEnv` - Snapshot of an import environment with mount support

.. note::
   All modifications to ``sys.path`` and ``sys.modules`` are reverted on context
   exit. Use the ``keep`` argument of :meth:`PythonPathEnv.mount` to persist
   changes into the snapshot.

Example::

    >>> from hbutils.reflection import mount_pythonpath
    >>> with mount_pythonpath('path/to/plugins') as env:
    ...     import my_plugin
    ...     print(my_plugin.__name__)
    my_plugin
    >>> # `my_plugin` is no longer importable outside the context

"""

import sys
import types
from contextlib import contextmanager
from typing import ContextManager, Mapping, List, Dict, Iterator

__all__ = [
    'mount_pythonpath',
    'PythonPathEnv',
]


def _copy_list(origin: List[str], target: List[str]) -> None:
    """
    Copy the contents of ``target`` list into ``origin`` list in-place.

    This helper performs an in-place update to the list referenced by ``origin``,
    ensuring that all references to the original list reflect the new contents.

    :param origin: The list to be modified in place.
    :type origin: List[str]
    :param target: The list to copy from.
    :type target: List[str]
    :return: This function returns ``None``.
    :rtype: None
    """
    origin[:] = target


def _copy_dict(origin: Dict[str, types.ModuleType],
               target: Dict[str, types.ModuleType]) -> None:
    """
    Synchronize ``origin`` dict with ``target`` dict in-place.

    Keys that are not present in ``target`` are removed from ``origin``, and
    keys present in ``target`` are added or updated to reference the same
    module objects.

    :param origin: The dictionary to be modified in place.
    :type origin: Dict[str, types.ModuleType]
    :param target: The dictionary to copy from.
    :type target: Dict[str, types.ModuleType]
    :return: This function returns ``None``.
    :rtype: None
    """
    for key in set(origin.keys()) | set(target.keys()):
        if key not in target:
            del origin[key]
        else:
            origin[key] = target[key]


@contextmanager
def _native_mount_pythonpath(paths: List[str],
                             modules: Dict[str, types.ModuleType]) -> Iterator[None]:
    """
    Temporarily replace ``sys.path`` and ``sys.modules`` with provided values.

    This internal context manager saves the current state of ``sys.path`` and
    ``sys.modules``, replaces them with the provided values, and restores the
    original state upon exit.

    :param paths: List of paths to assign to ``sys.path`` during the context.
    :type paths: List[str]
    :param modules: Mapping of modules to assign to ``sys.modules`` during the
        context.
    :type modules: Dict[str, types.ModuleType]
    :return: A context manager that yields ``None`` while mounted.
    :rtype: Iterator[None]

    Example::

        >>> with _native_mount_pythonpath(['/custom/path'], {}):
        ...     # sys.path is now ['/custom/path']
        ...     # sys.modules is now {}
        ...     pass
        >>> # sys.path and sys.modules are restored
    """
    from ..collection import get_recovery_func
    path_rec = get_recovery_func(sys.path, recursive=False)
    modules_rec = get_recovery_func(sys.modules, recursive=False)
    try:
        _copy_list(sys.path, paths)
        _copy_dict(sys.modules, modules)
        yield
    finally:
        path_rec()
        modules_rec()


class PythonPathEnv:
    """
    Snapshot of a Python import environment.

    This class captures a specific ``PYTHONPATH`` and module set so that it can
    be mounted later. It is typically created by :func:`mount_pythonpath`.

    :param pythonpath: Python path list to be used in this environment.
    :type pythonpath: List[str]
    :param modules: Dictionary of modules loaded in this environment.
    :type modules: Mapping[str, types.ModuleType]

    :ivar pythonpath: Stored path entries used when mounted.
    :vartype pythonpath: List[str]
    :ivar modules: Stored module mapping used when mounted.
    :vartype modules: Dict[str, types.ModuleType]
    """

    def __init__(self, pythonpath: List[str], modules: Mapping[str, types.ModuleType]):
        """
        Constructor of :class:`PythonPathEnv`.

        :param pythonpath: Python path list to be used in this environment.
        :type pythonpath: List[str]
        :param modules: Dictionary of modules loaded in this environment.
        :type modules: Mapping[str, types.ModuleType]
        """
        self.pythonpath: List[str] = list(pythonpath)
        self.modules: Dict[str, types.ModuleType] = dict(modules)

    @contextmanager
    def mount(self, keep: bool = True) -> Iterator['PythonPathEnv']:
        """
        Mount the stored ``PYTHONPATH`` and modules of this environment.

        This method activates the environment by setting ``sys.path`` and
        ``sys.modules`` to the values stored in this :class:`PythonPathEnv`
        instance. When the context exits, the original environment is restored.

        :param keep: If ``True``, changes made during the context (new imports,
            module modifications) will be kept in this :class:`PythonPathEnv`
            instance for future mounts. If ``False``, changes are discarded.
            Defaults to ``True``.
        :type keep: bool
        :return: Context manager that yields this :class:`PythonPathEnv` instance.
        :rtype: Iterator[PythonPathEnv]

        Examples::

            >>> from hbutils.reflection import mount_pythonpath
            >>> with mount_pythonpath('test/testfile/igm') as env:
            ...     from gf1 import FIXED
            ...     print('FIXED in igm:', FIXED)
            FIXED in igm: 1234567
            >>> with env.mount():
            ...     from gf1 import FIXED
            ...     print('FIXED in igm:', FIXED)
            FIXED in igm: 1234567
        """
        if keep:
            pythonpath, modules = self.pythonpath, self.modules
        else:
            pythonpath, modules = [*self.pythonpath], {**self.modules}

        with _native_mount_pythonpath(pythonpath, modules):
            yield self


@contextmanager
def mount_pythonpath(*path: str) -> Iterator[PythonPathEnv]:
    """
    Prepend paths to ``PYTHONPATH`` within a context manager.

    This function temporarily inserts directories into ``sys.path`` and
    restores both ``sys.path`` and ``sys.modules`` when the context exits,
    ensuring isolation.

    :param path: One or more directory paths to prepend to ``sys.path``.
    :type path: str
    :return: Context manager that yields a :class:`PythonPathEnv` instance
        representing the mounted environment.
    :rtype: Iterator[PythonPathEnv]

    Examples::

        Here is the testfile directory structure:

        >>> import os
        >>> os.system('tree test/testfile')
        test/testfile
        ├── dir1
        │   ├── gf1.py
        ├── dir2
        │   ├── gf1.py
        └── igm
            └── gf1.py

        We can import values from different directories:

        >>> from hbutils.reflection import mount_pythonpath
        >>> with mount_pythonpath('test/testfile/igm'):
        ...     from gf1 import FIXED
        ...     print('FIXED in igm:', FIXED)
        FIXED in igm: 1234567
        >>>
        >>> with mount_pythonpath('test/testfile/dir1'):
        ...     from gf1 import FIXED
        ...     print('FIXED in dir1:', FIXED)
        FIXED in dir1: 233
        >>>
        >>> with mount_pythonpath('test/testfile/dir2'):
        ...     from gf1 import FIXED
        ...     print('FIXED in dir2:', FIXED)
        FIXED in dir2: 455
        >>>
        >>> from gf1 import FIXED  # cannot import outside the context
        ModuleNotFoundError: No module named 'gf1'

    """
    with _native_mount_pythonpath([*path, *sys.path], {**sys.modules}):
        yield PythonPathEnv(sys.path, sys.modules)
