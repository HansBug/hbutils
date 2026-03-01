"""
String truncation utilities for producing readable short text previews.

This module provides functionality for truncating long strings into shorter
forms with customizable output width, optional tail display, and optional
length indicators. The core public utility is :func:`truncate`, which is a
thin wrapper around :func:`textwrap.shorten` with additional placeholder
configuration.

The module contains the following main components:

* :func:`truncate` - Truncate text with optional tail and length indicators.

.. note::
   The underlying implementation relies on :func:`textwrap.shorten`, which
   collapses consecutive whitespace and attempts to break on word boundaries.

.. warning::
   If the ``width`` is smaller than the placeholder length produced by
   ``show_length`` and ``tail_length`` options, :func:`textwrap.shorten` will
   raise :class:`ValueError`.

Example::

    >>> from hbutils.string.trunc import truncate
    >>> truncate('abc ' * 30, width=30)
    'abc abc abc abc abc abc ... '
    >>> truncate('abc ' * 30, width=40, tail_length=10)
    'abc abc abc abc abc abc ... c abc abc '
    >>> truncate('abc ' * 30, width=40, tail_length=10, show_length=True)
    'abc abc abc ..(120 chars).. c abc abc '

"""
from textwrap import shorten as _shorten

__all__ = ['truncate']


def truncate(text: str, width: int = 70, tail_length: int = 0, show_length: bool = False) -> str:
    """
    Truncate a string into a short, readable form.

    This function shortens the given ``text`` to fit within ``width``
    characters. The truncation placeholder can include the total character
    count of the original text and an optional tail segment, controlled via
    ``show_length`` and ``tail_length``. Internally, :func:`textwrap.shorten`
    is used, meaning whitespace is normalized and truncation occurs on word
    boundaries where possible.

    :param text: Original text to be truncated.
    :type text: str
    :param width: Maximum width of the resulting string, defaults to ``70``.
    :type width: int, optional
    :param tail_length: Number of characters from the end of ``text`` to
        append to the placeholder, defaults to ``0`` (no tail).
    :type tail_length: int, optional
    :param show_length: Whether to include the original text length in the
        placeholder, defaults to ``False``.
    :type show_length: bool, optional
    :return: Truncated string fitting within the given width.
    :rtype: str
    :raises ValueError: If ``width`` is smaller than the computed placeholder
        length, as enforced by :func:`textwrap.shorten`.

    .. note::
       The input is converted to ``str`` before processing, so non-string
       inputs will be stringified.

    Example::

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
