"""
Git installation inspection utilities.

This module serves as the public entry point for Git-related system utilities.
It re-exports all public objects from :mod:`hbutils.system.git.info`, providing
a concise API for retrieving information about Git and Git LFS installations.

The module focuses on:

* Discovering whether Git is installed.
* Retrieving Git version information.
* Detecting Git LFS and retrieving its version details.

The following public functions are commonly used:

* :func:`git_info` - Retrieve Git installation information.
* :func:`git_lfs_info` - Retrieve Git LFS installation information.

.. note::
   All functionality is implemented in :mod:`hbutils.system.git.info`. This
   module simply exposes that API for convenient import paths.

Example::

    >>> from hbutils.system.git import git_info
    >>> info = git_info()
    >>> if info['installed']:
    ...     print(f"Git version: {info['version']}")
    ...     if info['lfs']['installed']:
    ...         print(f"Git LFS version: {info['lfs']['version']}")

"""

from .info import *
