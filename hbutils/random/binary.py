import random
from random import _inst as _DEFAULT_RANDOM
from typing import Optional

__all__ = [
    'random_bytes',
]


def random_bytes(length: int = 32, allow_zero: bool = False, rnd: Optional[random.Random] = None) -> bytes:
    rnd = rnd or _DEFAULT_RANDOM
    bits = []
    for i in range(length):
        if allow_zero:
            bits.append(rnd.randint(0, 0xff))
        else:
            bits.append(rnd.randint(1, 0xff))

    return bytes(bits)
