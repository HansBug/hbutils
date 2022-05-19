import platform
from enum import IntEnum, unique
from functools import lru_cache

from ...model import int_enum_loads

__all__ = [
    'is_cpython',
    'is_ironpython',
    'is_jython',
    'is_pypy',
]


@int_enum_loads(name_preprocess=str.upper)
@unique
class PythonImplementation(IntEnum):
    CPYTHON = 1
    IRONPYTHON = 2
    JYTHON = 3
    PYPY = 4


@lru_cache()
def _get_python_implementation() -> PythonImplementation:
    return PythonImplementation.loads(platform.python_implementation())


def is_cpython() -> bool:
    return _get_python_implementation() == PythonImplementation.CPYTHON


def is_ironpython() -> bool:
    return _get_python_implementation() == PythonImplementation.IRONPYTHON


def is_jython() -> bool:
    return _get_python_implementation() == PythonImplementation.JYTHON


def is_pypy() -> bool:
    return _get_python_implementation() == PythonImplementation.PYPY
