"""
This module provides various test data generators for testing purposes.

It includes base generator classes, matrix-based generators, AETG (Automatic Efficient Test Generator) 
implementations, and functional utilities for generating test data. These generators are useful for 
creating comprehensive test cases and combinatorial testing scenarios.

The module exports:
- BaseGenerator: Abstract base class for all generators
- MatrixGenerator: Generator based on matrix operations
- AETGGenerator: AETG algorithm-based test case generator
- Functional utilities from the func submodule
"""

from .aetg import AETGGenerator
from .base import BaseGenerator
from .func import *
from .func import __all__ as _func_all
from .matrix import MatrixGenerator

__all__ = [
    'BaseGenerator', 'MatrixGenerator', 'AETGGenerator',
    *_func_all,
]
