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
    'load_req_file', 'pip', 'pip_install',
    'check_reqs', 'check_req_file',
]

PIP_PACKAGES: Dict[str, str] = {}


def _get_pip_pakages() -> Dict[str, str]:
    global PIP_PACKAGES
    if not PIP_PACKAGES:
        for i in pkg_resources.working_set:
            PIP_PACKAGES[i.key.lower()] = i.version

    return PIP_PACKAGES


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
    pip_packages = _get_pip_pakages()
    if _lower_name in pip_packages:
        return pkg_resources.parse_version(pip_packages[_lower_name])
    else:
        return None


def load_req_file(requirements_file: str) -> List[str]:
    with pathlib.Path(requirements_file).open() as reqfile:
        return list(map(str, pkg_resources.parse_requirements(reqfile)))


def pip(*args, silent: bool = False):
    with open(os.devnull, 'w') as sout:
        try:
            process = subprocess.run(
                [sys.executable, '-m', 'pip', *args],
                stdin=sys.stdin if not silent else None,
                stdout=sys.stdout if not silent else sout,
                stderr=sys.stderr if not silent else sout,
            )
            process.check_returncode()
        finally:
            if args and args[0] in {'install', 'uninstall'}:
                importlib.reload(pkg_resources)
                global PIP_PACKAGES
                PIP_PACKAGES.clear()


def check_reqs(reqs: List[str]) -> bool:
    try:
        pkg_resources.require(reqs)
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        return False
    else:
        return True


def check_req_file(requirements_file: str) -> bool:
    return check_reqs(load_req_file(requirements_file))


def pip_install(reqs: List[str], silent: bool = False, force: bool = False):
    if force or not check_reqs(reqs):
        pip('install', *reqs, silent=silent)
