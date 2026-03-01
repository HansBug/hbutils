"""
String processing package entry point for :mod:`hbutils.string`.

This module aggregates and re-exports the public utilities from the string
processing submodules, providing a unified interface for common string
manipulation tasks such as inflection, pluralization, templating, tree
representation, and truncation.

The main components are re-exported from the following submodules:

* :mod:`hbutils.string.inflection` - String inflection utilities such as case conversions.
* :mod:`hbutils.string.plural` - Pluralization and singularization helpers.
* :mod:`hbutils.string.template` - String templating utilities.
* :mod:`hbutils.string.tree` - Tree structure string representation helpers.
* :mod:`hbutils.string.trunc` - String truncation utilities.

This module serves as the primary access point for the package, enabling
wildcard imports to pull in all public APIs from the submodules.

Example::

    >>> from hbutils.string import camelize, pluralize
    >>> camelize('hello_world')
    'HelloWorld'
    >>> pluralize('box')
    'boxes'

.. note::
   The actual public functions and classes are defined in the submodules and
   are re-exported here for convenience. Refer to each submodule's
   documentation for detailed API references and usage.
"""
from .inflection import *
from .plural import *
from .template import *
from .tree import *
from .trunc import *
