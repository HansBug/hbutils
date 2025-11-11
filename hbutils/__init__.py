"""
hbutils - A comprehensive utility library providing various helper functions and tools.

This package provides a wide range of utility functions organized into multiple modules:

- algorithm: Linear and topological algorithms
- binary: Binary data manipulation and conversion
- collection: Collection utilities and functional operations
- color: Color model and conversion utilities
- config: Configuration and metadata management
- design: Design patterns (decorator, singleton, observer, etc.)
- encoding: Encoding/decoding utilities (ANSI, base64, hash, etc.)
- expression: Expression evaluation and manipulation
- file: File stream operations
- model: Model utilities (class, enum, comparison, etc.)
- random: Random data generation utilities
- reflection: Reflection and introspection utilities
- scale: Size and time scaling utilities
- string: String manipulation and formatting
- system: System-level utilities (filesystem, git, network, OS, Python)
- testing: Testing utilities and helpers

Example::
    >>> import hbutils
    >>> print(hbutils.__version__)
    '0.1.0'
"""

from .config.meta import __VERSION__ as __version__
