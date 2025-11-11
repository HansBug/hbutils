"""
Overview:
    Encoding module, include some not so complex but useful functions. They will improve \
    the quality of your coding experience when dealing with these data.

This module provides various encoding and decoding utilities including:

    - ANSI color and style encoding for terminal output
    - Base64 encoding and decoding operations
    - General decoding utilities for various data formats
    - Hash functions for data integrity and identification

The module aggregates functionality from several submodules:

    - ansi: ANSI escape code handling for terminal formatting
    - base64: Base64 encoding/decoding utilities
    - decode: Automatic encoding detection and decoding
    - hash: Cryptographic hash function wrappers

Examples::
    >>> from hbutils.encoding import md5, sha256
    >>> md5(b'hello world')
    '5eb63bbbe01eeed093cb22bb8f5acdc3'
    >>> sha256(b'hello world')
    'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
"""
from .ansi import *
from .base64 import *
from .decode import *
from .hash import *
