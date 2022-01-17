"""
Overview:
    Useful utilities for truncate (shorten) your string.
"""
from textwrap import shorten as _shorten

__all__ = ['truncate']


def truncate(text: str, width: int = 70, tail_length: int = 0, show_length: bool = False):
    """
    Overview:
        Truncate string into short form.

    Arguments:
        - text (:obj:`str`): Original text to be truncated.
        - width (:obj:`int`): Final width of the new string, default is ``70``.
        - tail_length (:obj:`int`): Tail's length of the new string, \
            default is ``0`` which means no tail.
        - show_length (:obj:`bool`): Show length in middle part or not, \
            default is ``False`` which means do not show this.

    Returns:
        - shortened (:obj:`str`) Short-formed string.

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
