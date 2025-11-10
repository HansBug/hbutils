"""
This module provides utilities for temporarily modifying Python's import path (PYTHONPATH) and module cache.

It allows you to mount additional paths to sys.path and manage sys.modules within a context manager,
ensuring that changes are properly isolated and can be reverted when exiting the context.

The main components are:
- :func:`mount_pythonpath`: Context manager to temporarily add paths to PYTHONPATH
- :class:`PythonPathEnv`: Class representing a Python environment with specific paths and modules
"""

import sys
import types
from contextlib import contextmanager
from typing import ContextManager, Mapping, List, Dict

__all__ = [
    'mount_pythonpath',
    'PythonPathEnv',
]


def _copy_list(origin: list, target: list):
    """
    Copy the contents of target list into origin list in-place.
    
    :param origin: The list to be modified.
    :type origin: list
    :param target: The list to copy from.
    :type target: list
    """
    origin[:] = target


def _copy_dict(origin: dict, target: dict):
    """
    Synchronize origin dict with target dict in-place.
    
    Removes keys from origin that are not in target, and updates/adds keys from target.
    
    :param origin: The dictionary to be modified.
    :type origin: dict
    :param target: The dictionary to copy from.
    :type target: dict
    """
    for key in set(origin.keys()) | set(target.keys()):
        if key not in target:
            del origin[key]
        else:
            origin[key] = target[key]


@contextmanager
def _native_mount_pythonpath(paths: List[str], modules: Dict[str, types.ModuleType]) -> ContextManager:
    """
    Internal context manager to temporarily replace sys.path and sys.modules.
    
    This function saves the current state of sys.path and sys.modules, replaces them with
    the provided values, and restores the original state upon exit.
    
    :param paths: List of paths to set as sys.path.
    :type paths: List[str]
    :param modules: Dictionary of modules to set as sys.modules.
    :type modules: Dict[str, types.ModuleType]
    :return: Context manager that handles the mounting and unmounting.
    :rtype: ContextManager
    
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
    Python environment object that encapsulates a specific PYTHONPATH and module set.
    
    This class represents a snapshot of Python's import environment, including the
    sys.path entries and loaded modules. It can be mounted to temporarily activate
    this environment.
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
    def mount(self, keep: bool = True) -> ContextManager['PythonPathEnv']:
        """
        Mount the ``PYTHONPATH`` and modules of this environment.

        This method activates the environment by setting sys.path and sys.modules to the
        values stored in this PythonPathEnv instance. When the context exits, the original
        environment is restored.

        :param keep: If ``True``, changes made during the context (new imports, module modifications)
            will be kept in this PythonPathEnv instance for future mounts. If ``False``, changes
            are discarded. Default is ``True``.
        :type keep: bool
        :return: Context manager that yields this PythonPathEnv instance.
        :rtype: ContextManager[PythonPathEnv]

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
def mount_pythonpath(*path) -> ContextManager[PythonPathEnv]:
    """
    Append paths to ``PYTHONPATH`` within a context manager.
    
    This function allows you to temporarily add directories to Python's import path,
    making packages in those directories importable. When the context exits, both
    sys.path and sys.modules are restored to their original state, ensuring isolation.

    :param path: One or more directory paths to prepend to sys.path.
    :type path: str
    :return: Context manager that yields a PythonPathEnv instance representing the mounted environment.
    :rtype: ContextManager[PythonPathEnv]
    
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
