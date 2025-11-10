"""
Module for checking command availability in the system environment.

This module provides utilities to verify if executable commands exist in the system PATH,
similar to the ``command -v`` functionality in Linux shells. It wraps the system's ``which``
command to provide a simple boolean interface for command existence checks.
"""

from ...system import which

__all__ = ['cmdv']


def cmdv(execfile: str) -> bool:
    """
    Check if the given command exists in this environment.
    
    This function behaves like the ``command -v xxx`` command in Linux, checking whether
    an executable file is available in the system PATH. It is useful for verifying
    dependencies or determining platform-specific command availability.

    :param execfile: Executable file name to check, such as ``python``, ``bash``, or ``apt-get``.
    :type execfile: str
    
    :return: True if the executable file exists in the system PATH, False otherwise.
    :rtype: bool

    Examples::
        >>> from hbutils.testing import cmdv
        >>>
        >>> cmdv('apt-get')  # should exist on Ubuntu
        True
        >>> cmdv('bash')  # should exist on Linux
        True
        >>> cmdv('cmd')  # should exist on Windows
        False
        >>> cmdv('not_installed')
        False
    """
    return bool(which(execfile))
