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
"""

import logging
import random
import string
import time
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
]

_HashFuncTyping = Union[str, _IntHashTyping]


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


def int_hash_val_determinism(hash_func: _HashFuncTyping, test_data: List[Union[str, bytes, bytearray]]) -> Dict[
    str, Any]:
    """
    Validate determinism: same input produces same output.
    
    Tests whether the hash function consistently produces the same output
    for identical inputs across multiple invocations.
    
    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    :param test_data: List of test inputs to validate determinism
    :type test_data: List[Union[str, bytes, bytearray]]
    
    :return: Dictionary containing validation results with keys:
             
             - 'passed' (bool): Whether all tests passed
             - 'failed_cases' (list): List of inputs that failed determinism test
             - 'total_tested' (int): Total number of test cases
             - 'failed_count' (int): Number of failed cases
    :rtype: Dict[str, Any]
    
    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_determinism(simple_hash, ["test", b"data"])
        >>> result['passed']
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

    results = {
        'passed': passed,
        'failed_cases': failed_cases,
        'total_tested': len(test_data),
        'failed_count': len(failed_cases)
    }

    if passed:
        logging.info(f"Determinism validation passed for all {len(test_data)} test cases")
    else:
        logging.warning(f"Determinism validation failed for {len(failed_cases)}/{len(test_data)} cases")

    return results


def int_hash_val_type_consistency(hash_func: _HashFuncTyping) -> Dict[str, Any]:
    """
    Validate type consistency: same content in different types should produce same hash.
    
    Tests whether the hash function produces identical hash values for the same
    content when provided as string, bytes, or bytearray types.
    
    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    
    :return: Dictionary containing validation results with keys:
             
             - 'passed' (bool): Whether all type consistency tests passed
             - 'failed_cases' (list): List of inputs that failed consistency test
             - 'total_tested' (int): Total number of test cases
             - 'failed_count' (int): Number of failed cases
             - 'consistent_hashes' (dict): Mapping of consistent inputs to their hash values
    :rtype: Dict[str, Any]
    
    Example::
        >>> def simple_hash(data):
        ...     if isinstance(data, str):
        ...         data = data.encode('utf-8')
        ...     return hash(bytes(data)) & 0xFFFFFFFF
        >>> result = int_hash_val_type_consistency(simple_hash)
        >>> result['passed']
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

    results = {
        'passed': passed,
        'failed_cases': failed_cases,
        'total_tested': len(test_strings),
        'failed_count': len(failed_cases),
        'consistent_hashes': consistent_hashes
    }

    if passed:
        logging.info(f"Type consistency validation passed for all {len(test_strings)} test cases")
    else:
        logging.warning(f"Type consistency validation failed for {len(failed_cases)}/{len(test_strings)} cases")

    return results


def int_hash_val_avalanche_effect(hash_func: _HashFuncTyping, sample_size: int = 100) -> Dict[str, Any]:
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
    
    :return: Dictionary containing validation results with keys:
             
             - 'passed' (bool): Whether avalanche effect is sufficient (>40% bit changes)
             - 'avg_bit_changes' (float): Average number of bits changed
             - 'change_percentage' (float): Percentage of bits changed on average
             - 'total_comparisons' (int): Number of valid comparisons made
             - 'bit_changes_list' (list): List of bit changes for each sample
             - 'min_changes' (int): Minimum bit changes observed
             - 'max_changes' (int): Maximum bit changes observed
    :rtype: Dict[str, Any]
    
    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_avalanche_effect(simple_hash, sample_size=50)
        >>> result['change_percentage'] > 40.0
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
        return {
            'passed': False,
            'avg_bit_changes': 0.0,
            'change_percentage': 0.0,
            'total_comparisons': 0,
            'bit_changes_list': []
        }

    avg_bit_changes = total_bit_changes / total_comparisons
    change_percentage = avg_bit_changes / 32 * 100  # Assuming 32-bit output

    # Good avalanche effect should change ~50% of bits
    passed = change_percentage > 40.0

    results = {
        'passed': passed,
        'avg_bit_changes': avg_bit_changes,
        'change_percentage': change_percentage,
        'total_comparisons': total_comparisons,
        'bit_changes_list': bit_changes_list,
        'min_changes': min(bit_changes_list) if bit_changes_list else 0,
        'max_changes': max(bit_changes_list) if bit_changes_list else 0
    }

    logging.info(f"Average bit changes: {avg_bit_changes:.2f}/32 ({change_percentage:.1f}%)")

    if passed:
        logging.info(f"Avalanche effect validation passed: {change_percentage:.1f}%")
    else:
        logging.warning(f"Avalanche effect validation failed: {change_percentage:.1f}% (expected >40%)")

    return results


def int_hash_val_uniform_distribution(hash_func: _HashFuncTyping, sample_size: int = 10000) -> Dict[str, Any]:
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
    
    :return: Dictionary containing validation results with keys:
             
             - 'passed' (bool): Whether distribution is uniform (uniformity_score > 0.95)
             - 'uniformity_score' (float): Score from 0 to 1 indicating uniformity
             - 'bucket_stats' (dict): Statistics about bucket distribution
             - 'sample_count' (int): Number of samples successfully hashed
             - 'buckets' (list): Distribution of hashes across buckets
    :rtype: Dict[str, Any]
    
    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_uniform_distribution(simple_hash, sample_size=1000)
        >>> result['uniformity_score'] > 0.95
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
        return {
            'passed': False,
            'uniformity_score': 0.0,
            'bucket_stats': {},
            'sample_count': 0
        }

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

    results = {
        'passed': passed,
        'uniformity_score': uniformity_score,
        'bucket_stats': {
            'max_bucket': max_bucket,
            'min_bucket': min_bucket,
            'expected': expected,
            'bucket_count': bucket_count
        },
        'sample_count': len(hashes),
        'buckets': buckets
    }

    logging.info(f"Max bucket: {max_bucket}, Min bucket: {min_bucket}, Expected: {expected:.1f}")
    logging.info(f"Uniformity score: {uniformity_score:.3f}")

    if passed:
        logging.info(f"Uniform distribution validation passed: {uniformity_score:.3f}")
    else:
        logging.warning(f"Uniform distribution validation failed: {uniformity_score:.3f} (expected >0.95)")

    return results


def int_hash_val_collision_resistance(hash_func: _HashFuncTyping, sample_size: int = 100000) -> Dict[str, Any]:
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
    
    :return: Dictionary containing validation results with keys:
             
             - 'passed' (bool): Whether collision rate is acceptable (<0.001)
             - 'collision_count' (int): Number of collisions detected
             - 'collision_rate' (float): Ratio of collisions to total samples
             - 'sample_size' (int): Total number of samples tested
             - 'unique_hashes' (int): Number of unique hash values generated
             - 'collision_pairs' (list): First 10 collision examples
    :rtype: Dict[str, Any]
    
    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_collision_resistance(simple_hash, sample_size=10000)
        >>> result['collision_rate'] < 0.001
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

    results = {
        'passed': passed,
        'collision_count': collisions,
        'collision_rate': collision_rate,
        'sample_size': sample_size,
        'unique_hashes': len(hashes),
        'collision_pairs': collision_pairs[:10]  # Store first 10 collisions for analysis
    }

    logging.info(f"Samples: {sample_size}, Collisions: {collisions}, Rate: {collision_rate:.6f}")

    if passed:
        logging.info(f"Collision resistance validation passed: {collision_rate:.6f}")
    else:
        logging.warning(f"Collision resistance validation failed: {collision_rate:.6f} (expected <0.001)")

    return results


def int_hash_val_empty_input(hash_func: _HashFuncTyping) -> Dict[str, Any]:
    """
    Validate empty input handling.
    
    Tests whether the hash function correctly handles empty inputs of different types
    (empty string, empty bytes, empty bytearray) and produces consistent results.
    
    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    
    :return: Dictionary containing validation results with keys:
             
             - 'passed' (bool): Whether empty inputs are handled consistently
             - 'hash_results' (list): Hash values for each empty input type
             - 'consistent_empty_hash' (bool): Whether all empty inputs produce same hash
             - 'error_cases' (list): List of (type, error) tuples for failed cases
             - 'empty_hash_value' (int): The hash value for empty input (if consistent)
    :rtype: Dict[str, Any]
    
    Example::
        >>> def simple_hash(data):
        ...     if isinstance(data, str):
        ...         data = data.encode('utf-8')
        ...     return hash(bytes(data)) & 0xFFFFFFFF
        >>> result = int_hash_val_empty_input(simple_hash)
        >>> result['consistent_empty_hash']
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
        logging.warning("Different empty inputs produce different hash values")
        passed = False

    results = {
        'passed': passed,
        'hash_results': results_list,
        'consistent_empty_hash': len(set(results_list)) == 1 if results_list else False,
        'error_cases': error_cases,
        'empty_hash_value': results_list[0] if results_list else None
    }

    if passed and results_list:
        logging.info(f"Empty input validation passed, consistent hash: {results_list[0]:08x}")
    else:
        logging.warning("Empty input validation failed")

    return results


def int_hash_val_performance(hash_func: _HashFuncTyping, data_sizes: List[int] = None) -> Dict[str, Any]:
    """
    Validate performance characteristics.
    
    Measures the hash function's performance across different input sizes,
    calculating average hashing time and throughput in MB/s.
    
    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    :param data_sizes: List of data sizes (in bytes) to test, defaults to [100, 1000, 10000, 100000]
    :type data_sizes: List[int], optional
    
    :return: Dictionary containing validation results with keys:
             
             - 'passed' (bool): Whether all performance tests completed without errors
             - 'performance_data' (dict): Performance metrics for each data size
             - 'tested_sizes' (list): List of data sizes that were tested
             - 'completed_sizes' (list): List of data sizes that completed successfully
    :rtype: Dict[str, Any]
    
    Example::
        >>> def simple_hash(data):
        ...     return hash(data) & 0xFFFFFFFF
        >>> result = int_hash_val_performance(simple_hash, data_sizes=[100, 1000])
        >>> result['passed']
        True
        >>> 100 in result['performance_data']
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

    results = {
        'passed': passed,
        'performance_data': performance_data,
        'tested_sizes': data_sizes,
        'completed_sizes': list(performance_data.keys())
    }

    if passed:
        logging.info(f"Performance validation completed for {len(performance_data)} sizes")
    else:
        logging.warning("Performance validation encountered errors")

    return results


def int_hash_val_comprehensive(hash_func: _HashFuncTyping) -> Dict[str, Any]:
    """
    Comprehensive validation of hash function properties.
    
    Runs a complete suite of validation tests on the hash function, including:
    determinism, type consistency, avalanche effect, uniform distribution,
    collision resistance, empty input handling, and performance characteristics.
    
    :param hash_func: The hash function to validate. Should accept str, bytes, or bytearray
                      and return an integer hash value. Can be a string name or callable.
    :type hash_func: _HashFuncTyping
    
    :return: Dictionary containing comprehensive validation results with keys:
             
             - 'passed' (bool): Whether all validation tests passed
             - 'not_passed_properties' (list): List of properties that failed validation
             - 'hash_function_name' (str): Name of the hash function
             - 'total_properties_tested' (int): Total number of properties tested
             - 'properties_passed' (int): Number of properties that passed
             - Individual validation results for each property
    :rtype: Dict[str, Any]
    
    Example::
        >>> def simple_hash(data):
        ...     if isinstance(data, str):
        ...         data = data.encode('utf-8')
        ...     return hash(bytes(data)) & 0xFFFFFFFF
        >>> result = int_hash_val_comprehensive(simple_hash)
        >>> result['hash_function_name']
        'simple_hash'
        >>> result['total_properties_tested']
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

    validation_results = {}
    not_passed_properties = []

    # Run all validation tests
    validations = [
        ('determinism', lambda: int_hash_val_determinism(hash_func, test_data)),
        ('type_consistency', lambda: int_hash_val_type_consistency(hash_func)),
        ('avalanche_effect', lambda: int_hash_val_avalanche_effect(hash_func)),
        ('uniform_distribution', lambda: int_hash_val_uniform_distribution(hash_func)),
        ('collision_resistance', lambda: int_hash_val_collision_resistance(hash_func)),
        ('empty_input', lambda: int_hash_val_empty_input(hash_func)),
        ('performance', lambda: int_hash_val_performance(hash_func))
    ]

    for prop_name, validation_func in validations:
        logging.info(f"Running {prop_name} validation")
        try:
            result = validation_func()
            validation_results[prop_name] = result

            if not result.get('passed', False):
                not_passed_properties.append(prop_name)
                logging.warning(f"{prop_name} validation failed")
            else:
                logging.info(f"{prop_name} validation passed")

        except Exception as e:
            logging.warning(f"Exception during {prop_name} validation: {e}")
            validation_results[prop_name] = {
                'passed': False,
                'error': str(e)
            }
            not_passed_properties.append(prop_name)

    # Overall pass/fail determination
    overall_passed = len(not_passed_properties) == 0

    comprehensive_results = {
        'passed': overall_passed,
        'not_passed_properties': not_passed_properties,
        'hash_function_name': hash_name,
        'total_properties_tested': len(validations),
        'properties_passed': len(validations) - len(not_passed_properties),
        **validation_results  # Include all individual validation results
    }

    if overall_passed:
        logging.info(f"Comprehensive validation PASSED for {hash_name} - all {len(validations)} properties validated")
    else:
        logging.warning(f"Comprehensive validation FAILED for {hash_name} - "
                        f"{len(not_passed_properties)} properties failed: {not_passed_properties}")

    return comprehensive_results
