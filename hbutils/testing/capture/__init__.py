"""
Overview:
    Utilities for capturing different kinds of results, which can be useful in testing.
    
    This module provides tools for capturing program exit behavior and output streams during testing.
    It includes functionality to intercept system exits and capture stdout/stderr output, making it
    easier to test code that produces side effects.
    
    The module exports all functionality from its submodules:
    
    - exit: Utilities for capturing and testing system exit behavior
    - output: Utilities for capturing stdout/stderr output streams
"""
from .exit import *
from .output import *
