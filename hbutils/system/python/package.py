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
    _packages = _get_packages()
    _name = name.lower()
    if _name in _packages:
        return parse_version(_packages[name])
    else:
        return None
