"""
Color utilities and model representations.

This package module exposes the public API for the :mod:`hbutils.color` package,
combining color model representations and common color utilities into a single
namespace. The main entry point is the :class:`Color` class, which supports
RGB/HSV/HLS conversions, CSS3 color names, and hexadecimal color strings.

The module re-exports the public symbols from the following submodules:

* :mod:`hbutils.color.model` - Core color model representations
* :mod:`hbutils.color.utils` - Color utility functions and helpers

.. note::
   This module is an aggregator and does not define additional functionality
   beyond re-exporting public APIs.

Example::

    >>> from hbutils.color import Color
    >>> color = Color('red')
    >>> str(color)
    '#ff0000'
    >>> color.hsv.hue
    0.0
"""
from .model import *
from .utils import *
