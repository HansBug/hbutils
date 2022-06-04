"""
Overview:
    Functions for directory processing.
"""
import errno
import os
import shutil

__all__ = [
    'copy', 'remove',
]


def copy(src: str, dst: str):
    """
    Overview:
        Copy a file or a directory from ``src`` to ``dst``.
        ``src`` can be a file or a directory, both are supported.

        From `Stack Overflow - Copy file or directories recursively in Python \
        <https://stackoverflow.com/a/1994840/6995899>`_.

    :param src: Source path.
    :param dst: Destination path.
    """
    try:
        shutil.copytree(src, dst)  # copy directory
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)  # copy file
        else:
            raise  # pragma: no cover


def remove(file: str):
    """
    Overview:
        Remove a file or a directory at ``file``.
        ``file`` can be a file or a directory, both are supported.

    :param file: File or directory to be removed.
    """
    try:
        shutil.rmtree(file)
    except NotADirectoryError:
        os.remove(file)
