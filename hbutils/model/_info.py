"""
Package metadata for :mod:`hbutils.model`.

This module centralizes core metadata for the :mod:`hbutils.model` package,
including its canonical name, homepage URL, and a reStructuredText (RST)
reference string pointing to the documentation.

The module contains the following main components:

* :data:`_PACKAGE_NAME` - Canonical package name
* :data:`_PACKAGE_HOMEPAGE` - Documentation homepage URL
* :data:`_PACKAGE_RST` - RST-formatted link to the homepage

Example::

    >>> from hbutils.model import _info
    >>> _info._PACKAGE_NAME
    'hbutils.model'
    >>> _info._PACKAGE_HOMEPAGE
    'https://hansbug.github.io/hbutils/main/api_doc/model/index.html'
    >>> _info._PACKAGE_RST
    '`hbutils.model <https://hansbug.github.io/hbutils/main/api_doc/model/index.html>`_'

"""

# Package information for hbutils.model.
_PACKAGE_NAME: str = 'hbutils.model'
_PACKAGE_HOMEPAGE: str = 'https://hansbug.github.io/hbutils/main/api_doc/model/index.html'
_PACKAGE_RST: str = f'`{_PACKAGE_NAME} <{_PACKAGE_HOMEPAGE}>`_'
