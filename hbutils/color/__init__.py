"""
Overview:
    Color module, include the basic color system model, and some simple color utilities.

This module provides comprehensive color manipulation functionality including:

    - Color model representations (RGB, HSV, etc.)
    - Color conversion utilities
    - Color manipulation and transformation functions
    
The module exports all public APIs from its submodules:

    - model: Color model representations (RGB, HSV, HLS color systems)
    - utils: Color utilities for manipulation, distance calculation, and gradient generation
"""
from .model import *
from .utils import *
