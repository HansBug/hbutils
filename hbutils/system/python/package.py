from typing import Dict, Optional

from packaging.version import Version
from pkg_resources import working_set, parse_version

__all__ = [
    'package_version',
]


def _get_packages() -> Dict[str, Version]:
    return {
        i.key.lower(): i.version
        for i in working_set
    }


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
    _packages = _get_packages()
    _name = name.lower()
    if _name in _packages:
        return parse_version(_packages[name])
    else:
        return None
