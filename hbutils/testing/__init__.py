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
"""
from .capture import *
from .compare import *
from .generator import *
from .isolated import *
from .requires import *
from .simulate import *
