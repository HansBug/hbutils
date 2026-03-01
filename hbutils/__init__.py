"""
hbutils - A comprehensive utility library providing various helper functions and tools.

This package exposes a collection of utilities organized into focused modules
for common development tasks. It provides a single public attribute,
:attr:`__version__`, which identifies the installed library version.

The package includes the following main modules:

* :mod:`hbutils.algorithm` - Linear and topological algorithms
* :mod:`hbutils.binary` - Binary data manipulation and conversion
* :mod:`hbutils.collection` - Collection utilities and functional operations
* :mod:`hbutils.color` - Color model and conversion utilities
* :mod:`hbutils.config` - Configuration and metadata management
* :mod:`hbutils.design` - Design patterns (decorator, singleton, observer, etc.)
* :mod:`hbutils.encoding` - Encoding/decoding utilities (ANSI, base64, hash, etc.)
* :mod:`hbutils.expression` - Expression evaluation and manipulation
* :mod:`hbutils.file` - File stream operations
* :mod:`hbutils.model` - Model utilities (class, enum, comparison, etc.)
* :mod:`hbutils.random` - Random data generation utilities
* :mod:`hbutils.reflection` - Reflection and introspection utilities
* :mod:`hbutils.scale` - Size and time scaling utilities
* :mod:`hbutils.string` - String manipulation and formatting
* :mod:`hbutils.system` - System-level utilities (filesystem, git, network, OS, Python)
* :mod:`hbutils.testing` - Testing utilities and helpers

Example::

    >>> import hbutils
    >>> print(hbutils.__version__)
    '0.14.2'

"""

from .config.meta import __VERSION__ as __version__
