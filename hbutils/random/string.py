"""
This module provides utilities for generating random strings in various formats.

It includes functions for creating random digits in different bases (binary, decimal, hexadecimal),
random hash strings (MD5, SHA1), random base64 strings, and timestamp-prefixed hash strings.
All functions support custom random number generators for reproducibility.

The module exports the following functions:
    - random_digits: Generate random digits in any base from 2 to 36
    - random_bin_digits: Generate random binary digits
    - random_hex_digits: Generate random hexadecimal digits
    - random_md5: Generate random MD5 hash string
    - random_sha1: Generate random SHA1 hash string
    - random_base64: Generate random base64 encoded string
    - random_md5_with_timestamp: Generate random MD5 hash with timestamp prefix
    - random_sha1_with_timestamp: Generate random SHA1 hash with timestamp prefix
"""
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
    """
    Validate that the base is a valid integer between 2 and 36 inclusive.

    :param base: The base to validate.
    :type base: int
    :raises ValueError: If base is less than 2 or greater than 36.
    :raises TypeError: If base is not an integer.
    """
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
    """
    Generate a single random digit character in the specified base.

    :param base: The base for the digit (2-36).
    :type base: int
    :param upper: Whether to use uppercase letters for bases > 10.
    :type upper: bool
    :param rnd: Random number generator instance.
    :type rnd: random.Random
    :return: A single character representing a digit in the specified base.
    :rtype: str
    """
    _val = rnd.randint(0, base - 1)
    if _val < 10:
        _base = _0_ASCII
    elif upper:
        _base = _UPPER_A_ASCII - 10
    else:
        _base = _LOWER_A_ASCII - 10

    return chr(_base + _val)


def random_digits(length: int = 32, base: int = 10, upper: bool = False, rnd: Optional[random.Random] = None) -> str:
    """
    Create random digits in the specified base.

    :param length: Length of the digits, default is 32.
    :type length: int
    :param base: Base of the digits, should be in [2, 36], default is 10.
    :type base: int
    :param upper: Upper the hex chars, default is ``False``.
    :type upper: bool
    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Random digital string.
    :rtype: str

    Examples::
        >>> from hbutils.random import random_digits
        >>> random_digits()
        '53518555004529024184262875530824'
        >>> random_digits(base=8)
        '77337055655313664176450107031511'
        >>> random_digits(48, base=8)
        '130107050101775254773050732461131017135371516420'
    """
    _check_base(base)
    rnd = rnd or _DEFAULT_RANDOM

    with io.StringIO() as sio:
        for i in range(length):
            sio.write(_random_dchar(base, upper, rnd))

        return sio.getvalue()


def random_bin_digits(length: int = 32, rnd: Optional[random.Random] = None) -> str:
    """
    Create random binary digits.

    :param length: Length of the digits, default is 32.
    :type length: int
    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Random binary digital string.
    :rtype: str

    Examples::
        >>> from hbutils.random import random_bin_digits
        >>> random_bin_digits()
        '11001011010101101100011010010011'
        >>> random_bin_digits(48)
        '010110000110101101111111011100010011101011010100'
    """
    return random_digits(length, 2, False, rnd)


def random_hex_digits(length: int = 32, upper: bool = False, rnd: Optional[random.Random] = None) -> str:
    """
    Create random hexadecimal digits.

    :param length: Length of the digits, default is 32.
    :type length: int
    :param upper: Whether to use uppercase letters, default is ``False``.
    :type upper: bool
    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Random hexadecimal digital string.
    :rtype: str

    Examples::
        >>> from hbutils.random import random_hex_digits
        >>> random_hex_digits()
        'bf4eadfb8c1700d74024833c3ce211a7'
        >>> random_hex_digits(upper=True)
        '7B85DE69A319BA132ACA27C7777A1C3E'
        >>> random_hex_digits(48)
        '7175a23730391687b7b5230c72d702a1664833a1c66783cc'
    """
    return random_digits(length, 16, upper, rnd)


_RANDOM_BYTES_LENGTH = 64


def _random_hash(hash_func, length: int = _RANDOM_BYTES_LENGTH, rnd: Optional[random.Random] = None):
    """
    Generate a random hash string using the specified hash function.

    :param hash_func: The hash function to apply to random bytes.
    :type hash_func: callable
    :param length: Length of random bytes to generate, default is 64.
    :type length: int
    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Hash string generated from random bytes.
    :rtype: str
    """
    return hash_func(random_bytes(length, allow_zero=False, rnd=rnd))


def random_md5(rnd: Optional[random.Random] = None) -> str:
    """
    Create random md5 string.

    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Random md5 string.
    :rtype: str

    Examples::
        >>> from hbutils.random import random_md5
        >>> random_md5()
        'bbffd8913a7c49161ebe31b9092a9016'
    """
    return _random_hash(md5, _RANDOM_BYTES_LENGTH, rnd)


def random_sha1(rnd: Optional[random.Random] = None) -> str:
    """
    Create random sha1 string.

    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Random sha1 string.
    :rtype: str

    Examples::
        >>> from hbutils.random import random_sha1
        >>> random_sha1()
        '13135aa6b05482dcdbc1f5a25d117298571e7fab'
    """
    return _random_hash(sha1, _RANDOM_BYTES_LENGTH, rnd)


def random_base64(length: int = _RANDOM_BYTES_LENGTH, rnd: Optional[random.Random] = None) -> str:
    """
    Create random base64 string, may be useful when matrix verification code.

    :param length: Length of the original binary data, default is 64.
    :type length: int
    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Random base64 string.
    :rtype: str

    Examples::
        >>> from hbutils.random import random_base64
        >>> random_base64()
        'PJZzHkM2-DpeXn1W9b3rp0I66MnOeD-31d2XYTA3va7N8DSNmQgvIINnvDMKWaRW-WHo_ftgKHg40z7XbDupbg=='
        >>> random_base64(48)
        'siRZNSeytSUXlIgKYuZOzbhehhI7oabcxFDB07PkjyZ5b0DI5hGC0pqjJFlD6NGQ'
    """
    return _random_hash(partial(base64_encode, urlsafe=True), length, rnd)


def _timestamp():
    """
    Get current timestamp in the format 'YYYYMMDDHHMMSSffffff'.

    :return: Formatted timestamp string.
    :rtype: str
    """
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def random_md5_with_timestamp(rnd: Optional[random.Random] = None) -> str:
    """
    Create random md5 string with timestamp prefix.

    The format is '{timestamp}_{md5}' where timestamp is in 'YYYYMMDDHHMMSSffffff' format.

    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Random md5 string with timestamp prefix.
    :rtype: str

    Examples::
        >>> from hbutils.random import random_md5_with_timestamp
        >>> random_md5_with_timestamp()
        '20220116233104357175_daf67fde4b758ff4aae21cc77f5ed689'
    """
    return f'{_timestamp()}_{random_md5(rnd)}'


def random_sha1_with_timestamp(rnd: Optional[random.Random] = None) -> str:
    """
    Create random sha1 string with timestamp prefix.

    The format is '{timestamp}_{sha1}' where timestamp is in 'YYYYMMDDHHMMSSffffff' format.

    :param rnd: Random object you used, default is ``None`` which means just use the default one provided by system.
    :type rnd: Optional[random.Random]
    :return: Random sha1 string with timestamp prefix.
    :rtype: str

    Examples::
        >>> from hbutils.random import random_sha1_with_timestamp
        >>> random_sha1_with_timestamp()
        '20220116233121916685_fba840b80163b55cd2295d84286a438bf8acb7c0'
    """
    return f'{_timestamp()}_{random_sha1(rnd)}'
