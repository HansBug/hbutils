import importlib
import os
import pathlib
import subprocess
import sys
from typing import Dict, Optional
from typing import List

import pkg_resources
from packaging.version import Version

__all__ = [
    'package_version',
    'load_req_file', 'pip',
    'check_reqs', 'check_req_file',
    'pip_install', 'pip_install_req_file',
]

PIP_PACKAGES: Dict[str, str] = {}


def _init_pip_packages():
    global PIP_PACKAGES
    PIP_PACKAGES.clear()
    for i in pkg_resources.working_set:
        PIP_PACKAGES[i.key.lower()] = i.version


_init_pip_packages()


def package_version(name: str) -> Optional[Version]:
    """
    Overview:
        Get version of package with given ``name``.

    :param name: Name of the package, case is not sensitive.
    :return: A :class:`packing.version.Version` object. If the package is not installed, return ``None``.

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
    _lower_name = name.lower()
    if _lower_name in PIP_PACKAGES:
        return pkg_resources.parse_version(PIP_PACKAGES[_lower_name])
    else:
        return None


def load_req_file(requirements_file: str) -> List[str]:
    """
    Overview:
        Load requirements items from a ``requirements.txt`` file.

    :param requirements_file: Requirements file.
    :return requirements: List of requirements.

    Examples::
        >>> from hbutils.system import load_req_file
        >>> load_req_file('requirements.txt')
        ['packaging>=21.3', 'setuptools>=50.0']
    """
    with pathlib.Path(requirements_file).open() as reqfile:
        return list(map(str, pkg_resources.parse_requirements(reqfile)))


def pip(*args, silent: bool = False):
    """
    Overview:
        Run pip command with code.

    :param args: Command line arguments for ``pip`` command.
    :param silent: Do not print anything. Default is false, which means print the output to ``sys.stdout`` \
        and ``sys.stderr``.

    Examples::
        >>> from hbutils.system import pip
        >>> pip('-V')
        pip 22.3.1 from /home/user/myproject/venv/lib/python3.7/site-packages/pip (python 3.7)
        >>> pip('-V', silent=True)  # nothing will be printed
    """
    try:
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
    finally:
        if args and args[0] in {'install', 'uninstall'}:
            importlib.reload(pkg_resources)
            _init_pip_packages()


def check_reqs(reqs: List[str]) -> bool:
    """
    Overview:
        Check if the given requirements are all satisfied.

    :param reqs: List of requirements.
    :return satisfied: All the requirements in ``reqs`` satisfied or not.

    Examples::
        >>> from hbutils.system import check_reqs
        >>> check_reqs(['pip>=20.0'])
        True
        >>> check_reqs(['pip~=19.2'])
        False
        >>> check_reqs(['pip>=20.0', 'setuptools>=50.0'])
        True
    """
    try:
        pkg_resources.require(reqs)
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        return False
    else:
        return True


def check_req_file(requirements_file: str) -> bool:
    """
    Overview:
        Check if the requirements in the given ``requirements_file`` is satisfied.

    :param requirements_file: Requirements file, such as ``requirements.txt``.
    :return satisfied: All the requirements in ``requirements_file`` satisfied or not.

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
    Overview:
        Pip install requirements with code.
        Similar to ``pip install req1 req2 ...``.

    :param reqs: Requirement items to install.
    :param silent: Do not print anything. Default is ``False``.
    :param force: Force execute the ``pip install`` command. Default is ``False`` which means the requirements \
        will be checked before installation, and the installation will be only executed when \
        some requirements not installed.
    :param user: User mode, represents ``--user`` option in ``pip``.

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
    Overview:
        Pip install requirements from file with code.
        Similar to ``pip install -r requirements.txt``.

    :param requirements_file: Requirements file, such as ``requirements.txt``.
    :param silent: Do not print anything. Default is ``False``.
    :param force: Force execute the ``pip install`` command. Default is ``False`` which means the requirements \
        will be checked before installation, and the installation will be only executed when \
        some requirements not installed.
    :param user: User mode, represents ``--user`` option in ``pip``.

    Examples::
        >>> from hbutils.system import pip_install_req_file
        >>> pip_install_req_file('requirements.txt')  # pip install -r requirements.txt
    """
    if force or not check_req_file(requirements_file):
        pip('install', *(('--user',) if user else ()), '-r', requirements_file, silent=silent)
