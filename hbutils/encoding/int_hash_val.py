"""
This module provides comprehensive validation utilities for hash functions, including tests for:

- Determinism: Ensures consistent output for the same input
- Type consistency: Validates consistent hashing across different input types
- Avalanche effect: Measures how small input changes affect output
- Uniform distribution: Analyzes hash value distribution patterns
- Collision resistance: Tests for hash collisions
- Empty input handling: Validates behavior with empty inputs
- Performance characteristics: Measures hashing speed and throughput

The module is designed to validate integer-based hash functions that accept
string, bytes, or bytearray inputs and return integer hash values.

Example::
    >>> from hbutils.encoding import int_hash_val_comprehensive
    >>>
    >>> print(int_hash_val_comprehensive('xs'))  # validate existing hash functions
    ╔══════════════════════════════════════════════════════════════════════════════════════════════╗
    ║                          COMPREHENSIVE HASH FUNCTION VALIDATION REPORT                       ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║ Function Name:     xs               │ Overall Status:    PASS                                ║
    ║ Properties Tested: 7                │ Properties Passed: 7    (100.0%)                       ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║                                    PROPERTY STATUS                                           ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║ ✓ Determinism                                   │ PASS                                       ║
    ║ ✓ Type Consistency                              │ PASS                                       ║
    ║ ✓ Avalanche Effect                              │ PASS       | Avalanche Effect:       42.9% ║
    ║ ✓ Uniform Distribution                          │ PASS       | Uniformity Score:       0.996 ║
    ║ ✓ Collision Resistance                          │ PASS       | Collision Rate:        0.0000 ║
    ║ ✓ Empty Input                                   │ PASS                                       ║
    ║ ✓ Performance                                   │ PASS       | Avg Throughput:      4.6 MB/s ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║                                   RECOMMENDATIONS                                            ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║ ✓ Hash function meets all validation criteria - suitable for production use                  ║
    ╚══════════════════════════════════════════════════════════════════════════════════════════════╝
    DETAILED ANALYSIS:
    • All validation tests passed successfully
    • Hash function demonstrates good cryptographic properties
    • Suitable for general-purpose hashing applications
    >>>
    >>> def basic_good_hash(data) -> int:
    ...     # Convert all input types to bytes
    ...     if isinstance(data, str):
    ...         data = data.encode('utf-8')
    ...     elif isinstance(data, bytearray):
    ...         data = bytes(data)
    ...     hash_val = 0x811c9dc5  # FNV offset basis (32-bit)
    ...     for byte in data:
    ...         # Simple polynomial hash variant
    ...         hash_val = ((hash_val * 33) ^ byte) & 0xffffffff
    ...         # Add some bit mixing
    ...         hash_val ^= hash_val >> 16
    ...         hash_val = (hash_val * 0x85ebca6b) & 0xffffffff
    ...         hash_val ^= hash_val >> 13
    ...     return hash_val & 0xffffffff
    ...
    >>> print(int_hash_val_comprehensive(basic_good_hash))
    ╔══════════════════════════════════════════════════════════════════════════════════════════════╗
    ║                          COMPREHENSIVE HASH FUNCTION VALIDATION REPORT                       ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║ Function Name:     basic_good_hash  │ Overall Status:    PASS                                ║
    ║ Properties Tested: 7                │ Properties Passed: 7    (100.0%)                       ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║                                    PROPERTY STATUS                                           ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║ ✓ Determinism                                   │ PASS                                       ║
    ║ ✓ Type Consistency                              │ PASS                                       ║
    ║ ✓ Avalanche Effect                              │ PASS       | Avalanche Effect:       50.5% ║
    ║ ✓ Uniform Distribution                          │ PASS       | Uniformity Score:       0.996 ║
    ║ ✓ Collision Resistance                          │ PASS       | Collision Rate:        0.0000 ║
    ║ ✓ Empty Input                                   │ PASS                                       ║
    ║ ✓ Performance                                   │ PASS       | Avg Throughput:      2.5 MB/s ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║                                   RECOMMENDATIONS                                            ║
    ╠══════════════════════════════════════════════════════════════════════════════════════════════╣
    ║ ✓ Hash function meets all validation criteria - suitable for production use                  ║
    ╚══════════════════════════════════════════════════════════════════════════════════════════════╝
    DETAILED ANALYSIS:
    • All validation tests passed successfully
    • Hash function demonstrates good cryptographic properties
    • Suitable for general-purpose hashing applications
"""

import logging
import os
import random
import string
import time
from dataclasses import dataclass
from typing import Union, List, Dict, Any, Tuple

from .int_hash import _IntHashTyping, _INT_HASH_FUNCS

__all__ = [
    'int_hash_val_determinism',
    'int_hash_val_type_consistency',
    'int_hash_val_avalanche_effect',
    'int_hash_val_uniform_distribution',
    'int_hash_val_collision_resistance',
    'int_hash_val_empty_input',
    'int_hash_val_performance',
    'int_hash_val_comprehensive',
    'DeterminismValidationResult',
    'TypeConsistencyValidationResult',
    'AvalancheEffectValidationResult',
    'UniformDistributionValidationResult',
    'CollisionResistanceValidationResult',
    'EmptyInputValidationResult',
    'PerformanceValidationResult',
    'ComprehensiveValidationResult',
]

_HashFuncTyping = Union[str, _IntHashTyping]


@dataclass
class DeterminismValidationResult:
    """
    Results from determinism validation test.

    :param passed: Whether the determinism test passed
    :type passed: bool
    :param failed_cases: List of test cases that failed determinism check
    :type failed_cases: List[str]
    :param total_tested: Total number of test cases evaluated
    :type total_tested: int
    :param failed_count: Number of test cases that failed
    :type failed_count: int
    """
    passed: bool
    failed_cases: List[str]
    total_tested: int
    failed_count: int


@dataclass
class TypeConsistencyValidationResult:
    """
    Results from type consistency validation test.

    :param passed: Whether the type consistency test passed
    :type passed: bool
    :param failed_cases: List of test cases that failed type consistency check
    :type failed_cases: List[str]
    :param total_tested: Total number of test cases evaluated
    :type total_tested: int
    :param failed_count: Number of test cases that failed
    :type failed_count: int
    :param consistent_hashes: Dictionary mapping test strings to their consistent hash values
    :type consistent_hashes: Dict[str, int]
    """
    passed: bool
    failed_cases: List[str]
    total_tested: int
    failed_count: int
    consistent_hashes: Dict[str, int]


@dataclass
class AvalancheEffectValidationResult:
    """
    Results from avalanche effect validation test.

    :param passed: Whether the avalanche effect test passed
    :type passed: bool
    :param avg_bit_changes: Average number of bits changed across all comparisons
    :type avg_bit_changes: float
    :param change_percentage: Percentage of bits changed (avg_bit_changes / total_bits * 100)
    :type change_percentage: float
    :param total_comparisons: Total number of hash comparisons performed
    :type total_comparisons: int
    :param bit_changes_list: List of bit changes for each comparison
    :type bit_changes_list: List[int]
    :param min_changes: Minimum number of bits changed in any comparison
    :type min_changes: int
    :param max_changes: Maximum number of bits changed in any comparison
    :type max_changes: int
    """
    passed: bool
    avg_bit_changes: float
    change_percentage: float
    total_comparisons: int
    bit_changes_list: List[int]
    min_changes: int
    max_changes: int


@dataclass
class UniformDistributionValidationResult:
    """
    Results from uniform distribution validation test.

    :param passed: Whether the uniform distribution test passed
    :type passed: bool
    :param uniformity_score: Score indicating distribution uniformity (0-1, higher is better)
    :type uniformity_score: float
    :param bucket_stats: Statistics about bucket distribution
    :type bucket_stats: Dict[str, Any]
    :param sample_count: Number of samples used in the test
    :type sample_count: int
    :param buckets: List of counts for each bucket
    :type buckets: List[int]
    """
    passed: bool
    uniformity_score: float
    bucket_stats: Dict[str, Any]
    sample_count: int
    buckets: List[int]


@dataclass
class CollisionResistanceValidationResult:
    """
    Results from collision resistance validation test.

    :param passed: Whether the collision resistance test passed
    :type passed: bool
    :param collision_count: Number of collisions detected
    :type collision_count: int
    :param collision_rate: Rate of collisions (collision_count / sample_size)
    :type collision_rate: float
    :param sample_size: Total number of samples tested
    :type sample_size: int
    :param unique_hashes: Number of unique hash values generated
    :type unique_hashes: int
    :param collision_pairs: List of (input, hash) tuples that collided
    :type collision_pairs: List[Tuple[str, int]]
    """
    passed: bool
    collision_count: int
    collision_rate: float
    sample_size: int
    unique_hashes: int
    collision_pairs: List[Tuple[str, int]]


@dataclass
class EmptyInputValidationResult:
    """
    Results from empty input validation test.

    :param passed: Whether the empty input test passed
    :type passed: bool
    :param hash_results: List of hash values for empty inputs
    :type hash_results: List[int]
    :param consistent_empty_hash: Whether all empty inputs produced the same hash
    :type consistent_empty_hash: bool
    :param error_cases: List of (input_type, error_message) tuples for failed cases
    :type error_cases: List[Tuple[str, str]]
    :param empty_hash_value: The consistent hash value for empty inputs, or None if inconsistent
    :type empty_hash_value: Union[int, None]
    """
    passed: bool
    hash_results: List[int]
    consistent_empty_hash: bool
    error_cases: List[Tuple[str, str]]
    empty_hash_value: Union[int, None]


@dataclass
class PerformanceValidationResult:
    """
    Results from performance validation test.

    :param passed: Whether the performance test passed (completed without errors)
    :type passed: bool
    :param performance_data: Dictionary mapping data sizes to performance metrics
    :type performance_data: Dict[int, Dict[str, float]]
    :param tested_sizes: List of data sizes that were tested
    :type tested_sizes: List[int]
    :param completed_sizes: List of data sizes that completed successfully
    :type completed_sizes: List[int]
    """
    passed: bool
    performance_data: Dict[int, Dict[str, float]]
    tested_sizes: List[int]
    completed_sizes: List[int]


@dataclass
class ComprehensiveValidationResult:
    """
    Results from comprehensive validation test.

    :param passed: Whether all validation tests passed
    :type passed: bool
    :param not_passed_properties: List of property names that failed validation
    :type not_passed_properties: List[str]
    :param hash_function_name: Name of the hash function being validated
    :type hash_function_name: str
    :param total_properties_tested: Total number of properties tested
    :type total_properties_tested: int
    :param properties_passed: Number of properties that passed validation
    :type properties_passed: int
    :param determinism: Results from determinism validation
    :type determinism: DeterminismValidationResult
    :param type_consistency: Results from type consistency validation
    :type type_consistency: TypeConsistencyValidationResult
    :param avalanche_effect: Results from avalanche effect validation
    :type avalanche_effect: AvalancheEffectValidationResult
    :param uniform_distribution: Results from uniform distribution validation
    :type uniform_distribution: UniformDistributionValidationResult
    :param collision_resistance: Results from collision resistance validation
    :type collision_resistance: CollisionResistanceValidationResult
    :param empty_input: Results from empty input validation
    :type empty_input: EmptyInputValidationResult
    :param performance: Results from performance validation
    :type performance: PerformanceValidationResult
    """
    passed: bool
    not_passed_properties: List[str]
    hash_function_name: str
    total_properties_tested: int
    properties_passed: int
    determinism: DeterminismValidationResult
    type_consistency: TypeConsistencyValidationResult
    avalanche_effect: AvalancheEffectValidationResult
    uniform_distribution: UniformDistributionValidationResult
    collision_resistance: CollisionResistanceValidationResult
    empty_input: EmptyInputValidationResult
    performance: PerformanceValidationResult

    def __str__(self) -> str:
        """
        Generate a formatted string representation of the validation results.

        :return: Formatted validation report
        :rtype: str
        """
        overall_status = "PASS" if self.passed else "FAIL"
        success_rate = (
                self.properties_passed / self.total_properties_tested * 100) if self.total_properties_tested > 0 else 0

        # Property status summary
        properties = [
            ("Determinism", self.determinism),
            ("Type Consistency", self.type_consistency),
            ("Avalanche Effect", self.avalanche_effect),
            ("Uniform Distribution", self.uniform_distribution),
            ("Collision Resistance", self.collision_resistance),
            ("Empty Input", self.empty_input),
            ("Performance", self.performance),
        ]

        prop_lines = []
        for prop_name, prop in properties:
            status_symbol = "✓" if prop.passed else "✗"
            status_text = "PASS" if prop.passed else "FAIL"
            if isinstance(prop, AvalancheEffectValidationResult):
                prop_lines.append(
                    f"║ {status_symbol} {prop_name:<45} │ {status_text:<10} | Avalanche Effect: {self.avalanche_effect.change_percentage:>10.1f}% ║")
            elif isinstance(prop, UniformDistributionValidationResult):
                prop_lines.append(
                    f"║ {status_symbol} {prop_name:<45} │ {status_text:<10} | Uniformity Score: {self.uniform_distribution.uniformity_score:>11.3f} ║")
            elif isinstance(prop, CollisionResistanceValidationResult):
                prop_lines.append(
                    f"║ {status_symbol} {prop_name:<45} │ {status_text:<10} | Collision Rate: {self.collision_resistance.collision_rate:>13.4f} ║")
            elif isinstance(prop, PerformanceValidationResult):
                avg_throughput = sum(self.performance.performance_data[size]['throughput_mbps']
                                     for size in self.performance.completed_sizes) / len(
                    self.performance.completed_sizes)
                prop_lines.append(
                    f"║ {status_symbol} {prop_name:<45} │ {status_text:<10} | Avg Throughput: {avg_throughput:>8.1f} MB/s ║")
            else:
                prop_lines.append(f"║ {status_symbol} {prop_name:<45} │ {status_text:<42} ║")

        # Key metrics summary
        metrics_lines = [
            f"║ Avalanche Effect:     {self.avalanche_effect.change_percentage:>6.1f}% │ Uniformity Score:    {self.uniform_distribution.uniformity_score:>6.3f} ║",
            f"║ Collision Rate:       {self.collision_resistance.collision_rate:>6.4f} │ Empty Hash Consistent: {str(self.empty_input.consistent_empty_hash):>5} ║",
        ]

        return f"""
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                          COMPREHENSIVE HASH FUNCTION VALIDATION REPORT                       ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║ Function Name:     {self.hash_function_name:<16} │ Overall Status:    {overall_status:<33}   ║
║ Properties Tested: {self.total_properties_tested:<16} │ Properties Passed: {self.properties_passed:<4} ({success_rate:>5.1f}%)                       ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                    PROPERTY STATUS                                           ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
{os.linesep.join(prop_lines)}
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                   RECOMMENDATIONS                                            ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║ {self._get_recommendation():<92} ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝

{self._get_detailed_analysis()}""".strip()

    def _get_recommendation(self) -> str:
        """
        Generate a recommendation based on validation results.

        :return: Recommendation string
        :rtype: str
        """
        if self.passed:
            return "✓ Hash function meets all validation criteria - suitable for production use"
        elif self.determinism.passed and self.collision_resistance.passed:
            return "⚠ Hash function has minor issues - review failed properties before use"
        else:
            return "✗ Hash function has significant issues - not recommended for use"

    def _get_detailed_analysis(self) -> str:
        """
        Generate detailed analysis of validation results.

        :return: Detailed analysis string
        :rtype: str
        """
        analysis = []

        if not self.determinism.passed:
            analysis.append("• CRITICAL: Determinism failure - hash function produces inconsistent results")

        if not self.type_consistency.passed:
            analysis.append("• WARNING: Type inconsistency - different input types produce different hashes")

        if not self.avalanche_effect.passed:
            analysis.append(
                f"• WARNING: Poor avalanche effect ({self.avalanche_effect.change_percentage:.1f}%) - weak cryptographic properties")

        if not self.uniform_distribution.passed:
            analysis.append(
                f"• WARNING: Poor distribution uniformity ({self.uniform_distribution.uniformity_score:.3f}) - potential bias")

        if not self.collision_resistance.passed:
            analysis.append(
                f"• CRITICAL: High collision rate ({self.collision_resistance.collision_rate:.4f}) - security risk")

        if not self.empty_input.passed:
            analysis.append("• WARNING: Inconsistent empty input handling - may cause unexpected behavior")

        if not self.performance.passed:
            analysis.append("• INFO: Performance test issues - check implementation efficiency")

        if not analysis:
            analysis.append("• All validation tests passed successfully")
            analysis.append("• Hash function demonstrates good cryptographic properties")
            analysis.append("• Suitable for general-purpose hashing applications")

        return os.linesep.join(["DETAILED ANALYSIS:", *analysis])


def _norm_func(hash_func: _HashFuncTyping) -> Tuple[str, _IntHashTyping]:
    """
    Normalize hash function input to a tuple of (name, function).

    Converts string hash function names to their corresponding function objects
    from the registry, or extracts the function name from callable objects.

    :param hash_func: Either a string name of a registered hash function or a callable hash function
    :type hash_func: Union[str, _IntHashTyping]

    :return: A tuple containing (function_name, function_object)
    :rtype: Tuple[str, _IntHashTyping]

    Example::
        >>> def my_hash(data):
        ...     return hash(data)
        >>> name, func = _norm_func(my_hash)
        >>> name
        'my_hash'
        >>> name, func = _norm_func('xxhash32')  # If registered
        >>> name
        'xxhash32'
    """
    if isinstance(hash_func, str):
        return hash_func, _INT_HASH_FUNCS[hash_func]
    else:
        return hash_func.__name__, hash_func


def int_hash_val_determinism(hash_func: _HashFuncTyping,
                             test_data: List[Union[str, bytes, bytearray]]) -> DeterminismValidationResult:
    """
    Validate determinism: same input produces same output.

    Tests whether the hash function consistently produces the same output
    for identical inputs across multiple invocations.

    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    :param test_data: List of test inputs to validate determinism
    :type test_data: List[Union[str, bytes, bytearray]]

    :return: Determinism validation results
    :rtype: DeterminismValidationResult

    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_determinism(simple_hash, ["test", b"data"])
        >>> result.passed
        True
    """
    _, hash_func = _norm_func(hash_func)
    logging.info("Starting determinism validation")

    passed = True
    failed_cases = []

    for data in test_data:
        hash_results = [hash_func(data) for _ in range(10)]
        is_deterministic = len(set(hash_results)) == 1

        if not is_deterministic:
            logging.warning(f"Determinism validation failed for input: {repr(data)[:50]}")
            passed = False
            failed_cases.append(repr(data)[:50])
        else:
            logging.debug(f"Determinism OK: {repr(data)[:50]} -> {hash_results[0]:08x}")

    results = DeterminismValidationResult(
        passed=passed,
        failed_cases=failed_cases,
        total_tested=len(test_data),
        failed_count=len(failed_cases)
    )

    if passed:
        logging.info(f"Determinism validation passed for all {len(test_data)} test cases")
    else:
        logging.warning(f"Determinism validation failed for {len(failed_cases)}/{len(test_data)} cases")

    return results


def int_hash_val_type_consistency(hash_func: _HashFuncTyping) -> TypeConsistencyValidationResult:
    """
    Validate type consistency: same content in different types should produce same hash.

    Tests whether the hash function produces identical hash values for the same
    content when provided as string, bytes, or bytearray types.

    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping

    :return: Type consistency validation results
    :rtype: TypeConsistencyValidationResult

    Example::
        >>> def simple_hash(data):
        ...     if isinstance(data, str):
        ...         data = data.encode('utf-8')
        ...     return hash(bytes(data)) & 0xFFFFFFFF
        >>> result = int_hash_val_type_consistency(simple_hash)
        >>> result.passed
        True
    """
    _, hash_func = _norm_func(hash_func)
    logging.info("Starting type consistency validation")

    test_strings = ["hello", "world", "test", ""]
    passed = True
    failed_cases = []
    consistent_hashes = {}

    for s in test_strings:
        try:
            str_hash = hash_func(s)
            bytes_hash = hash_func(s.encode('utf-8'))
            bytearray_hash = hash_func(bytearray(s.encode('utf-8')))

            if str_hash != bytes_hash or bytes_hash != bytearray_hash:
                logging.warning(f"Type consistency failed for: {repr(s)}")
                logging.warning(f"  str: {str_hash:08x}, bytes: {bytes_hash:08x}, bytearray: {bytearray_hash:08x}")
                passed = False
                failed_cases.append(s)
            else:
                logging.debug(f"Type consistency OK: {repr(s)[:30]} -> {str_hash:08x}")
                consistent_hashes[s] = str_hash

        except Exception as e:
            logging.warning(f"Exception during type consistency test for {repr(s)}: {e}")
            passed = False
            failed_cases.append(s)

    results = TypeConsistencyValidationResult(
        passed=passed,
        failed_cases=failed_cases,
        total_tested=len(test_strings),
        failed_count=len(failed_cases),
        consistent_hashes=consistent_hashes
    )

    if passed:
        logging.info(f"Type consistency validation passed for all {len(test_strings)} test cases")
    else:
        logging.warning(f"Type consistency validation failed for {len(failed_cases)}/{len(test_strings)} cases")

    return results


def int_hash_val_avalanche_effect(hash_func: _HashFuncTyping,
                                  sample_size: int = 100) -> AvalancheEffectValidationResult:
    """
    Validate avalanche effect: small input changes cause significant output changes.

    Tests the avalanche effect property where a small change in input (single bit/character)
    should result in approximately 50% of the output bits changing. This is a key property
    of good hash functions.

    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    :param sample_size: Number of random samples to test, defaults to 100
    :type sample_size: int

    :return: Avalanche effect validation results
    :rtype: AvalancheEffectValidationResult

    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_avalanche_effect(simple_hash, sample_size=50)
        >>> result.change_percentage > 40.0
        True
    """
    _, hash_func = _norm_func(hash_func)
    logging.info(f"Starting avalanche effect validation with {sample_size} samples")

    def hamming_distance(a: int, b: int) -> int:
        """
        Calculate Hamming distance between two integers.

        :param a: First integer
        :type a: int
        :param b: Second integer
        :type b: int

        :return: Number of differing bits
        :rtype: int
        """
        return bin(a ^ b).count('1')

    total_bit_changes = 0
    total_comparisons = 0
    bit_changes_list = []

    for i in range(sample_size):
        # Generate random string
        original = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

        # Randomly modify one character
        pos = random.randint(0, len(original) - 1)
        chars = list(original)
        chars[pos] = random.choice(string.ascii_letters + string.digits)
        modified = ''.join(chars)

        if original != modified:
            try:
                hash1 = hash_func(original)
                hash2 = hash_func(modified)

                bit_changes = hamming_distance(hash1, hash2)
                bit_changes_list.append(bit_changes)
                total_bit_changes += bit_changes
                total_comparisons += 1

                logging.debug(f"Sample {i}: {bit_changes}/32 bits changed")

            except Exception as e:
                logging.warning(f"Exception during avalanche test sample {i}: {e}")

    if total_comparisons == 0:
        logging.warning("No valid comparisons for avalanche effect test")
        return AvalancheEffectValidationResult(
            passed=False,
            avg_bit_changes=0.0,
            change_percentage=0.0,
            total_comparisons=0,
            bit_changes_list=[],
            min_changes=0,
            max_changes=0
        )

    avg_bit_changes = total_bit_changes / total_comparisons
    change_percentage = avg_bit_changes / 32 * 100  # Assuming 32-bit output

    # Good avalanche effect should change ~50% of bits
    passed = change_percentage > 40.0

    results = AvalancheEffectValidationResult(
        passed=passed,
        avg_bit_changes=avg_bit_changes,
        change_percentage=change_percentage,
        total_comparisons=total_comparisons,
        bit_changes_list=bit_changes_list,
        min_changes=min(bit_changes_list) if bit_changes_list else 0,
        max_changes=max(bit_changes_list) if bit_changes_list else 0
    )

    logging.info(f"Average bit changes: {avg_bit_changes:.2f}/32 ({change_percentage:.1f}%)")

    if passed:
        logging.info(f"Avalanche effect validation passed: {change_percentage:.1f}%")
    else:
        logging.warning(f"Avalanche effect validation failed: {change_percentage:.1f}% (expected >40%)")

    return results


def int_hash_val_uniform_distribution(hash_func: _HashFuncTyping,
                                      sample_size: int = 10000) -> UniformDistributionValidationResult:
    """
    Validate uniform distribution of hash outputs.

    Tests whether the hash function produces uniformly distributed output values
    across the hash space. Divides the hash space into buckets and checks if
    hash values are evenly distributed.

    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    :param sample_size: Number of random samples to generate and hash, defaults to 10000
    :type sample_size: int

    :return: Uniform distribution validation results
    :rtype: UniformDistributionValidationResult

    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_uniform_distribution(simple_hash, sample_size=1000)
        >>> result.uniformity_score > 0.95
        True
    """
    _, hash_func = _norm_func(hash_func)
    logging.info(f"Starting uniform distribution validation with {sample_size} samples")

    # Generate random samples
    hashes = []
    for i in range(sample_size):
        data = ''.join(random.choices(string.ascii_letters + string.digits,
                                      k=random.randint(1, 50)))
        try:
            hashes.append(hash_func(data))
        except Exception as e:
            logging.warning(f"Exception during distribution test sample {i}: {e}")

    if not hashes:
        logging.warning("No valid hash samples for distribution test")
        return UniformDistributionValidationResult(
            passed=False,
            uniformity_score=0.0,
            bucket_stats={},
            sample_count=0,
            buckets=[]
        )

    # Calculate distribution statistics
    bucket_count = 256  # Divide hash values into 256 buckets
    buckets = [0] * bucket_count

    for h in hashes:
        bucket = h % bucket_count
        buckets[bucket] += 1

    # Calculate uniformity metrics
    expected = len(hashes) / bucket_count
    max_bucket = max(buckets)
    min_bucket = min(buckets)
    uniformity_score = 1 - (max_bucket - min_bucket) / len(hashes)

    # Good distribution should have uniformity > 0.95
    passed = uniformity_score > 0.95

    results = UniformDistributionValidationResult(
        passed=passed,
        uniformity_score=uniformity_score,
        bucket_stats={
            'max_bucket': max_bucket,
            'min_bucket': min_bucket,
            'expected': expected,
            'bucket_count': bucket_count
        },
        sample_count=len(hashes),
        buckets=buckets
    )

    logging.info(f"Max bucket: {max_bucket}, Min bucket: {min_bucket}, Expected: {expected:.1f}")
    logging.info(f"Uniformity score: {uniformity_score:.3f}")

    if passed:
        logging.info(f"Uniform distribution validation passed: {uniformity_score:.3f}")
    else:
        logging.warning(f"Uniform distribution validation failed: {uniformity_score:.3f} (expected >0.95)")

    return results


def int_hash_val_collision_resistance(hash_func: _HashFuncTyping,
                                      sample_size: int = 100000) -> CollisionResistanceValidationResult:
    """
    Validate collision resistance.

    Tests the hash function's resistance to collisions by generating many random
    inputs and checking for duplicate hash values. A good hash function should have
    a very low collision rate.

    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    :param sample_size: Number of random samples to test, defaults to 100000
    :type sample_size: int

    :return: Collision resistance validation results
    :rtype: CollisionResistanceValidationResult

    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_collision_resistance(simple_hash, sample_size=10000)
        >>> result.collision_rate < 0.001
        True
    """
    _, hash_func = _norm_func(hash_func)
    logging.info(f"Starting collision resistance validation with {sample_size} samples")

    hashes = set()
    collisions = 0
    collision_pairs = []

    for i in range(sample_size):
        data = f"test_string_{i}_{random.randint(0, 1000000)}"
        try:
            h = hash_func(data)

            if h in hashes:
                collisions += 1
                collision_pairs.append((data, h))
                logging.debug(f"Collision detected: {data} -> {h:08x}")
            hashes.add(h)

        except Exception as e:
            logging.warning(f"Exception during collision test sample {i}: {e}")

    collision_rate = collisions / sample_size if sample_size > 0 else 1.0

    # Good collision resistance should have rate < 0.001
    passed = collision_rate < 0.001

    results = CollisionResistanceValidationResult(
        passed=passed,
        collision_count=collisions,
        collision_rate=collision_rate,
        sample_size=sample_size,
        unique_hashes=len(hashes),
        collision_pairs=collision_pairs[:10]  # Store first 10 collisions for analysis
    )

    logging.info(f"Samples: {sample_size}, Collisions: {collisions}, Rate: {collision_rate:.6f}")

    if passed:
        logging.info(f"Collision resistance validation passed: {collision_rate:.6f}")
    else:
        logging.warning(f"Collision resistance validation failed: {collision_rate:.6f} (expected <0.001)")

    return results


def int_hash_val_empty_input(hash_func: _HashFuncTyping) -> EmptyInputValidationResult:
    """
    Validate empty input handling.

    Tests whether the hash function correctly handles empty inputs of different types
    (empty string, empty bytes, empty bytearray) and produces consistent results.

    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping

    :return: Empty input validation results
    :rtype: EmptyInputValidationResult

    Example::
        >>> def simple_hash(data):
        ...     if isinstance(data, str):
        ...         data = data.encode('utf-8')
        ...     return hash(bytes(data)) & 0xFFFFFFFF
        >>> result = int_hash_val_empty_input(simple_hash)
        >>> result.consistent_empty_hash
        True
    """
    _, hash_func = _norm_func(hash_func)
    logging.info("Starting empty input validation")

    empty_inputs = [
        ("str", ""),
        ("bytes", b""),
        ("bytearray", bytearray())
    ]

    results_list = []
    passed = True
    error_cases = []

    for input_type, empty in empty_inputs:
        try:
            result = hash_func(empty)
            results_list.append(result)
            logging.debug(f"{input_type}() -> {result:08x}")
        except Exception as e:
            logging.warning(f"{input_type}() -> Error: {e}")
            passed = False
            error_cases.append((input_type, str(e)))

    # Check if all empty inputs produce same result
    if results_list and len(set(results_list)) != 1:
        logging.warning(f"Different empty inputs produce different hash values - "
                        f"{list(zip(empty_inputs, results_list))!r}")
        passed = False

    results = EmptyInputValidationResult(
        passed=passed,
        hash_results=results_list,
        consistent_empty_hash=len(set(results_list)) == 1 if results_list else False,
        error_cases=error_cases,
        empty_hash_value=results_list[0] if results_list else None
    )

    if passed and results_list:
        logging.info(f"Empty input validation passed, consistent hash: {results_list[0]:08x}")
    else:
        logging.warning("Empty input validation failed")

    return results


def int_hash_val_performance(hash_func: _HashFuncTyping, data_sizes: List[int] = None) -> PerformanceValidationResult:
    """
    Validate performance characteristics.

    Measures the hash function's performance across different input sizes,
    calculating average hashing time and throughput in MB/s.

    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    :param data_sizes: List of data sizes (in bytes) to test, defaults to [100, 1000, 10000, 100000]
    :type data_sizes: List[int], optional

    :return: Performance validation results
    :rtype: PerformanceValidationResult

    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_performance(simple_hash, data_sizes=[100, 1000])
        >>> result.passed
        True
        >>> 100 in result.performance_data
        True
    """
    _, hash_func = _norm_func(hash_func)
    if data_sizes is None:
        data_sizes = [100, 1000, 10000, 100000]

    logging.info(f"Starting performance validation with data sizes: {data_sizes}")

    passed = True
    performance_data = {}

    for size in data_sizes:
        logging.debug(f"Testing performance for size: {size} bytes")

        # Generate test data
        test_data = 'a' * size

        # Warmup
        try:
            for _ in range(10):
                hash_func(test_data)
        except Exception as e:
            logging.warning(f"Warmup failed for size {size}: {e}")
            passed = False
            continue

        # Actual test
        iterations = max(1, 10000 // size)  # Adjust iterations based on data size

        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                hash_func(test_data)
            end_time = time.perf_counter()

            total_time = end_time - start_time
            avg_time = total_time / iterations
            throughput = size / avg_time / (1024 * 1024)  # MB/s

            performance_data[size] = {
                'avg_time_seconds': avg_time,
                'avg_time_microseconds': avg_time * 1000000,
                'throughput_mbps': throughput,
                'iterations': iterations,
                'total_time': total_time
            }

            logging.info(f"Size: {size:6d} bytes, Avg time: {avg_time * 1000000:8.2f} μs, "
                         f"Throughput: {throughput:8.2f} MB/s")

        except Exception as e:
            logging.warning(f"Performance test failed for size {size}: {e}")
            passed = False

    # Performance is considered "passed" if all tests completed without errors
    # Individual performance metrics should be evaluated by the caller

    results = PerformanceValidationResult(
        passed=passed,
        performance_data=performance_data,
        tested_sizes=data_sizes,
        completed_sizes=list(performance_data.keys())
    )

    if passed:
        logging.info(f"Performance validation completed for {len(performance_data)} sizes")
    else:
        logging.warning("Performance validation encountered errors")

    return results


def int_hash_val_comprehensive(hash_func: _HashFuncTyping) -> ComprehensiveValidationResult:
    """
    Comprehensive validation of hash function properties.

    Runs a complete suite of validation tests on the hash function, including:
    determinism, type consistency, avalanche effect, uniform distribution,
    collision resistance, empty input handling, and performance characteristics.

    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping

    :return: Comprehensive validation results
    :rtype: ComprehensiveValidationResult

    Example::
        >>> def simple_hash(data):
        ...     if isinstance(data, str):
        ...         data = data.encode('utf-8')
        ...     return hash(bytes(data)) & 0xFFFFFFFF
        >>> result = int_hash_val_comprehensive(simple_hash)
        >>> result.hash_function_name
        'simple_hash'
        >>> result.total_properties_tested
        7
    """
    hash_name, hash_func = _norm_func(hash_func)
    logging.info(f"Starting comprehensive validation for hash function: {hash_name}")

    # Test data for various validations
    test_data = [
        "hello",
        "world",
        "test_string",
        "",
        "a" * 1000,
        b"binary_data",
        bytearray(b"bytearray_data")
    ]

    not_passed_properties = []

    # Run all validation tests
    try:
        determinism_result = int_hash_val_determinism(hash_func, test_data)
        if not determinism_result.passed:
            not_passed_properties.append('determinism')
    except Exception as e:
        logging.warning(f"Exception during determinism validation: {e}")
        determinism_result = DeterminismValidationResult(False, [], 0, 0)
        not_passed_properties.append('determinism')

    try:
        type_consistency_result = int_hash_val_type_consistency(hash_func)
        if not type_consistency_result.passed:
            not_passed_properties.append('type_consistency')
    except Exception as e:
        logging.warning(f"Exception during type_consistency validation: {e}")
        type_consistency_result = TypeConsistencyValidationResult(False, [], 0, 0, {})
        not_passed_properties.append('type_consistency')

    try:
        avalanche_effect_result = int_hash_val_avalanche_effect(hash_func)
        if not avalanche_effect_result.passed:
            not_passed_properties.append('avalanche_effect')
    except Exception as e:
        logging.warning(f"Exception during avalanche_effect validation: {e}")
        avalanche_effect_result = AvalancheEffectValidationResult(False, 0.0, 0.0, 0, [], 0, 0)
        not_passed_properties.append('avalanche_effect')

    try:
        uniform_distribution_result = int_hash_val_uniform_distribution(hash_func)
        if not uniform_distribution_result.passed:
            not_passed_properties.append('uniform_distribution')
    except Exception as e:
        logging.warning(f"Exception during uniform_distribution validation: {e}")
        uniform_distribution_result = UniformDistributionValidationResult(False, 0.0, {}, 0, [])
        not_passed_properties.append('uniform_distribution')

    try:
        collision_resistance_result = int_hash_val_collision_resistance(hash_func)
        if not collision_resistance_result.passed:
            not_passed_properties.append('collision_resistance')
    except Exception as e:
        logging.warning(f"Exception during collision_resistance validation: {e}")
        collision_resistance_result = CollisionResistanceValidationResult(False, 0, 0.0, 0, 0, [])
        not_passed_properties.append('collision_resistance')

    try:
        empty_input_result = int_hash_val_empty_input(hash_func)
        if not empty_input_result.passed:
            not_passed_properties.append('empty_input')
    except Exception as e:
        logging.warning(f"Exception during empty_input validation: {e}")
        empty_input_result = EmptyInputValidationResult(False, [], False, [], None)
        not_passed_properties.append('empty_input')

    try:
        performance_result = int_hash_val_performance(hash_func)
        if not performance_result.passed:
            not_passed_properties.append('performance')
    except Exception as e:
        logging.warning(f"Exception during performance validation: {e}")
        performance_result = PerformanceValidationResult(False, {}, [], [])
        not_passed_properties.append('performance')

    # Overall pass/fail determination
    overall_passed = len(not_passed_properties) == 0
    total_properties = 7
    properties_passed = total_properties - len(not_passed_properties)

    comprehensive_results = ComprehensiveValidationResult(
        passed=overall_passed,
        not_passed_properties=not_passed_properties,
        hash_function_name=hash_name,
        total_properties_tested=total_properties,
        properties_passed=properties_passed,
        determinism=determinism_result,
        type_consistency=type_consistency_result,
        avalanche_effect=avalanche_effect_result,
        uniform_distribution=uniform_distribution_result,
        collision_resistance=collision_resistance_result,
        empty_input=empty_input_result,
        performance=performance_result
    )

    if overall_passed:
        logging.info(f"Comprehensive validation PASSED for {hash_name} - all {total_properties} properties validated")
    else:
        logging.warning(f"Comprehensive validation FAILED for {hash_name} - "
                        f"{len(not_passed_properties)} properties failed: {not_passed_properties}")

    return comprehensive_results
