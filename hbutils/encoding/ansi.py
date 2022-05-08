"""
Overview:
    Functions for ansi escaping and unescapes.
    See `ANSI escape code - Wikipedia <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.
"""
import re

__all__ = [
    'ansi_unescape',
]

_ANSI_PATTERN = re.compile(r'\x1B\[\d+(;\d+){0,2}m')


def ansi_unescape(string: str) -> str:
    """
    Overview:
        Unescape ansi string.
        See `ANSI escape code - Wikipedia <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.

    :param string: Original output string.
    :return unescaped: Unescaped ansi string.

    Examples::
        >>> from hbutils.encoding import ansi_unescape
        >>> ansi_unescape("\x1b[1;31mHello")
        'Hello'
        >>> ansi_unescape("\x1b[2;37;41mWorld")
        'World'
    """
    return _ANSI_PATTERN.sub('', string)
