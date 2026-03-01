"""
Package metadata constants for the :mod:`hbutils` project.

This module provides centralized metadata attributes for the ``hbutils`` package,
including the project title, version, description, and author information. These
constants are primarily used in packaging and distribution workflows (e.g.,
``setup.py`` or ``pyproject.toml`` configurations).

The module contains the following public constants:

* :data:`__TITLE__` - Package title identifier
* :data:`__VERSION__` - Current package version
* :data:`__DESCRIPTION__` - Short project description
* :data:`__AUTHOR__` - Package author name
* :data:`__AUTHOR_EMAIL__` - Contact email for the author

Example::

    >>> from hbutils.config.meta import __TITLE__, __VERSION__
    >>> print(f"{__TITLE__} v{__VERSION__}")
    hbutils v0.14.2

.. note::
   These values are meant to be imported and used by packaging tools or to
   expose metadata at runtime.

"""

#: Title of this project (should be `hbutils`).
__TITLE__: str = "hbutils"

#: Version of this project.
__VERSION__: str = "0.14.2"

#: Short description of the project, will be included in ``setup.py``.
__DESCRIPTION__: str = 'Some useful functions and classes in Python infrastructure development.'

#: Author of this project.
__AUTHOR__: str = "HansBug"

#: Email of the authors'.
__AUTHOR_EMAIL__: str = "hansbug@buaa.edu.cn"
