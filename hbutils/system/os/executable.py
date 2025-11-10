"""
Overview:
    Some useful utils to locate the executable files.

    Based on `hweickert/where <https://github.com/hweickert/where>`_, \
    and this version below will be long-term maintained here.
    
    This module provides functionality to search for executable files in the system PATH,
    similar to the Unix 'which' and 'where' commands. It supports both Unix-like systems
    and Windows, handling platform-specific differences in executable file extensions and
    search paths.
"""
import itertools
import os
from typing import Iterable, Iterator, Optional, List

from deprecation import deprecated

from .type import is_windows
from ...config.meta import __VERSION__

__all__ = [
    'where', 'which',
]


def where(execfile: str) -> List[str]:
    """
    Returns all matching file paths for the given executable file.

    This function searches through all directories in the system PATH environment
    variable and returns a list of all absolute paths where the executable file
    can be found. On Windows, it also checks for common executable extensions
    (.bat, .cmd, .com, .exe).

    :param execfile: Executable file to locate (such as ``python``).
    :type execfile: str
    :return: The list of absolute paths of the executable files.
    :rtype: List[str]

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


@deprecated(deprecated_in="0.9", removed_in="1.0", current_version=__VERSION__,
            details="Use the native :func:`shutil.which` instead")
def which(execfile: str) -> Optional[str]:
    """
    Returns first matching file path, which is the one when we operate in terminal.

    This function returns the first executable file found in the system PATH,
    which is typically the one that would be executed when running the command
    in a terminal. Returns None if no matching executable is found.

    .. deprecated:: 0.9
        Use the native :func:`shutil.which` instead. This function will be removed in version 1.0.

    :param execfile: Executable file to locate (such as ``python``).
    :type execfile: str
    :return: Absolute path of the executable file, or None if not found.
    :rtype: Optional[str]

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

    This is an internal helper function that generates an iterator of all matching
    executable file paths. It was originally named ``iwhere`` but is now hidden
    as :func:`where` is the preferred public interface.

    :param filename: The executable filename to search for.
    :type filename: str
    :return: An iterator yielding absolute paths of matching executable files.
    :rtype: Iterator[str]
    """
    possible_paths = _gen_possible_matches(filename)
    existing_file_paths = filter(_is_executable, possible_paths)
    return existing_file_paths


def _is_executable(filename: str) -> bool:
    """
    Check if the file is an executable file.

    A file is considered executable if it:
    * Exists
    * Is a file (not a directory)
    * Has executable permissions (not a common file)

    :param filename: The file path to check.
    :type filename: str
    :return: True if the file is executable, False otherwise.
    :rtype: bool
    """
    return os.path.exists(filename) and os.path.isfile(filename) and os.access(filename, os.X_OK)


def _normpath(filename: str) -> str:
    """
    Normalize a file path to a canonical form.

    This function applies both case normalization and path normalization to ensure
    consistent path representation across different platforms. This is especially
    important on Windows where path representations can vary significantly.

    Note:
        os.path.normcase and os.path.normpath are VERY important here,
        because the expression form of a path is actually not unique, especially on Windows.

    :param filename: The file path to normalize.
    :type filename: str
    :return: The normalized absolute path.
    :rtype: str
    """
    return os.path.normcase(os.path.normpath(os.path.abspath(filename)))


def _unique_str(siter: Iterable[str]) -> Iterator[str]:
    """
    Filter an iterable of strings to yield only unique values.

    This function maintains the order of first occurrence while removing duplicates
    from the input iterable.

    :param siter: An iterable of strings.
    :type siter: Iterable[str]
    :return: An iterator yielding unique strings in order of first occurrence.
    :rtype: Iterator[str]
    """
    _exist_str = set()
    for s in siter:
        if s not in _exist_str:
            yield s
            _exist_str.add(s)


def _gen_possible_matches(filename: str) -> Iterator[str]:
    """
    Generate all possible file paths where the executable might be located.

    This function generates potential paths by combining the filename with all
    directories in the system PATH. On Windows, it also:
    * Includes the current directory in the search
    * Appends common executable extensions (.bat, .cmd, .com, .exe)

    All generated paths are normalized to ensure uniqueness and consistency.

    :param filename: The executable filename to search for.
    :type filename: str
    :return: An iterator yielding normalized possible file paths.
    :rtype: Iterator[str]
    """
    path_parts = os.environ.get("PATH", "").split(os.pathsep)
    if is_windows():  # Only in Windows, the executable file in current directory can be called.
        path_parts = itertools.chain((os.curdir,), path_parts)

    possible_paths = map(lambda x: os.path.join(x, filename), path_parts)
    if is_windows():
        possible_paths = itertools.chain(
            *map(lambda path: (path, f"{path}.bat", f"{path}.cmd", f"{path}.com", f"{path}.exe"), possible_paths))

    return _unique_str(map(_normpath, possible_paths))
