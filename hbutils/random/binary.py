import random
from random import _inst as _DEFAULT_RANDOM
from typing import Optional

__all__ = [
    'random_bytes',
]


def random_bytes(length: int = 32, allow_zero: bool = False, rnd: Optional[random.Random] = None) -> bytes:
    r"""
    Overview:
        Generate random bytes.

    Arguments:
        - length (:obj:`int`): Length of bytes, default is 32.
        - allow_zero (:obj:`bool`): Allow 0x00 appear in the result, default is ``False``.
        - rnd (:obj:`Optional[random.Random]`): Random object you used, \
            default is ``None`` which means just use the default one provided by system.

    Returns:
        - bytes (:obj:`bytes`): Random bytes.

    Examples::
        >>> from hbutils.random import random_bytes
        >>> random_bytes()
        b'\xdc\xdc$\x05\x83\x04\x812\xfd\xda^\x7f[{\xbc\x99\x88*\xab3\x87}\xd1\xab\xddc\xa2p\xb2\xcb\x07\xc5'
        >>> random_bytes(64)
        b"i7\x98\xd5\x81\x1d\xdb\xd8\xe1^\xf2\xe4\xbf\xe0O^\xeb\xed\xb0i\xaa\xf3\x16Jx\xf7J\xd7\xae1\x81\xc6\xad\xd21\x15\x8aX\xb6\xc7\x85\xa4\x1c{\xac^6\xdf\x03\x94kR}\x91\x96\xfe\x06{'I\xed5\x03r"
    """
    rnd = rnd or _DEFAULT_RANDOM
    bits = []
    for i in range(length):
        if allow_zero:
            bits.append(rnd.randint(0, 0xff))
        else:
            bits.append(rnd.randint(1, 0xff))

    return bytes(bits)
