from ...system import which

__all__ = ['cmdv']


def cmdv(execfile: str) -> bool:
    """
    Overview:
        Check if the given command is exist in this environment, like the ``command -v xxx`` command in Linux.

    :param execfile: Executable file, such as ``python``.
    :return: This executable file is exist or not.

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
