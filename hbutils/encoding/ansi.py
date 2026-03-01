"""
ANSI escape sequence utilities.

This module provides lightweight utilities for removing ANSI escape sequences
from text. ANSI escape codes are commonly used by terminals to apply formatting
such as colors and styles. The primary public API is :func:`ansi_unescape`,
which strips these sequences and returns plain text.

The module contains the following main components:

* :func:`ansi_unescape` - Remove ANSI escape sequences from a string.

.. note::
   This module focuses on the most common CSI "SGR" color/style sequences
   (e.g., ``\\x1b[31m`` or ``\\x1b[1;32m``). Other escape sequences are not
   processed by the current implementation.

Example::

    >>> from hbutils.encoding.ansi import ansi_unescape
    >>> ansi_unescape("\\x1b[1;31mHello\\x1b[0m")
    'Hello'

"""
import re

__all__ = [
    'ansi_unescape',
]

_ANSI_PATTERN = re.compile(r'\x1B\[\d+(;\d+){0,2}m')


def ansi_unescape(string: str) -> str:
    """
    Remove ANSI escape codes from a string.

    This function strips common ANSI SGR (Select Graphic Rendition) escape
    sequences used for terminal text formatting. It operates by matching
    sequences such as ``\\x1b[31m`` or ``\\x1b[1;32m`` and removing them,
    returning only the unformatted text.

    See `ANSI escape code - Wikipedia <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.

    :param string: Original string that may contain ANSI escape sequences.
    :type string: str
    :return: String with ANSI escape sequences removed.
    :rtype: str

    Example::

        >>> from hbutils.encoding import ansi_unescape
        >>> ansi_unescape("\\x1b[1;31mHello")  # Remove red bold formatting
        'Hello'
        >>> ansi_unescape("\\x1b[2;37;41mWorld")  # Remove dim white on red background
        'World'

    .. warning::
       Only ANSI SGR sequences matching the pattern ``\\x1b[...m`` with up to
       two semicolon-separated numeric parameters are removed. Other ANSI
       control sequences are left intact.
    """
    return _ANSI_PATTERN.sub('', string)
