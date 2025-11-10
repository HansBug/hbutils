"""
Overview:
    Functions for ansi escaping and unescapes.
    See `ANSI escape code - Wikipedia <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.
    
    This module provides utilities to remove ANSI escape codes from strings, which are commonly
    used for terminal text formatting (colors, styles, etc.). The main functionality is to clean
    strings by removing these escape sequences, leaving only the plain text content.
"""
import re

__all__ = [
    'ansi_unescape',
]

_ANSI_PATTERN = re.compile(r'\x1B\[\d+(;\d+){0,2}m')


def ansi_unescape(string: str) -> str:
    """
    Unescape ansi string by removing ANSI escape codes.
    
    This function removes ANSI escape sequences from the input string, which are typically
    used for terminal text formatting such as colors, bold, underline, etc. The function
    uses a regular expression pattern to match and remove these escape codes.
    
    See `ANSI escape code - Wikipedia <https://en.wikipedia.org/wiki/ANSI_escape_code>`_.

    :param string: Original output string containing ANSI escape codes.
    :type string: str
    
    :return: Unescaped ansi string with all ANSI escape codes removed.
    :rtype: str

    Examples::
        >>> from hbutils.encoding import ansi_unescape
        >>> ansi_unescape("\x1b[1;31mHello")  # Remove red bold formatting
        'Hello'
        >>> ansi_unescape("\x1b[2;37;41mWorld")  # Remove dim white text on red background
        'World'
    """
    return _ANSI_PATTERN.sub('', string)
