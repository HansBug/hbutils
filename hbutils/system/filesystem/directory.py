"""
Overview:
    Functions for directory processing.
"""
import errno
import shutil

__all__ = [
    'copy',
]


def copy(src, dst):
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
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            raise  # pragma: no cover
