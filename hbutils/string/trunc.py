"""
Overview:
    Useful utilities for truncate (shorten) your string.
    
This module provides functionality to truncate long strings into shorter forms
with customizable options for width, tail display, and length indication.
"""
from textwrap import shorten as _shorten

__all__ = ['truncate']


def truncate(text: str, width: int = 70, tail_length: int = 0, show_length: bool = False) -> str:
    """
    Truncate string into short form.
    
    This function shortens a given text to a specified width, optionally showing
    the tail portion of the original text and/or the total character count.

    :param text: Original text to be truncated.
    :type text: str
    :param width: Final width of the new string, default is ``70``.
    :type width: int
    :param tail_length: Tail's length of the new string, default is ``0`` which means no tail.
    :type tail_length: int
    :param show_length: Show length in middle part or not, default is ``False`` which means do not show this.
    :type show_length: bool
    
    :return: Short-formed string.
    :rtype: str

    Examples::
        >>> from hbutils.string import truncate
        >>> truncate('abc ' * 30, width=30)
        'abc abc abc abc abc abc ... '
        >>> truncate('abc ' * 30, width=40, tail_length=10)
        'abc abc abc abc abc abc ... c abc abc '
        >>> truncate('abc ' * 30, width=40, tail_length=10, show_length=True)
        'abc abc abc ..(120 chars).. c abc abc '

    """
    text = str(text)

    if show_length:
        omission = ' ..({length} chars).. '.format(length=len(text))
    else:
        omission = ' ... '
    if tail_length:
        omission += text[len(text) - tail_length:]

    return _shorten(text, width=width, placeholder=omission)
