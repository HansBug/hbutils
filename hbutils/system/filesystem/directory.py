"""
Overview:
    Functions for directory processing.
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
    try:
        shutil.copytree(src, dst)  # copy directory
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)  # copy file
        else:
            raise  # pragma: no cover


def copy(src1: str, src2: str, *srcn_dst: str):
    """
    Overview:
        Copy files or directories.

        No less than 2 arguments are accepted.
        When the last path is an existing path, all the fore paths will be copied to this path.
        Otherwise, the first path will be copied to the last path (exactly 2 arguments are accepted in this \
            case, or ``NotADirectoryError`` will be raised).

        From `Stack Overflow - Copy file or directories recursively in Python \
        <https://stackoverflow.com/a/1994840/6995899>`_.

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
        >>> print(*os.listdir('new_path_2'), sep=\'\\n\')
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
    Overview:
        Remove a file or a directory at ``file``.
        ``file`` can be a file or a directory, both are supported.

    :param files: Files or directories to be removed.

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
        >>> print(*os.listdir('new_path_2'), sep=\'\\n\')
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
        >>> print(*os.listdir('new_path_2'), sep=\'\\n\')
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
    Overview:
        Get size of a file or a directory.

    :param files: File paths.
    :return: Size of the file or the total size of the directory.

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
