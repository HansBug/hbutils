"""
Command availability checking utilities.

This module provides a small wrapper around the system ``which`` mechanism to
determine whether a given executable is available in the current environment.
It exposes a single public function for use in tests and environment checks.

The module contains the following main component:

* :func:`cmdv` - Check whether an executable exists in the system ``PATH``.

.. note::
   Internally, this module relies on :func:`hbutils.system.which`, which may be
   deprecated in favor of :func:`shutil.which` in newer versions of the
   dependency.

Example::

    >>> from hbutils.testing.requires.cmd import cmdv
    >>> cmdv('python')  # doctest: +SKIP
    True
    >>> cmdv('not_installed')
    False

"""

from ...system import which

__all__ = ['cmdv']


def cmdv(execfile: str) -> bool:
    """
    Check if the given command exists in this environment.

    This function behaves like the ``command -v`` command in Linux, checking whether
    an executable file is available in the system PATH. It is useful for verifying
    dependencies or determining platform-specific command availability.

    :param execfile: Executable file name to check, such as ``python``, ``bash``,
                     or ``apt-get``.
    :type execfile: str
    :return: ``True`` if the executable file exists in the system PATH, ``False``
             otherwise.
    :rtype: bool

    Example::

        >>> from hbutils.testing import cmdv
        >>> cmdv('bash')  # doctest: +SKIP
        True
        >>> cmdv('not_installed')
        False
    """
    return bool(which(execfile))
