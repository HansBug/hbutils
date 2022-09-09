import sys
from contextlib import contextmanager
from typing import ContextManager

__all__ = ['mount_pythonpath']


@contextmanager
def mount_pythonpath(*path, recover=True, recover_when_replaced=False) -> ContextManager:
    """
    Overview:
        Append ``PYTHONPATH`` in context, the packages in given paths will be able to be imported.
        ``sys.modules`` will also be recovered when quit.

    :param path: Appended python path.
    :param recover: Recover the ``sys.path`` when context is over, default is ``True``.
    :param recover_when_replaced: If ``sys.path`` is replaced again, recover it or not, default is ``False``.
    
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
    oldpath = sys.path
    oldmodules = sys.modules

    newpath = [*path, *oldpath]
    newmodules = {**sys.modules}

    try:
        sys.path = newpath
        sys.modules = newmodules
        yield
    finally:
        if recover:
            if sys.path is newpath or recover_when_replaced:
                sys.path = oldpath
            if sys.modules is newmodules or recover_when_replaced:
                sys.modules = oldmodules
