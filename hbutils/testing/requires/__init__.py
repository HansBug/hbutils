"""
Overview:
    System requirements conditions for unittest.
    Can be used on ``unittest.skipUnless``, ``pytest.mark.skipUnless``, etc.
    
    This module provides various condition checkers for testing requirements,
    including command availability, expression evaluation, and git-related checks.
    These conditions can be used to conditionally skip tests based on system
    capabilities and environment setup.

The module aggregates functionality from:

    - cmd: Command availability checking
    - expr: Version and environment expression evaluation
    - git: Git and Git LFS installation and version checking

Example::
    >>> from hbutils.testing.requires import vpython, is_git_installed
    >>> # Check Python version
    >>> vpython >= '3.7'
    True
    >>> # Check if Git is installed
    >>> is_git_installed()
    True
"""
from .cmd import *
from .expr import *
from .git import *
