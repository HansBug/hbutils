"""
Overview:
    String process module, include some useful utilities for string processing.
    This module provides various string manipulation utilities including inflection,
    pluralization, templating, tree structure representation, and truncation functions.

The module exports functionality from the following submodules:
    - inflection: String inflection utilities (e.g., camelCase, snake_case conversions)
    - plural: Pluralization and singularization utilities
    - template: String templating utilities
    - tree: Tree structure string representation utilities
    - trunc: String truncation utilities

This is the main entry point for the hbutils.string package, providing a unified
interface to all string processing utilities through wildcard imports from its
submodules.
"""
from .inflection import *
from .plural import *
from .template import *
from .tree import *
from .trunc import *
