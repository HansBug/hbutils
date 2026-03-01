"""
System requirement predicates for conditional test execution.

This package module aggregates a collection of requirement checkers that are
commonly used with conditional test decorators such as
:func:`unittest.skipUnless` or ``pytest.mark.skipUnless``. The available
predicates and objects are imported from the following submodules:

* :mod:`hbutils.testing.requires.cmd` - command availability checks
* :mod:`hbutils.testing.requires.expr` - Python version and implementation expressions
* :mod:`hbutils.testing.requires.git` - Git and Git LFS availability checks

The module exposes these utilities at the package level via ``import *`` to
provide a concise import experience for test suites.

Example::

    >>> from hbutils.testing.requires import vpython, is_git_installed
    >>> # Check the current Python version (evaluated at runtime)
    >>> vpython >= '3.7'
    True
    >>> # Check whether Git is installed on the system
    >>> is_git_installed()
    True

.. note::
   The exported names depend on the corresponding submodules. Refer to
   :mod:`hbutils.testing.requires.cmd`, :mod:`hbutils.testing.requires.expr`,
   and :mod:`hbutils.testing.requires.git` for detailed descriptions of
   individual utilities.

"""
from .cmd import *
from .expr import *
from .git import *
