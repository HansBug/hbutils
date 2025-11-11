# hbutils

[![PyPI](https://img.shields.io/pypi/v/hbutils)](https://pypi.org/project/hbutils/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hbutils)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/hbutils)
![PyPI - Downloads](https://img.shields.io/pypi/dm/hbutils)

![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/1ffdd46a0c79027a7776b262143b20a4/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/HansBug/1ffdd46a0c79027a7776b262143b20a4/raw/comments.json)
[![Maintainability](https://api.codeclimate.com/v1/badges/5b6e14a915b63faeae90/maintainability)](https://codeclimate.com/github/HansBug/hbutils/maintainability)
[![codecov](https://codecov.io/gh/hansbug/hbutils/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/hansbug/hbutils)

[![Docs Deploy](https://github.com/hansbug/hbutils/workflows/Docs%20Deploy/badge.svg)](https://github.com/hansbug/hbutils/actions?query=workflow%3A%22Docs+Deploy%22)
[![Code Test](https://github.com/hansbug/hbutils/workflows/Code%20Test/badge.svg)](https://github.com/hansbug/hbutils/actions?query=workflow%3A%22Code+Test%22)
[![Badge Creation](https://github.com/hansbug/hbutils/workflows/Badge%20Creation/badge.svg)](https://github.com/hansbug/hbutils/actions?query=workflow%3A%22Badge+Creation%22)
[![Package Release](https://github.com/hansbug/hbutils/workflows/Package%20Release/badge.svg)](https://github.com/hansbug/hbutils/actions?query=workflow%3A%22Package+Release%22)

[![GitHub stars](https://img.shields.io/github/stars/hansbug/hbutils)](https://github.com/hansbug/hbutils/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/hansbug/hbutils)](https://github.com/hansbug/hbutils/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hansbug/hbutils)
[![GitHub issues](https://img.shields.io/github/issues/hansbug/hbutils)](https://github.com/hansbug/hbutils/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/hansbug/hbutils)](https://github.com/hansbug/hbutils/pulls)
[![Contributors](https://img.shields.io/github/contributors/hansbug/hbutils)](https://github.com/hansbug/hbutils/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/hansbug/hbutils)](https://github.com/HansBug/hbutils/blob/master/LICENSE)

**hbutils** is a comprehensive collection of useful functions and classes designed to simplify and accelerate Python
infrastructure development. It provides a wide array of utilities covering algorithms, data structures, system
operations, design patterns, and testing tools.

## Installation

You can simply install it with the `pip` command line from the official PyPI site.

```shell
pip install hbutils
```

For more information about installation, you can refer to
the [Installation Guide](https://hbutils.readthedocs.io/en/latest/tutorials/installation/index.html).

## Compatibility

The library is designed to be cross-platform and supports a wide range of Python environments. It has been thoroughly
tested on:

| Operating System | Python Versions                  | Implementations                               |
|:-----------------|:---------------------------------|:----------------------------------------------|
| **Windows**      | 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 | CPython, PyPy3.8, PyPy3.9, PyPy3.10, PyPy3.11 |
| **Ubuntu**       | 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 | CPython, PyPy3.8, PyPy3.9, PyPy3.10, PyPy3.11 |
| **macOS**        | 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 | CPython, PyPy3.8, PyPy3.9, PyPy3.10, PyPy3.11 |

## Modules Overview

The project is structured into several top-level modules, each dedicated to a specific area of utility:

| Module                   | Description                                                                                                                         | Documentation Link                                                                          |
|:-------------------------|:------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------|
| **`hbutils.algorithm`**  | Provides implementations for useful classic algorithms, such as linear mapping and topological sorting.                             | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/algorithm/index.html)  |
| **`hbutils.binary`**     | Offers basic IO types and utilities for structured binary file operations, often used for low-level data handling.                  | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/binary/index.html)     |
| **`hbutils.collection`** | Offers advanced data structures and utilities for manipulating sequences and collections, including grouping and deduplication.     | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/collection/index.html) |
| **`hbutils.color`**      | Deals with color models (RGB, HSV, HLS) and their calculations, including parsing and conversion.                                   | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/color/index.html)      |
| **`hbutils.config`**     | Contains global meta information of this package.                                                                                   | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/config/index.html)     |
| **`hbutils.design`**     | Contains extendable implementations for common design patterns in Python, such as Singleton.                                        | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/design/index.html)     |
| **`hbutils.encoding`**   | Provides utilities for common encoding, decoding, and cryptographic hash calculations for binary data.                              | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/encoding/index.html)   |
| **`hbutils.expression`** | A flexible system for creating and composing callable functions and complex expressions with operator overloading.                  | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/expression/index.html) |
| **`hbutils.file`**       | Offers useful utilities for managing file streams, including cursor position and size retrieval.                                    | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/file/index.html)       |
| **`hbutils.model`**      | Provides decorators and utilities for enhancing Python classes with features like automatic field access and visual representation. | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/model/index.html)      |
| **`hbutils.random`**     | Utilities for generating random sequences, strings (e.g., random hashes), and performing random choices.                            | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/random/index.html)     |
| **`hbutils.reflection`** | Provides powerful utilities for introspection and manipulation of Python objects, functions, and modules.                           | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/reflection/index.html) |
| **`hbutils.scale`**      | Handles the calculation and parsing of scaled values, such as memory size and time spans, for human-readable output.                | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/scale/index.html)      |
| **`hbutils.string`**     | Simple but useful string processing utilities, including pluralization, singularization, and truncation.                            | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/string/index.html)     |
| **`hbutils.system`**     | Encapsulates operations on the current running environment, including filesystem, network, and OS information.                      | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/system/index.html)     |
| **`hbutils.testing`**    | A set of utilities for building robust unit tests, including isolation, capture, and test data generation.                          | [API Documentation](https://hbutils.readthedocs.io/en/latest/api_doc/testing/index.html)    |

## Featured Utilities

Here are some representative examples showcasing the functionality of key modules.

### `hbutils.algorithm`

This module provides implementations for classic algorithms.

#### `linear_map`

Creates a callable piecewise linear function from a sequence of control points for custom interpolation.

**Documentation:
** [linear_map](https://hbutils.readthedocs.io/en/latest/api_doc/algorithm/linear.html#hbutils.algorithm.linear.linear_map)

```python
from hbutils.algorithm import linear_map

# Simple linear map with auto x-spacing (0, 0.5, 1.0)
# Points: (0, 0), (0.5, 1), (1.0, 0.5)
f = linear_map((0, 1, 0.5))

print(f(0.25))
# Expected output: 0.5

print(f(1))
# Expected output: 0.5

# Complex linear map with custom (x, y) points
f_custom = linear_map(((-0.2, 0), (0.7, 1), (1.1, 0.5)))

print(f_custom(0.7))
# Expected output: 1.0
```

#### `topoids`

Performs topological sorting on a directed acyclic graph (DAG) represented by integer node IDs and edges.

**Documentation:
** [topoids](https://hbutils.readthedocs.io/en/latest/api_doc/algorithm/topological.html#hbutils.algorithm.topological.topoids)

```python
from hbutils.algorithm import topoids

# Edges: 0 -> 1, 2 -> 1
result = topoids(3, [(0, 1), (2, 1)])
print(result)
# Expected output: [0, 2, 1] or [2, 0, 1] (non-deterministic order for nodes with no incoming edges)

# With sort=True, the result is deterministic
# Edges: 0 -> 2, 0 -> 1, 2 -> 3, 1 -> 3
result_sorted = topoids(4, [(0, 2), (0, 1), (2, 3), (1, 3)], sort=True)
print(result_sorted)
# Expected output: [0, 1, 2, 3]
```

### `hbutils.collection`

Utilities for manipulating sequences and collections.

#### `unique`

Removes duplicate elements from a sequence while preserving the original order.

**Documentation:
** [unique](https://hbutils.readthedocs.io/en/latest/api_doc/collection/sequence.html#hbutils.collection.sequence.unique)

```python
from hbutils.collection import unique

result_list = unique([3, 1, 2, 1, 4, 3])
print(result_list)
# Expected output: [3, 1, 2, 4]

result_tuple = unique(('a', 'b', 'a', 'c'))
print(result_tuple)
# Expected output: ('a', 'b', 'c')
```

#### `group_by`

Divides elements into groups based on a key function, with optional post-processing for each group.

**Documentation:
** [group_by](https://hbutils.readthedocs.io/en/latest/api_doc/collection/sequence.html#hbutils.collection.sequence.group_by)

```python
from hbutils.collection import group_by

foods = ['apple', 'orange', 'pear', 'banana', 'fish']

# Group by length
by_len = group_by(foods, len)
print(by_len)
# Expected output: {5: ['apple', 'orange'], 4: ['pear', 'fish'], 6: ['banana']}

# Group by first letter and count the items in each group
by_first_letter_count = group_by(foods, lambda x: x[0], len)
print(by_first_letter_count)
# Expected output: {'a': 1, 'o': 1, 'p': 1, 'b': 1, 'f': 1}
```

### `hbutils.design`

Implementations of common design patterns.

#### `SingletonMeta`

A metaclass to enforce the traditional Singleton pattern, ensuring only one instance of a class exists.

**Documentation:
** [SingletonMeta](https://hbutils.readthedocs.io/en/latest/api_doc/design/singleton.html#hbutils.design.singleton.SingletonMeta)

```python
from hbutils.design import SingletonMeta


class MyService(metaclass=SingletonMeta):
    def __init__(self):
        self.value = 42


s1 = MyService()
s2 = MyService()

print(s1 is s2)
# Expected output: True
```

#### `ValueBasedSingletonMeta`

A metaclass for creating singletons based on a specific initialization value.

**Documentation:
** [ValueBasedSingletonMeta](https://hbutils.readthedocs.io/en/latest/api_doc/design/singleton.html#hbutils.design.singleton.ValueBasedSingletonMeta)

```python
from hbutils.design import ValueBasedSingletonMeta


class MyData(metaclass=ValueBasedSingletonMeta):
    def __init__(self, value):
        self.value = value


d1 = MyData(1)
d2 = MyData(1)
d3 = MyData(2)

print(d1 is d2)
# Expected output: True

print(d1 is d3)
# Expected output: False
```

### `hbutils.encoding`

Wrappers for cryptographic hash functions.

#### `md5`, `sha256`, and `sha3`

Provides simple functions for computing common cryptographic hashes of binary data.

**Documentation:
** [md5](https://hbutils.readthedocs.io/en/latest/api_doc/encoding/hash.html#hbutils.encoding.hash.md5), [sha256](https://hbutils.readthedocs.io/en/latest/api_doc/encoding/hash.html#hbutils.encoding.hash.sha256), [sha3](https://hbutils.readthedocs.io/en/latest/api_doc/encoding/hash.html#hbutils.encoding.hash.sha3)

```python
from hbutils.encoding import md5, sha256, sha3

data = b'this is a word'

print(md5(data))
# Expected output: cdfc9527f76e296c76cdb331ac2d1d88

print(sha256(data))
# Expected output: 91ccca153f5d3739af1f0d304d033f193b25208d44d371c1304877a6503471bf

# SHA3 with configurable bit length (default is 256)
print(sha3(data, n=224))
# Expected output: e0271d2734fc2c1a6dfcb6051bec6dc59e5f7fbec4b0d42ef1faee64
```

### `hbutils.file`

Utilities for managing file streams.

#### `keep_cursor`

A context manager that saves and restores the file stream's cursor position, ensuring operations within the block do not
affect the external cursor state.

**Documentation:
** [keep_cursor](https://hbutils.readthedocs.io/en/latest/api_doc/file/stream.html#hbutils.file.stream.keep_cursor)

```python
import io
from hbutils.file import keep_cursor

file = io.BytesIO(b'\xde\xad\xbe\xef')
print(f"Initial position: {file.tell()}")

with keep_cursor(file):
    file.read(2)
    print(f"Position inside block: {file.tell()}")

print(f"Position after block: {file.tell()}")
# Expected output: Position after block: 0 (restored)
```

#### `getsize`

Retrieves the size of a seekable file stream in bytes, without changing the cursor position.

**Documentation:
** [getsize](https://hbutils.readthedocs.io/en/latest/api_doc/file/stream.html#hbutils.file.stream.getsize)

```python
import io
from hbutils.file import getsize

file = io.BytesIO(b'\xde\xad\xbe\xef')
size = getsize(file)

print(f"File size: {size}")
# Expected output: File size: 4
```

### `hbutils.reflection`

Advanced function and object introspection and manipulation.

#### `dynamic_call`

A decorator that enables a function to be called with a flexible number of arguments, automatically filtering them based
on the function's signature.

**Documentation:
** [dynamic_call](https://hbutils.readthedocs.io/en/latest/api_doc/reflection/func.html#hbutils.reflection.func.dynamic_call)

```python
from hbutils.reflection import dynamic_call


@dynamic_call
def my_func(x, y):
    return x + y


# Extra arguments are ignored
result = my_func(1, 2, 3, z=4)
print(f"Result with extra args: {result}")
# Expected output: Result with extra args: 3

# Keyword arguments are supported
result_kw = my_func(y=5, x=10)
print(f"Result with keywords: {result_kw}")
# Expected output: Result with keywords: 15
```

#### `frename`

A decorator to easily rename a function by changing its `__name__` attribute.

**Documentation:
** [frename](https://hbutils.readthedocs.io/en/latest/api_doc/reflection/func.html#hbutils.reflection.func.frename)

```python
from hbutils.reflection import frename


@frename('new_name')
def old_name(a, b):
    return a * b


print(f"Function name: {old_name.__name__}")
# Expected output: Function name: new_name
```

### `hbutils.scale`

Handling and formatting of scaled values.

#### `size_to_bytes`

Converts various memory size representations (int, float, string like "3.54 GB") into an integer value in bytes.

**Documentation:
** [size_to_bytes](https://hbutils.readthedocs.io/en/latest/api_doc/scale/size.html#hbutils.scale.size.size_to_bytes)

```python
from hbutils.scale import size_to_bytes

size_int = size_to_bytes(23344)
print(f"Integer size: {size_int}")
# Expected output: Integer size: 23344

size_str_si = size_to_bytes('23356 KB')
print(f"SI size (KB): {size_str_si}")
# Expected output: SI size (KB): 23356000

size_str_nist = size_to_bytes('3.54 GiB')
print(f"NIST size (GiB): {size_str_nist}")
# Expected output: NIST size (GiB): 3801046057 (approx)
```

#### `size_to_bytes_str`

Converts a size value to a human-readable string with the most appropriate unit (e.g., KiB, MB, GB).

**Documentation:
** [size_to_bytes_str](https://hbutils.readthedocs.io/en/latest/api_doc/scale/size.html#hbutils.scale.size.size_to_bytes_str)

```python
from hbutils.scale import size_to_bytes_str

# Default (NIST/binary system) with precision
result_nist = size_to_bytes_str(23344, precision=2)
print(f"NIST format: {result_nist}")
# Expected output: NIST format: 22.79 KiB

# SI/decimal system
result_si = size_to_bytes_str('3.54 GB', system='si', precision=3)
print(f"SI format: {result_si}")
# Expected output: SI format: 3.540 GB
```

### `hbutils.string`

Simple but powerful string processing utilities.

#### `plural_word`

Formats a word with its count, automatically using the correct singular or plural form.

**Documentation:
** [plural_word](https://hbutils.readthedocs.io/en/latest/api_doc/string/plural.html#hbutils.string.plural.plural_word)

```python
from hbutils.string import plural_word

print(plural_word(1, 'word'))
# Expected output: 1 word

print(plural_word(2, 'word'))
# Expected output: 2 words

print(plural_word(2, 'woman'))
# Expected output: 2 women
```

#### `plural_form`

Gets the plural form of a word, handling irregular plurals.

**Documentation:
** [plural_form](https://hbutils.readthedocs.io/en/latest/api_doc/string/plural.html#hbutils.string.plural.plural_form)

```python
from hbutils.string import plural_form

print(plural_form('it'))
# Expected output: they

print(plural_form('woman'))
# Expected output: women
```

### `hbutils.system`

Unix-like commands for filesystem operations.

#### `copy`, `remove`, and `getsize`

Provides powerful, glob-enabled utilities for file system manipulation, similar to Unix commands like `cp -rf`,
`rm -rf`, and `du -sh`.

**Documentation:
** [copy](https://hbutils.readthedocs.io/en/latest/api_doc/system/filesystem.html#hbutils.system.filesystem.directory.copy), [remove](https://hbutils.readthedocs.io/en/latest/api_doc/system/filesystem.html#hbutils.system.filesystem.directory.remove), [getsize](https://hbutils.readthedocs.io/en/latest/api_doc/system/filesystem.html#hbutils.system.filesystem.directory.getsize)

```python
from hbutils.system import copy, remove, getsize
import os

# Example setup (assuming a file 'README.md' exists)
# Note: These examples are illustrative and require a temporary environment to run safely.

# --- copy example ---
copy('README.md', 'README_copy.md')
print(os.path.exists('README_copy.md'))
# Expected output: True

# --- getsize example ---
size = getsize('README.md')
print(f"Size of README.md: {size} bytes")

# --- remove example ---
remove('README_copy.md')
print(os.path.exists('README_copy.md'))
# Expected output: False
```

### `hbutils.testing`

Utilities for isolated and robust unit testing.

#### `isolated_directory`

A context manager that executes code within a temporary, isolated directory, with optional mapping of files/directories
from the original location. This is ideal for tests that modify the file system.

**Documentation:
** [isolated_directory](https://hbutils.readthedocs.io/en/latest/api_doc/testing/isolated.html#hbutils.testing.isolated.directory.isolated_directory)

```python
from hbutils.testing import isolated_directory
import os

# The code inside the 'with' block runs in a temporary directory.
with isolated_directory():
    # Create a file in the temporary directory
    with open('temp_file.txt', 'w') as f:
        f.write('test content')

    print(os.listdir('.'))
    # Expected output: ['temp_file.txt']

# After exiting, the temporary directory and its contents are automatically cleaned up.
# The original working directory is restored.
print(os.path.exists('temp_file.txt'))
# Expected output: False
```

## Contributing

We welcome contributions from the community! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get
started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
