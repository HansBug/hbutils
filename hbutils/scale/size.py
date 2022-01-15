import warnings
from typing import Union

from bitmath import Byte
from bitmath import parse_string_unsafe as parse_bytes

_EPS = 1e-10


def _is_int(value: Union[int, float], stacklevel: int = 4) -> int:
    if isinstance(value, float):
        _delta = abs(value - round(value))
        if _delta >= _EPS:
            warnings.warn(UserWarning('Float detected in variable in bytes, '
                                      'rounded integer value is used.'), stacklevel=stacklevel)
        return int(round(value))
    elif isinstance(value, int):
        return value
    else:
        assert False, f"Should not reach here, {repr(type(value))} detected, " \
                      f"something may be wrong with {__name__}._is_int function."  # pragma: no cover


def _base_size_to_bytes(size, stacklevel: int = 4) -> int:
    if isinstance(size, (float, int)):
        return _is_int(size, stacklevel)
    elif isinstance(size, str):
        return _is_int(parse_bytes(size).bytes, stacklevel)
    elif isinstance(size, Byte):
        return _is_int(size.bytes, stacklevel)
    else:
        raise TypeError('{int}, {str} or {byte} expected but {actual} found.'.format(
            int=int.__name__,
            str=str.__name__,
            byte=Byte.__name__,
            actual=type(size).__name__,
        ))


def size_to_bytes(size) -> int:
    return _base_size_to_bytes(size)


def size_to_bytes_str(size) -> str:
    return str(Byte(_base_size_to_bytes(size)).best_prefix())
