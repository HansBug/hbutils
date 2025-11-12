from typing import Union

import pytest

from hbutils.encoding import int_hash_val_comprehensive


def minimal_good_hash(data: Union[str, bytes, bytearray]) -> int:
    """
    A minimal but functional hash function that satisfies basic hash properties.

    Uses a simple polynomial hash with a single bit mixing operation to improve
    avalanche effect.

    :param data: The input data to hash. Can be string, bytes, or bytearray.
    :type data: Union[str, bytes, bytearray]

    :return: A 32-bit unsigned integer hash value.
    :rtype: int

    Example::
        >>> minimal_good_hash('hello')  # Hash a string
        123456789
        >>> minimal_good_hash(b'hello')  # Hash bytes
        123456789
    """
    # Convert all input types to bytes
    if isinstance(data, str):
        data = data.encode("utf-8")
    elif isinstance(data, bytearray):
        data = bytes(data)

    # Simple polynomial hash: hash = (hash * 31 + byte)
    hash_val = 0
    for byte in data:
        hash_val = (hash_val * 31 + byte) & 0xFFFFFFFF

    # Single bit mixing to improve avalanche effect
    hash_val ^= hash_val >> 16

    return hash_val & 0xFFFFFFFF


def basic_good_hash(data: Union[str, bytes, bytearray]) -> int:
    """
    A basic hash function that satisfies fundamental hash properties.

    Uses a simple polynomial rolling hash with bit operations to provide
    better distribution and avalanche effect than minimal_good_hash.

    :param data: The input data to hash. Can be string, bytes, or bytearray.
    :type data: Union[str, bytes, bytearray]

    :return: A 32-bit unsigned integer hash value.
    :rtype: int

    Example::
        >>> basic_good_hash('test')  # Hash a string
        987654321
        >>> basic_good_hash(b'test')  # Hash bytes
        987654321
    """
    # Convert all input types to bytes
    if isinstance(data, str):
        data = data.encode("utf-8")
    elif isinstance(data, bytearray):
        data = bytes(data)

    hash_val = 0x811C9DC5  # FNV offset basis (32-bit)

    for byte in data:
        # Simple polynomial hash variant
        hash_val = ((hash_val * 33) ^ byte) & 0xFFFFFFFF
        # Add some bit mixing
        hash_val ^= hash_val >> 16
        hash_val = (hash_val * 0x85EBCA6B) & 0xFFFFFFFF
        hash_val ^= hash_val >> 13

    return hash_val & 0xFFFFFFFF


def bad_hash_constant(data: Union[str, bytes, bytearray]) -> int:
    """
    Bad hash function #1: Always returns a constant value.

    This violates: uniform distribution, collision resistance, and avalanche effect.
    Every input produces the same output, making it useless as a hash function.

    :param data: The input data (ignored).
    :type data: Union[str, bytes, bytearray]

    :return: Always returns 42.
    :rtype: int

    Example::
        >>> bad_hash_constant('anything')  # Always returns 42
        42
        >>> bad_hash_constant('different')  # Still returns 42
        42
    """
    return 42


def bad_hash_length_only(data: Union[str, bytes, bytearray]) -> int:
    """
    Bad hash function #2: Hash based only on input length.

    This violates: collision resistance and avalanche effect.
    Any inputs with the same length produce the same hash value.

    :param data: The input data to measure.
    :type data: Union[str, bytes, bytearray]

    :return: The length of the input data in bytes.
    :rtype: int

    Example::
        >>> bad_hash_length_only('abc')  # Returns 3
        3
        >>> bad_hash_length_only('xyz')  # Also returns 3
        3
    """
    if isinstance(data, str):
        return len(data.encode("utf-8"))
    return len(data)


def bad_hash_first_byte(data: Union[str, bytes, bytearray]) -> int:
    """
    Bad hash function #3: Uses only the first byte of input.

    This violates: avalanche effect and collision resistance.
    Changes to any byte except the first do not affect the hash value.

    :param data: The input data.
    :type data: Union[str, bytes, bytearray]

    :return: The value of the first byte, or 0 if input is empty.
    :rtype: int

    Example::
        >>> bad_hash_first_byte('abc')  # Returns ASCII value of 'a'
        97
        >>> bad_hash_first_byte('axy')  # Also returns 97
        97
        >>> bad_hash_first_byte('')  # Empty input returns 0
        0
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    elif isinstance(data, bytearray):
        data = bytes(data)

    if len(data) == 0:
        return 0
    return data[0]


def bad_hash_simple_sum(data: Union[str, bytes, bytearray]) -> int:
    """
    Bad hash function #4: Simple sum of all bytes.

    This violates: avalanche effect (byte order doesn't matter) and collision resistance.
    Anagrams and permutations of the same bytes produce identical hash values.

    :param data: The input data.
    :type data: Union[str, bytes, bytearray]

    :return: The sum of all byte values, masked to 32 bits.
    :rtype: int

    Example::
        >>> bad_hash_simple_sum('abc')  # Sum of ASCII values
        294
        >>> bad_hash_simple_sum('cba')  # Same sum, different order
        294
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    elif isinstance(data, bytearray):
        data = bytes(data)

    return sum(data) & 0xFFFFFFFF


def bad_hash_type_inconsistent(data: Union[str, bytes, bytearray]) -> int:
    """
    Bad hash function #5: Type-inconsistent hashing.

    This violates: type consistency.
    Uses different algorithms for different input types, so equivalent data
    in different formats produces different hash values.

    :param data: The input data.
    :type data: Union[str, bytes, bytearray]

    :return: Hash value computed using different algorithms based on input type.
    :rtype: int

    Example::
        >>> bad_hash_type_inconsistent('test')  # String algorithm
        123456
        >>> bad_hash_type_inconsistent(b'test')  # Bytes algorithm (different result)
        789012
    """
    if isinstance(data, str):
        # Use one algorithm for strings
        return hash(data) & 0xFFFFFFFF
    elif isinstance(data, bytes):
        # Use another algorithm for bytes
        return sum(data) & 0xFFFFFFFF
    elif isinstance(data, bytearray):
        # Use a third algorithm for bytearray
        return len(data) * 17 & 0xFFFFFFFF
    else:
        return 0


def bad_hash_non_deterministic(data: Union[str, bytes, bytearray]) -> int:
    """
    Bad hash function #6: Non-deterministic hashing.

    This violates: determinism, type consistency, and empty input handling.
    Returns different values for the same input on different calls due to
    random numbers and time-based factors.

    :param data: The input data.
    :type data: Union[str, bytes, bytearray]

    :return: A hash value that varies with each call due to randomness and time.
    :rtype: int

    Example::
        >>> bad_hash_non_deterministic('test')  # First call
        123456789
        >>> bad_hash_non_deterministic('test')  # Second call (different result)
        987654321
    """
    import random
    import time

    # Based on current time and random number, result differs each call
    base_hash = hash(str(data)) & 0xFFFFFFFF
    random_factor = random.randint(0, 1000)
    time_factor = int(time.time() * 1000000) & 0xFF

    return (base_hash + random_factor + time_factor) & 0xFFFFFFFF


@pytest.mark.unittest
class TestEncodingIntHashVal:
    @pytest.mark.parametrize(
        ["func", "passed", "properties"],
        [
            (minimal_good_hash, True, []),
            (basic_good_hash, True, []),
            (
                    bad_hash_constant,
                    False,
                    ["avalanche_effect", "uniform_distribution", "collision_resistance"],
            ),
            (bad_hash_length_only, False, ["avalanche_effect", "collision_resistance"]),
            (bad_hash_first_byte, False, ["avalanche_effect", "collision_resistance"]),
            (bad_hash_simple_sum, False, ["avalanche_effect", "collision_resistance"]),
            (bad_hash_type_inconsistent, False, ["type_consistency"]),
            (
                    bad_hash_non_deterministic,
                    False,
                    ["determinism", "type_consistency", "empty_input"],
            ),
        ],
    )
    def test_int_hash_val_comprehensive(self, func, passed, properties):
        result = int_hash_val_comprehensive(func)
        assert result["passed"] == passed
        assert result["not_passed_properties"] == properties
