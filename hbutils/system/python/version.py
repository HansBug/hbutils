"""
Python version inspection utilities.

This module provides a lightweight helper for retrieving the current Python
interpreter version as a :class:`packaging.version.Version` instance. The
returned object offers rich comparison semantics, making it suitable for
version checks and conditional logic in system-dependent workflows.

The module contains the following main components:

* :func:`python_version` - Retrieve the interpreter version as a
  :class:`packaging.version.Version` object.

Example::

    >>> from hbutils.system.python.version import python_version
    >>> ver = python_version()
    >>> ver >= Version("3.8")
    True

.. note::
   This module relies on :mod:`platform` to query the interpreter version and
   uses :class:`packaging.version.Version` for standardized parsing.

"""

import platform

from packaging.version import Version

__all__ = [
    'python_version',
]


def python_version() -> Version:
    """
    Retrieve the current Python interpreter version.

    This function queries the running Python interpreter using
    :func:`platform.python_version` and returns a parsed
    :class:`packaging.version.Version` instance. The returned object can be
    compared directly with other version strings or :class:`Version` instances.

    :return: The current Python interpreter version.
    :rtype: Version

    Example::

        >>> from hbutils.system.python.version import python_version
        >>> python_version()  # doctest: +ELLIPSIS
        Version('...')

    """
    return Version(platform.python_version())
