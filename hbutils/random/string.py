import io
import random
from datetime import datetime
from functools import partial
from random import _inst as _DEFAULT_RANDOM
from typing import Optional

from .binary import random_bytes
from ..encoding import md5, sha1, base64_encode

__all__ = [
    'random_digits', 'random_bin_digits', 'random_hex_digits',
    'random_md5', 'random_sha1', 'random_base64',
    'random_md5_with_timestamp', 'random_sha1_with_timestamp',
]


def _check_base(base: int):
    if base < 2:
        raise ValueError(f'Base should be an integer no less than 2, but {repr(base)} found.')
    elif base > 36:
        raise ValueError(f'Base should be an integer no greater then 36, but {repr(base)} found.')
    elif not isinstance(base, int):
        raise TypeError(f'Base should be an integer, but {repr(type(base))} found.')


_0_ASCII = ord('0')
_LOWER_A_ASCII = ord('a')
_UPPER_A_ASCII = ord('A')


def _random_dchar(base: int, upper: bool, rnd: random.Random):
    _val = rnd.randint(0, base - 1)
    if _val < 10:
        _base = _0_ASCII
    elif upper:
        _base = _UPPER_A_ASCII - 10
    else:
        _base = _LOWER_A_ASCII - 10

    return chr(_base + _val)


def random_digits(length: int = 32, base: int = 10, upper: bool = False, rnd: Optional[random.Random] = None):
    _check_base(base)
    rnd = rnd or _DEFAULT_RANDOM

    with io.StringIO() as sio:
        for i in range(length):
            sio.write(_random_dchar(base, upper, rnd))

        return sio.getvalue()


def random_bin_digits(length: int = 32, rnd: Optional[random.Random] = None):
    return random_digits(length, 2, False, rnd)


def random_hex_digits(length: int = 32, upper: bool = False, rnd: Optional[random.Random] = None):
    return random_digits(length, 16, upper, rnd)


_RANDOM_BYTES_LENGTH = 64


def _random_hash(hash_func, length: int = _RANDOM_BYTES_LENGTH, rnd: Optional[random.Random] = None):
    return hash_func(random_bytes(length, allow_zero=False, rnd=rnd))


def random_md5(rnd: Optional[random.Random] = None):
    return _random_hash(md5, _RANDOM_BYTES_LENGTH, rnd)


def random_sha1(rnd: Optional[random.Random] = None):
    return _random_hash(sha1, _RANDOM_BYTES_LENGTH, rnd)


def random_base64(length: int = _RANDOM_BYTES_LENGTH, rnd: Optional[random.Random] = None):
    return _random_hash(partial(base64_encode, urlsafe=True), length, rnd)


def _timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def random_md5_with_timestamp(rnd: Optional[random.Random] = None):
    return f'{_timestamp()}_{random_md5(rnd)}'


def random_sha1_with_timestamp(rnd: Optional[random.Random] = None):
    return f'{_timestamp()}_{random_sha1(rnd)}'
