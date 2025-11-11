"""
Overview:
    Testing process module, include some useful utilities for unittest.
    
    This module provides various testing utilities organized into several categories:
    
    - **capture**: Utilities for capturing program output and exit behavior
    - **compare**: Utilities for comparing test results, especially text comparisons
    - **generator**: Test case generation utilities including AETG algorithm and matrix generation
    - **isolated**: Utilities for creating isolated test environments (directories, entry points, input, logging)
    - **requires**: Utilities for checking test requirements (commands, expressions, git, versions)
    - **simulate**: Utilities for simulating program entry points and execution
    
    These utilities help in writing comprehensive and maintainable unit tests by providing
    common testing patterns and infrastructure.
    
    The module serves as the main entry point for all testing utilities, re-exporting
    functionality from its submodules for convenient access. It enables developers to
    write more robust and maintainable tests by providing common patterns for:
    
    - Capturing and verifying program output and exit codes
    - Comparing text output with flexible preprocessing
    - Generating comprehensive test case combinations
    - Creating isolated test environments
    - Checking system requirements and dependencies
    - Simulating CLI entry points
    
    Example::
        >>> from hbutils.testing import capture_output, TextAligner, isolated_directory
        >>> # Use testing utilities in your test suite
        >>> with capture_output() as (stdout, stderr):
        ...     print("test output")
        >>> stdout.getvalue()
        'test output\\n'
"""
from .capture import *
from .compare import *
from .generator import *
from .isolated import *
from .requires import *
from .simulate import *
