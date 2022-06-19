"""
Overview:
    Some useful utils to locate the executable files.

    Based on `hweickert/where <https://github.com/hweickert/where>`_, \
    and this version below will be long-term maintained here.
"""
import itertools
import os
from typing import Iterable, Iterator, Optional, List

from .type import is_windows

__all__ = [
    'where', 'which',
]


def where(execfile: str) -> List[str]:
    """
    Overview:
        Returns all matching file paths.

    :param execfile: Executable file to locate (such as ``python``).
    :return: The list of absolute paths of the executable files.

    Examples::
        >>> from hbutils.system import where
        >>>
        >>> where('apt-get')
        ['/usr/bin/apt-get', '/bin/apt-get']
        >>> where('bash')
        ['/usr/bin/bash', '/bin/bash']
        >>> where('not_installed')
        []
    """
    return list(_iter_where(execfile))


def which(execfile: str) -> Optional[str]:
    """
    Overview:
        Returns first matching file path, which is the one when we operate in terminal.

    :param execfile: Executable file to locate (such as ``python``).
    :return: Absolute path fo the executable file.

    Examples::
        >>> from hbutils.system import which
        >>>
        >>> which('apt-get')
        '/usr/bin/apt-get'
        >>> which('bash')
        '/usr/bin/bash'
        >>> which('not_installed')
        None
    """
    try:
        return next(_iter_where(execfile))
    except StopIteration:
        return None


def _iter_where(filename: str) -> Iterator[str]:
    """
    Like where() but returns an iterator.
    It is originally ``iwhere`` function, but now hidden because :func:`where` is the better choice than this.
    """
    possible_paths = _gen_possible_matches(filename)
    existing_file_paths = filter(_is_executable, possible_paths)
    return existing_file_paths


def _is_executable(filename: str) -> bool:
    """
    Check if the file is an executable file, which should be

    * Exist (of course)
    * Is a file (not a directory)
    * Is executable (not a common file)
    """
    return os.path.exists(filename) and os.path.isfile(filename) and os.access(filename, os.X_OK)


# os.path.normcase and os.path.normpath is VERRRRRRRRY important here,
# because the expression form of a path is actually not unique, especially on Windows.
def _normpath(filename: str) -> str:
    return os.path.normcase(os.path.normpath(os.path.abspath(filename)))


def _unique_str(siter: Iterable[str]) -> Iterator[str]:
    _exist_str = set()
    for s in siter:
        if s not in _exist_str:
            yield s


def _gen_possible_matches(filename) -> Iterator[str]:
    path_parts = os.environ.get("PATH", "").split(os.pathsep)
    if is_windows():  # Only in Windows, the executable file in current directory can be called.
        path_parts = itertools.chain((os.curdir,), path_parts)

    possible_paths = map(lambda x: os.path.join(x, filename), path_parts)
    if is_windows():
        possible_paths = itertools.chain(
            *map(lambda path: (path, f"{path}.bat", f"{path}.cmd", f"{path}.com", f"{path}.exe"), possible_paths))

    return _unique_str(map(_normpath, possible_paths))
