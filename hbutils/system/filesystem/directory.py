"""
Overview:
    Functions for directory processing.
    
    This module provides utility functions for common directory and file operations
    including copying, removing, and calculating sizes of files and directories.
    These functions support glob patterns and provide Unix-like command functionality.
"""
import errno
import os
import shutil

from .file import glob

__all__ = [
    'copy', 'remove',
    'getsize',
]


def _single_copy(src: str, dst: str):
    """
    Copy a single file or directory from source to destination.
    
    This is an internal helper function that handles both file and directory copying.
    It attempts to copy as a directory first, and falls back to file copying if needed.
    
    :param src: Source path to copy from.
    :type src: str
    :param dst: Destination path to copy to.
    :type dst: str
    :raises OSError: If the copy operation fails for reasons other than type mismatch.
    """
    try:
        shutil.copytree(src, dst)  # copy directory
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)  # copy file
        else:
            raise  # pragma: no cover


def copy(src1: str, src2: str, *srcn_dst: str):
    """
    Copy files or directories.

    No less than 2 arguments are accepted.
    When the last path is an existing path, all the fore paths will be copied to this path.
    Otherwise, the first path will be copied to the last path (exactly 2 arguments are accepted in this
    case, or ``NotADirectoryError`` will be raised).

    From `Stack Overflow - Copy file or directories recursively in Python
    <https://stackoverflow.com/a/1994840/6995899>`_.

    :param src1: First source path.
    :type src1: str
    :param src2: Second source path or destination path.
    :type src2: str
    :param srcn_dst: Additional source paths and the final destination path.
    :type srcn_dst: str
    :raises NotADirectoryError: If destination is not a directory when multiple sources are provided.

    .. note::
        You can use this like ``cp -rf`` command on unix.

    Examples::
        >>> import os
        >>> from hbutils.system import copy
        >>>
        >>> os.listdir('.')
        ['test', 'README.md', 'cloc.sh', 'LICENSE', 'codecov.yml', 'pytest.ini', 'Makefile', 'setup.py', 'requirements-test.txt', 'requirements-doc.txt', 'requirements.txt']
        >>>
        >>> copy('cloc.sh', 'new_cloc.sh')  # copy file
        >>> copy('test', 'new_test')  # copy directory
        >>> os.listdir('.')
        ['test', 'README.md', 'cloc.sh', 'LICENSE', 'codecov.yml', 'new_test', 'pytest.ini', 'Makefile', 'setup.py', 'requirements-test.txt', 'requirements-doc.txt', 'requirements.txt', 'new_cloc.sh']
        >>>
        >>> os.makedirs('new_path_1')
        >>> copy('*.txt', 'new_path_1')  # copy to new path
        >>> os.listdir('new_path_1')
        ['requirements-test.txt', 'requirements-doc.txt', 'requirements.txt']
        >>>
        >>> os.makedirs('new_path_2')
        >>> copy('*.txt', 'test/system/**/*.py', 'new_path_2')  # copy plenty of files to new path
        >>> print(*os.listdir('new_path_2'), sep='\\n')
        test_version.py
        test_file.py
        test_type.py
        test_package.py
        test_implementation.py
        requirements-test.txt
        __init__.py
        test_directory.py
        requirements-doc.txt
        requirements.txt
    """
    *srcs, dst = (src1, src2, *srcn_dst)
    if os.path.exists(dst) and os.path.isdir(dst):  # copy to directory
        for file in glob(*srcs):
            _, name = os.path.split(file)
            _single_copy(file, os.path.join(dst, name))

    else:  # copy to file
        if len(srcs) > 1:
            raise NotADirectoryError(dst)
        _single_copy(srcs[0], dst)


def remove(*files: str):
    """
    Remove files or directories.
    
    This function can remove both files and directories. It supports glob patterns
    to match multiple files at once. The function works recursively for directories.

    :param files: Files or directories to be removed. Supports glob patterns.
    :type files: str

    .. note::
        You can use this like ``rm -rf`` command on unix.

    Examples::
        >>> import os
        >>> from hbutils.system import remove
        >>>
        >>> os.listdir('.')
        ['test', 'README.md', 'cloc.sh', 'codecov.yml', 'new_test', 'new_path_2', 'setup.py', 'requirements-test.txt', 'new_path_1', 'requirements-doc.txt', 'requirements.txt', 'new_cloc.sh']
        >>>
        >>> remove('codecov.yml')  # remove file
        >>> remove('new_test')  # remove directory
        >>> os.listdir('.')
        ['test', 'README.md', 'cloc.sh', 'new_path_2', 'setup.py', 'requirements-test.txt', 'new_path_1', 'requirements-doc.txt', 'requirements.txt', 'new_cloc.sh']
        >>>
        >>> os.listdir('new_path_1')
        ['requirements-test.txt', 'requirements-doc.txt', 'requirements.txt']
        >>> remove('new_path_1/*.txt')  # remove files from directory
        >>> os.listdir('new_path_1')
        []
        >>>
        >>> print(*os.listdir('new_path_2'), sep='\\n')
        test_version.py
        test_file.py
        test_type.py
        test_package.py
        test_implementation.py
        requirements-test.txt
        __init__.py
        test_directory.py
        requirements-doc.txt
        requirements.txt
        >>> remove('README.md', 'test/**/*.py', 'new_path_2/*.py')  # remove plenty of files
        >>> print(*os.listdir('new_path_2'), sep='\\n')
        requirements-test.txt
        requirements-doc.txt
        requirements.txt
    """
    for file in glob(*files):
        try:  # remove directory
            shutil.rmtree(file)
        except NotADirectoryError:  # remove file
            os.remove(file)


def _single_getsize(file: str) -> int:
    """
    Get the size of a single file or directory.
    
    This is an internal helper function that calculates the total size of a file
    or recursively sums up all file sizes in a directory, excluding symbolic links.
    
    :param file: Path to the file or directory.
    :type file: str
    :return: Size in bytes of the file or total size of all files in the directory.
    :rtype: int
    """
    if os.path.isfile(file):
        return os.path.getsize(file)
    else:
        total = 0
        for dirpath, dirnames, filenames in os.walk(file):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)

        return total


def getsize(*files: str) -> int:
    """
    Get the total size of files or directories.
    
    This function calculates the total size of one or more files or directories.
    For directories, it recursively sums up all file sizes. Supports glob patterns
    to match multiple files.

    :param files: File or directory paths. Supports glob patterns.
    :type files: str
    :return: Total size in bytes of all specified files or directories.
    :rtype: int

    .. note::
        You can use this like ``du -sh`` command on unix.

    Examples::
        >>> from hbutils.system import getsize
        >>>
        >>> getsize('README.md')  # a file
        5368
        >>> getsize('test')  # a directory
        1575574
        >>> getsize('hbutils/**/*.py')  # glob filtered files
        238080
    """
    return sum(map(_single_getsize, glob(*files)))
