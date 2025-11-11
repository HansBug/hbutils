"""
This module provides utilities for generating random bytes with customizable options.

The module offers functionality to generate random byte sequences with control over
length, zero byte inclusion, and the random number generator used.
"""

import random
from random import _inst as _DEFAULT_RANDOM
from typing import Optional

__all__ = [
    'random_bytes',
]


def random_bytes(length: int = 32, allow_zero: bool = False, rnd: Optional[random.Random] = None) -> bytes:
    r"""
    Generate random bytes with customizable options.

    This function generates a sequence of random bytes with specified length.
    It provides options to control whether zero bytes (0x00) are allowed and
    which random number generator to use.

    :param length: Length of the byte sequence to generate, defaults to 32.
    :type length: int
    :param allow_zero: Whether to allow 0x00 to appear in the result. If False,
        only bytes from 0x01 to 0xFF will be generated. Defaults to False.
    :type allow_zero: bool
    :param rnd: Random object to use for generation. If None, uses the default
        system random number generator.
    :type rnd: Optional[random.Random]

    :return: A sequence of random bytes with the specified length.
    :rtype: bytes

    Examples::
        >>> from hbutils.random import random_bytes
        >>> random_bytes()
        b'\xdc\xdc$\x05\x83\x04\x812\xfd\xda^\x7f[{\xbc\x99\x88*\xab3\x87}\xd1\xab\xddc\xa2p\xb2\xcb\x07\xc5'
        >>> random_bytes(64)
        b"i7\x98\xd5\x81\x1d\xdb\xd8\xe1^\xf2\xe4\xbf\xe0O^\xeb\xed\xb0i\xaa\xf3\x16Jx\xf7J\xd7\xae1\x81\xc6\xad\xd21\x15\x8aX\xb6\xc7\x85\xa4\x1c{\xac^6\xdf\x03\x94kR}\x91\x96\xfe\x06{'I\xed5\x03r"
        >>> random_bytes(16, allow_zero=True)  # May contain 0x00 bytes
        b'\x00\x45\x8a\x00\xf3\x12\x67\x00\xab\xcd\xef\x00\x11\x22\x33\x44'
    """
    rnd = rnd or _DEFAULT_RANDOM
    bits = []
    for i in range(length):
        if allow_zero:
            bits.append(rnd.randint(0, 0xff))
        else:
            bits.append(rnd.randint(1, 0xff))

    return bytes(bits)
