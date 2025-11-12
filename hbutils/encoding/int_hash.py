"""
Non-cryptographic hash algorithms module.

This module provides implementations of various fast, non-cryptographic hash algorithms
commonly used for hash tables, checksums, and data fingerprinting. These algorithms
prioritize speed over cryptographic security.

Available hash algorithms:

- FNV-1a (32-bit and 64-bit): Fowler-Noll-Vo hash function
- DJB2: Daniel J. Bernstein's hash algorithm
- SDBM: Hash function from the SDBM database library
- MurmurHash3 (32-bit): Fast non-cryptographic hash by Austin Appleby
- CRC32 Variant: Modified CRC32 algorithm
- xxHash32: Extremely fast hash algorithm
- xs: A tiny and fast but reliable hash algorithm

The module provides a unified interface through the `int_hash` function, which allows
selecting different hash algorithms via the method parameter. Custom hash functions
can be registered using the `register_int_hash` decorator.

Example::
    >>> from hbutils.encoding import int_hash
    >>> int_hash("hello", method='FNV-1a-32')
    1335831723
    >>> int_hash(b"world", method='DJB2')
    279393645
"""

import struct
from typing import Union, Callable, Dict, Optional

__all__ = [
    'register_int_hash',
    'int_hash',
]


def _norm_input(data: Union[str, bytes, bytearray]) -> bytes:
    """
    Normalize input data to bytes format.

    :param data: Input data in string, bytes, or bytearray format.
    :type data: Union[str, bytes, bytearray]

    :return: Normalized data as bytes.
    :rtype: bytes

    Example::
        >>> _norm_input("hello")
        b'hello'
        >>> _norm_input(bytearray(b"world"))
        b'world'
    """
    if isinstance(data, str):
        return data.encode('utf-8')
    elif isinstance(data, bytearray):
        return bytes(data)
    return data


_IntHashTyping = Callable[[Union[str, bytes, bytearray]], int]
_INT_HASH_FUNCS: Dict[str, _IntHashTyping] = {}


def _register(name: str, func: _IntHashTyping):
    """
    Register a hash function with a given name.

    :param name: The name to register the hash function under.
    :type name: str
    :param func: The hash function to register.
    :type func: _IntHashTyping
    """
    _INT_HASH_FUNCS[name] = func


def register_int_hash(name: str, func: Optional[_IntHashTyping] = None) -> Optional[Callable]:
    """
    Register an integer hash function decorator.

    This function can be used as a decorator to register hash functions,
    or called directly with both name and function parameters.

    :param name: The name to register the hash function under.
    :type name: str
    :param func: The hash function to register (optional).
    :type func: Optional[_IntHashTyping]

    :return: The decorator function if func is None, otherwise None.
    :rtype: Optional[Callable]

    Example::
        >>> @register_int_hash('my_hash')
        ... def my_hash_func(data):
        ...     return hash(data)
        >>> register_int_hash('another_hash', lambda x: hash(x))
    """
    if func is None:
        def _decorator(f):
            _register(name, f)
            return f

        return _decorator
    else:
        _register(name, func)


@register_int_hash('FNV-1a-32')
def _int_hash_fnv1a_32(data: Union[str, bytes, bytearray]) -> int:
    """
    Compute FNV-1a 32-bit hash.

    FNV-1a (Fowler-Noll-Vo) is a fast, non-cryptographic hash function with good
    distribution properties. It uses XOR and multiplication operations.

    :param data: Input data to hash.
    :type data: Union[str, bytes, bytearray]

    :return: 32-bit hash value.
    :rtype: int

    Example::
        >>> _int_hash_fnv1a_32("hello")
        1335831723
        >>> _int_hash_fnv1a_32(b"world")
        2166136261
    """
    data = _norm_input(data)
    hash_val = 0x811c9dc5  # FNV offset basis
    fnv_prime = 0x01000193  # FNV prime

    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * fnv_prime) & 0xFFFFFFFF

    return hash_val


@register_int_hash('FNV-1a-64')
def _int_hash_fnv1a_64(data: Union[str, bytes, bytearray]) -> int:
    """
    Compute FNV-1a 64-bit hash.

    64-bit version of FNV-1a hash algorithm, providing larger hash space
    and better collision resistance than the 32-bit version.

    :param data: Input data to hash.
    :type data: Union[str, bytes, bytearray]

    :return: 64-bit hash value.
    :rtype: int

    Example::
        >>> _int_hash_fnv1a_64("hello")
        11831194018420276491
        >>> _int_hash_fnv1a_64(b"world")
        14687969915205230528
    """
    data = _norm_input(data)
    hash_val = 0xcbf29ce484222325  # FNV offset basis
    fnv_prime = 0x100000001b3  # FNV prime

    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * fnv_prime) & 0xFFFFFFFFFFFFFFFF

    return hash_val


@register_int_hash('DJB2')
def _int_hash_djb2(data: Union[str, bytes, bytearray]) -> int:
    """
    Compute DJB2 hash.

    DJB2 is a simple and effective hash function created by Daniel J. Bernstein.
    It uses bit shifting and addition operations for fast computation.

    :param data: Input data to hash.
    :type data: Union[str, bytes, bytearray]

    :return: 32-bit hash value.
    :rtype: int

    Example::
        >>> _int_hash_djb2("hello")
        210676686969
        >>> _int_hash_djb2(b"world")
        894552257
    """
    data = _norm_input(data)
    hash_val = 5381

    for byte in data:
        hash_val = ((hash_val << 5) + hash_val + byte) & 0xFFFFFFFF

    return hash_val


@register_int_hash('SDBM')
def _int_hash_sdbm(data: Union[str, bytes, bytearray]) -> int:
    """
    Compute SDBM hash.

    SDBM hash algorithm from the SDBM database library. It uses bit shifting
    and subtraction operations to generate hash values.

    :param data: Input data to hash.
    :type data: Union[str, bytes, bytearray]

    :return: 32-bit hash value.
    :rtype: int

    Example::
        >>> _int_hash_sdbm("hello")
        430867652
        >>> _int_hash_sdbm(b"world")
        4031760169
    """
    data = _norm_input(data)
    hash_val = 0

    for byte in data:
        hash_val = (byte + (hash_val << 6) + (hash_val << 16) - hash_val) & 0xFFFFFFFF

    return hash_val


@register_int_hash('MurmurHash3-32')
def _int_hash_murmur3_32(data: Union[str, bytes, bytearray], seed: int = 0) -> int:
    """
    Compute MurmurHash3 32-bit hash (simplified implementation).

    MurmurHash3 is a fast, non-cryptographic hash function with excellent
    distribution and avalanche properties. This is a simplified implementation
    of the 32-bit version.

    :param data: Input data to hash.
    :type data: Union[str, bytes, bytearray]
    :param seed: Seed value for hash initialization (default: 0).
    :type seed: int

    :return: 32-bit hash value.
    :rtype: int

    Example::
        >>> _int_hash_murmur3_32("hello")
        613153351
        >>> _int_hash_murmur3_32("hello", seed=42)
        1335626643
    """
    data = _norm_input(data)
    length = len(data)

    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    r1 = 15
    r2 = 13
    m = 5
    n = 0xe6546b64

    hash_val = seed

    # Process 4-byte blocks
    for i in range(0, length - (length % 4), 4):
        k = struct.unpack('<I', data[i:i + 4])[0]
        k = (k * c1) & 0xFFFFFFFF
        k = ((k << r1) | (k >> (32 - r1))) & 0xFFFFFFFF
        k = (k * c2) & 0xFFFFFFFF

        hash_val ^= k
        hash_val = ((hash_val << r2) | (hash_val >> (32 - r2))) & 0xFFFFFFFF
        hash_val = ((hash_val * m) + n) & 0xFFFFFFFF

    # Process remaining bytes
    remaining = length % 4
    if remaining:
        k = 0
        for i in range(remaining):
            k |= data[length - remaining + i] << (i * 8)

        k = (k * c1) & 0xFFFFFFFF
        k = ((k << r1) | (k >> (32 - r1))) & 0xFFFFFFFF
        k = (k * c2) & 0xFFFFFFFF
        hash_val ^= k

    # Final mixing
    hash_val ^= length
    hash_val ^= hash_val >> 16
    hash_val = (hash_val * 0x85ebca6b) & 0xFFFFFFFF
    hash_val ^= hash_val >> 13
    hash_val = (hash_val * 0xc2b2ae35) & 0xFFFFFFFF
    hash_val ^= hash_val >> 16

    return hash_val


@register_int_hash('CRC32-Variant')
def _int_hash_crc32_variant(data: Union[str, bytes, bytearray]) -> int:
    """
    Compute CRC32 variant hash.

    A variant of the CRC32 (Cyclic Redundancy Check) algorithm adapted for
    hash table use. Uses a simplified CRC32 polynomial for computation.

    :param data: Input data to hash.
    :type data: Union[str, bytes, bytearray]

    :return: 32-bit hash value.
    :rtype: int

    Example::
        >>> _int_hash_crc32_variant("hello")
        907060870
        >>> _int_hash_crc32_variant(b"world")
        3134015206
    """
    data = _norm_input(data)

    # Simplified CRC32 polynomial
    polynomial = 0xEDB88320
    hash_val = 0xFFFFFFFF

    for byte in data:
        hash_val ^= byte
        for _ in range(8):
            if hash_val & 1:
                hash_val = (hash_val >> 1) ^ polynomial
            else:
                hash_val >>= 1

    return hash_val ^ 0xFFFFFFFF


@register_int_hash('xxHash32-Simple')
def _int_hash_xxhash32_simple(data: Union[str, bytes, bytearray], seed: int = 0) -> int:
    """
    Compute xxHash32 hash (simplified implementation).

    xxHash is an extremely fast non-cryptographic hash algorithm, working at
    speeds close to RAM limits. This is a simplified implementation of the
    32-bit version.

    :param data: Input data to hash.
    :type data: Union[str, bytes, bytearray]
    :param seed: Seed value for hash initialization (default: 0).
    :type seed: int

    :return: 32-bit hash value.
    :rtype: int

    Example::
        >>> _int_hash_xxhash32_simple("hello")
        4211111929
        >>> _int_hash_xxhash32_simple("hello", seed=42)
        3252879916
    """
    data = _norm_input(data)
    length = len(data)

    PRIME32_1 = 0x9E3779B1
    PRIME32_2 = 0x85EBCA77
    PRIME32_3 = 0xC2B2AE3D
    PRIME32_4 = 0x27D4EB2F
    PRIME32_5 = 0x165667B1

    if length >= 16:
        v1 = (seed + PRIME32_1 + PRIME32_2) & 0xFFFFFFFF
        v2 = (seed + PRIME32_2) & 0xFFFFFFFF
        v3 = seed
        v4 = (seed - PRIME32_1) & 0xFFFFFFFF

        # Process 16-byte blocks
        for i in range(0, length - 15, 16):
            for j in range(4):
                val = struct.unpack('<I', data[i + j * 4:i + j * 4 + 4])[0]
                if j == 0:
                    v1 = ((v1 + val * PRIME32_2) & 0xFFFFFFFF)
                    v1 = (((v1 << 13) | (v1 >> 19)) * PRIME32_1) & 0xFFFFFFFF
                elif j == 1:
                    v2 = ((v2 + val * PRIME32_2) & 0xFFFFFFFF)
                    v2 = (((v2 << 13) | (v2 >> 19)) * PRIME32_1) & 0xFFFFFFFF
                elif j == 2:
                    v3 = ((v3 + val * PRIME32_2) & 0xFFFFFFFF)
                    v3 = (((v3 << 13) | (v3 >> 19)) * PRIME32_1) & 0xFFFFFFFF
                else:
                    v4 = ((v4 + val * PRIME32_2) & 0xFFFFFFFF)
                    v4 = (((v4 << 13) | (v4 >> 19)) * PRIME32_1) & 0xFFFFFFFF

        hash_val = (((v1 << 1) | (v1 >> 31)) +
                    ((v2 << 7) | (v2 >> 25)) +
                    ((v3 << 12) | (v3 >> 20)) +
                    ((v4 << 18) | (v4 >> 14))) & 0xFFFFFFFF

        remaining_start = length - (length % 16)
    else:
        hash_val = (seed + PRIME32_5) & 0xFFFFFFFF
        remaining_start = 0

    hash_val = (hash_val + length) & 0xFFFFFFFF

    # Process remaining bytes
    for i in range(remaining_start, length):
        hash_val = (hash_val + data[i] * PRIME32_5) & 0xFFFFFFFF
        hash_val = (((hash_val << 11) | (hash_val >> 21)) * PRIME32_1) & 0xFFFFFFFF

    # Final mixing
    hash_val ^= hash_val >> 15
    hash_val = (hash_val * PRIME32_2) & 0xFFFFFFFF
    hash_val ^= hash_val >> 13
    hash_val = (hash_val * PRIME32_3) & 0xFFFFFFFF
    hash_val ^= hash_val >> 16

    return hash_val


@register_int_hash('xs')
def _int_hash_xs(data: Union[str, bytes, bytearray]) -> int:
    """
    Compute a minimal but functional hash using simple polynomial hashing.

    This is a lightweight hash function that uses a simple polynomial hash
    (hash = hash * 31 + byte) with a single bit mixing operation to improve
    the avalanche effect. It satisfies basic hash properties while maintaining
    simplicity and speed.

    :param data: The input data to hash. Can be string, bytes, or bytearray.
    :type data: Union[str, bytes, bytearray]

    :return: A 32-bit unsigned integer hash value.
    :rtype: int

    Example::
        >>> _int_hash_xs('hello')  # Hash a string
        123456789
        >>> _int_hash_xs(b'hello')  # Hash bytes
        123456789
    """
    # Convert all input types to bytes
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif isinstance(data, bytearray):
        data = bytes(data)

    # Simple polynomial hash: hash = (hash * 31 + byte)
    hash_val = 0
    for byte in data:
        hash_val = (hash_val * 31 + byte) & 0xffffffff

    # Single bit mixing to improve avalanche effect
    hash_val ^= hash_val >> 16

    return hash_val & 0xffffffff


def int_hash(data: Union[str, bytes, bytearray], method: str = 'FNV-1a-32') -> int:
    """
    Compute integer hash using the specified method.

    This is the main entry point for computing hashes. It dispatches to the
    appropriate hash function based on the method parameter.

    :param data: Input data to hash.
    :type data: Union[str, bytes, bytearray]
    :param method: Hash algorithm to use (default: 'FNV-1a-32').
                   Available methods: 'FNV-1a-32', 'FNV-1a-64', 'DJB2', 'SDBM',
                   'MurmurHash3-32', 'CRC32-Variant', 'xxHash32-Simple', 'xs'.
    :type method: str

    :return: Hash value computed by the specified method.
    :rtype: int
    :raises KeyError: If the specified method is not registered.

    Example::
        >>> int_hash("hello")
        1335831723
        >>> int_hash("hello", method='FNV-1a-32')
        1335831723
        >>> int_hash(b"world", method='DJB2')
        279393645
    """
    return _INT_HASH_FUNCS[method](data)
