"""
This module provides utilities for managing Python package requirements and pip operations.

It includes functions for:
- Checking package versions
- Loading and parsing requirements files
- Running pip commands programmatically
- Checking if requirements are satisfied
- Installing packages and requirements files

The module handles requirement parsing, dependency checking, and pip command execution
in a programmatic way, making it easier to manage dependencies in Python projects.
"""

import functools
import itertools
import os
import pathlib
import subprocess
import sys
from typing import List, Optional

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

try:
    import importlib.metadata as importlib_metadata
except (ModuleNotFoundError, ImportError):
    import importlib_metadata
from packaging.version import Version

__all__ = [
    'package_version',
    'load_req_file', 'pip',
    'check_reqs', 'check_req_file',
    'pip_install', 'pip_install_req_file',
]


def package_version(name: str) -> Optional[Version]:
    """
    Get version of package with given name.

    :param name: Name of the package, case is not sensitive.
    :type name: str
    :return: A :class:`packaging.version.Version` object. If the package is not installed, return ``None``.
    :rtype: Optional[Version]

    Examples::
        >>> from hbutils.system import package_version
        >>>
        >>> package_version('pip')
        <Version('21.3.1')>
        >>> package_version('setuptools')
        <Version('59.6.0')>
        >>> package_version('not_a_package')
        None
    """
    try:
        return Version(importlib_metadata.distribution(canonicalize_name(name)).version)
    except importlib_metadata.PackageNotFoundError:
        return None


def _nonblank(text: str) -> bool:
    """
    Check if text is non-blank and not a comment line.

    :param text: Text to check.
    :type text: str
    :return: True if text is non-blank and doesn't start with '#'.
    :rtype: bool
    """
    return text and not text.startswith('#')


@functools.singledispatch
def yield_lines(iterable):
    """
    Yield valid lines of a string or iterable.
    
    Based on https://github.com/jaraco/jaraco.text/blob/main/jaraco/text/__init__.py#L537 .
    
    :param iterable: An iterable of strings or a string.
    :return: Generator yielding valid non-blank lines.
    
    Examples::
        >>> list(yield_lines(''))
        []
        >>> list(yield_lines(['foo', 'bar']))
        ['foo', 'bar']
        >>> list(yield_lines('foo\\nbar'))
        ['foo', 'bar']
        >>> list(yield_lines('\\nfoo\\n#bar\\nbaz #comment'))
        ['foo', 'baz #comment']
        >>> list(yield_lines(['foo\\nbar', 'baz', 'bing\\n\\n\\n']))
        ['foo', 'bar', 'baz', 'bing']
    """
    return itertools.chain.from_iterable(map(yield_lines, iterable))


@yield_lines.register(str)
def _(text: str):
    """
    Yield valid lines from a string.
    
    :param text: Text string to process.
    :type text: str
    :return: Generator yielding valid non-blank lines.
    """
    return filter(_nonblank, map(str.strip, text.splitlines()))


def drop_comment(line: str) -> str:
    """
    Drop comments from a line.
    
    Based on https://github.com/jaraco/jaraco.text/blob/main/jaraco/text/__init__.py#L560 .
    
    :param line: Line of text to process.
    :type line: str
    :return: Line with comment removed.
    :rtype: str
    
    Examples::
        >>> drop_comment('foo # bar')
        'foo'
        
    A hash without a space may be in a URL::
        >>> drop_comment('https://example.com/foo#bar')
        'https://example.com/foo#bar'
    """
    return line.partition(' #')[0]


def join_continuation(lines):
    """
    Join lines continued by a trailing backslash.
    
    Based on https://github.com/jaraco/jaraco.text/blob/main/jaraco/text/__init__.py#L575 .
    
    :param lines: Iterable of lines to process.
    :return: Generator yielding joined lines.
    
    Examples::
        >>> list(join_continuation(['foo \\\\', 'bar', 'baz']))
        ['foobar', 'baz']
        >>> list(join_continuation(['foo \\\\', 'bar', 'baz']))
        ['foobar', 'baz']
        >>> list(join_continuation(['foo \\\\', 'bar \\\\', 'baz']))
        ['foobarbaz']
        
    Note:
        The character preceding the backslash is also elided::
            >>> list(join_continuation(['goo\\\\', 'dly']))
            ['godly']
        
        If no line is available to continue, suppress the lines::
            >>> list(join_continuation(['foo', 'bar\\\\', 'baz\\\\']))
            ['foo']
    """
    lines = iter(lines)
    for item in lines:
        while item.endswith('\\'):
            try:  # pragma: no cover
                item = item[:-2].strip() + next(lines)
            except StopIteration:
                return
        yield item


def load_req_file(requirements_file: str) -> List[str]:
    """
    Load requirements items from a requirements.txt file.

    :param requirements_file: Requirements file path.
    :type requirements_file: str
    :return: List of requirements.
    :rtype: List[str]

    Examples::
        >>> from hbutils.system import load_req_file
        >>> load_req_file('requirements.txt')
        ['packaging>=21.3', 'setuptools>=50.0']
    """
    with pathlib.Path(requirements_file).open() as reqfile:
        return list(map(
            lambda x: str(Requirement(x)),
            join_continuation(map(drop_comment, yield_lines(reqfile)))
        ))


def pip(*args, silent: bool = False):
    """
    Run pip command with code.

    :param args: Command line arguments for ``pip`` command.
    :param silent: Do not print anything. Default is False, which means print the output to ``sys.stdout`` \
        and ``sys.stderr``.
    :type silent: bool
    :raises AssertionError: If pip command returns non-zero exit code.

    Examples::
        >>> from hbutils.system import pip
        >>> pip('-V')
        pip 22.3.1 from /home/user/myproject/venv/lib/python3.7/site-packages/pip (python 3.7)
        >>> pip('-V', silent=True)  # nothing will be printed
    """
    process = subprocess.run(
        [sys.executable, '-m', 'pip', *args],
        stdin=sys.stdin if not silent else None,
        stdout=sys.stdout if not silent else subprocess.PIPE,
        stderr=sys.stderr if not silent else subprocess.PIPE,
    )
    assert not process.returncode, f'Error when calling {process.args!r}{os.linesep}' \
                                   f'Error Code - {process.returncode}{os.linesep}' \
                                   f'Stdout:{os.linesep}' \
                                   f'{process.stdout.decode()}{os.linesep}' \
                                   f'{os.linesep}' \
                                   f'Stderr:{os.linesep}' \
                                   f'{process.stderr.decode()}{os.linesep}'
    process.check_returncode()


def _yield_reqs_to_install(req: Requirement, current_extra: str = ''):
    """
    Yield requirements that need to be installed.
    
    This function recursively checks a requirement and its dependencies to determine
    which packages need to be installed.

    :param req: Requirement to check.
    :type req: Requirement
    :param current_extra: Current extra being evaluated.
    :type current_extra: str
    :return: Generator yielding requirements that need installation.
    """
    if req.marker and not req.marker.evaluate({'extra': current_extra}):
        return

    try:
        version = importlib_metadata.distribution(req.name).version
    except importlib_metadata.PackageNotFoundError:  # req not installed
        yield req
    else:
        if req.specifier.contains(version):
            for child_req in (importlib_metadata.metadata(req.name).get_all('Requires-Dist') or []):
                child_req_obj = Requirement(child_req)

                need_check, ext = False, None
                for extra in req.extras:
                    if child_req_obj.marker and child_req_obj.marker.evaluate({'extra': extra}):
                        need_check = True
                        ext = extra
                        break

                if need_check:  # check for extra reqs
                    yield from _yield_reqs_to_install(child_req_obj, ext)

        else:  # main version not match
            yield req


def _check_req(req: Requirement) -> bool:
    """
    Check if a single requirement is satisfied.

    :param req: Requirement to check.
    :type req: Requirement
    :return: True if requirement is satisfied, False otherwise.
    :rtype: bool
    """
    return not bool(list(itertools.islice(_yield_reqs_to_install(req), 1)))


def check_reqs(reqs: List[str]) -> bool:
    """
    Check if the given requirements are all satisfied.

    :param reqs: List of requirements.
    :type reqs: List[str]
    :return: All the requirements in ``reqs`` satisfied or not.
    :rtype: bool

    Examples::
        >>> from hbutils.system import check_reqs
        >>> check_reqs(['pip>=20.0'])
        True
        >>> check_reqs(['pip~=19.2'])
        False
        >>> check_reqs(['pip>=20.0', 'setuptools>=50.0'])
        True

    .. note::
        If a requirement's marker is not satisfied in this environment,
        **it will be ignored** instead of return ``False``.
    """
    return all(map(lambda x: _check_req(Requirement(x)), reqs))


def check_req_file(requirements_file: str) -> bool:
    """
    Check if the requirements in the given requirements_file is satisfied.

    :param requirements_file: Requirements file, such as ``requirements.txt``.
    :type requirements_file: str
    :return: All the requirements in ``requirements_file`` satisfied or not.
    :rtype: bool

    Examples::
        >>> from hbutils.system import check_req_file
        >>>
        >>> check_req_file('requirements.txt')
        True
        >>> check_req_file('requirements-test.txt')
        True
    """
    return check_reqs(load_req_file(requirements_file))


def pip_install(reqs: List[str], silent: bool = False, force: bool = False, user: bool = False):
    """
    Pip install requirements with code.
    
    Similar to ``pip install req1 req2 ...``.

    :param reqs: Requirement items to install.
    :type reqs: List[str]
    :param silent: Do not print anything. Default is ``False``.
    :type silent: bool
    :param force: Force execute the ``pip install`` command. Default is ``False`` which means the requirements \
        will be checked before installation, and the installation will be only executed when \
        some requirements not installed.
    :type force: bool
    :param user: User mode, represents ``--user`` option in ``pip``.
    :type user: bool

    Examples::
        >>> from hbutils.system import pip_install
        >>> pip_install(['scikit-learn'])  # not installed
        Looking in indexes: https://xxx/simple
        Collecting scikit-learn
          Using cached https://xxx/scikit_learn-1.0.2-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (24.8 MB)
        Installing collected packages: threadpoolctl, scipy, joblib, scikit-learn
        Successfully installed joblib-1.2.0 scikit-learn-1.0.2 scipy-1.7.3 threadpoolctl-3.1.0
        >>> pip_install(['numpy>=1.10.0'])  # installed
        >>> pip_install(['numpy>=1.10.0'], force=True)  # force execute
        Looking in indexes: https://xxx/simple
        Requirement already satisfied: numpy>=1.10.0 in ./venv/lib/python3.7/site-packages (1.21.6)
    """
    if force or not check_reqs(reqs):
        pip('install', *(('--user',) if user else ()), *reqs, silent=silent)


def pip_install_req_file(requirements_file: str, silent: bool = False, force: bool = False, user: bool = False):
    """
    Pip install requirements from file with code.
    
    Similar to ``pip install -r requirements.txt``.

    :param requirements_file: Requirements file, such as ``requirements.txt``.
    :type requirements_file: str
    :param silent: Do not print anything. Default is ``False``.
    :type silent: bool
    :param force: Force execute the ``pip install`` command. Default is ``False`` which means the requirements \
        will be checked before installation, and the installation will be only executed when \
        some requirements not installed.
    :type force: bool
    :param user: User mode, represents ``--user`` option in ``pip``.
    :type user: bool

    Examples::
        >>> from hbutils.system import pip_install_req_file
        >>> pip_install_req_file('requirements.txt')  # pip install -r requirements.txt
    """
    if force or not check_req_file(requirements_file):
        pip('install', *(('--user',) if user else ()), '-r', requirements_file, silent=silent)
