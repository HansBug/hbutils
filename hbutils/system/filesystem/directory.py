"""
Overview:
    This module provides functions for directory processing, including copying files and directories,
    removing files and directories, and getting the size of files and directories.
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
    Copy a single file or directory.

    :param src: Source path.
    :type src: str
    :param dst: Destination path.
    :type dst: str
    :raises OSError: If there's an error during the copy operation.
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

    This function provides a flexible way to copy multiple files or directories to a destination.
    It can be used similarly to the 'cp -rf' command in Unix.

    :param src1: First source path.
    :type src1: str
    :param src2: Second source path or destination path.
    :type src2: str
    :param srcn_dst: Additional source paths and the destination path.
    :type srcn_dst: str

    :raises NotADirectoryError: If the destination is not a directory when copying multiple sources.

    Usage:
        1. To copy a single file or directory: copy('source', 'destination')
        2. To copy multiple files/directories to an existing directory: copy('source1', 'source2', 'destination')
        3. To copy files matching a pattern: copy('*.txt', 'destination')

    Examples:
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

    This function can remove both files and directories. It supports glob patterns for batch removal.
    It can be used similarly to the 'rm -rf' command in Unix.

    :param files: Files or directories to be removed.
    :type files: str

    Usage:
        1. To remove a single file or directory: remove('path/to/file_or_dir')
        2. To remove multiple files or directories: remove('file1', 'dir1', 'file2')
        3. To remove files matching a pattern: remove('*.txt', 'dir/**/*.py')

    Examples:
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


def _single_getsize(file: str):
    """
    Get the size of a single file or directory.

    :param file: Path to the file or directory.
    :type file: str
    :return: Size of the file or total size of the directory in bytes.
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


def getsize(*files: str):
    """
    Get the size of files or directories.

    This function calculates the total size of all specified files and directories.
    It supports glob patterns for batch size calculation.

    :param files: Paths to files or directories.
    :type files: str
    :return: Total size in bytes.
    :rtype: int

    Usage:
        1. To get size of a single file or directory: getsize('path/to/file_or_dir')
        2. To get total size of multiple files or directories: getsize('file1', 'dir1', 'file2')
        3. To get total size of files matching a pattern: getsize('*.txt', 'dir/**/*.py')

    Examples:
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
