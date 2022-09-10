import sys
import types
from contextlib import contextmanager
from typing import ContextManager, Mapping, List, Dict

__all__ = [
    'mount_pythonpath',
    'PythonPathEnv',
]


@contextmanager
def _native_mount_pythonpath(paths: List[str], modules: Dict[str, types.ModuleType]) -> ContextManager:
    oldpath, oldmodules = sys.path, sys.modules
    try:
        sys.path = paths
        sys.modules = modules
        yield
    finally:
        sys.path = oldpath
        sys.modules = oldmodules


class PythonPathEnv:
    """
    Overview:
        Python environment object.
    """

    def __init__(self, pythonpath: List[str], modules: Mapping[str, types.ModuleType]):
        """
        Constructor of :class:`PythonPathEnv`.

        :param pythonpath: Python path list.
        :param modules: Modules loaded.
        """
        self.pythonpath: List[str] = list(pythonpath)
        self.modules: Dict[str, types.ModuleType] = dict(modules)

    @contextmanager
    def mount(self, keep: bool = True) -> ContextManager['PythonPathEnv']:
        """
        Mount the ``PYTHONPATH`` and modules of this environment.

        :param keep: Keep the changes inside. Default is ``True`` which means the new imports and modules \
            will be kept inside and will be usable when next time the :meth:`mount` is called.

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
    Overview:
        Append ``PYTHONPATH`` in context, the packages in given paths will be able to be imported.
        ``sys.modules`` will also be recovered when quit.

    :param path: Appended python path.
    
    Examples::
        Here is the testfile directory

        >>> import os
        >>> os.system('tree test/testfile')
        test/testfile
        ├── dir1
        │   ├── gf1.py
        ├── dir2
        │   ├── gf1.py
        └── igm
            └── gf1.py

        We can import the values from the other directories, like this

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
        >>> from gf1 import FIXED  # cannot import outside
        ModuleNotFoundError: No module named 'gf1'

    """
    with _native_mount_pythonpath([*path, *sys.path], {**sys.modules}):
        yield PythonPathEnv(sys.path, sys.modules)
