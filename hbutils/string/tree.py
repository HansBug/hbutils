# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Jonathan M. Lange <jml@mumak.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This is a copy of https://github.com/jml/tree-format, with a few modifications,
# its based commit id is 4c6de1074d96129b7e03eecdf42fac2cde3b5151.

"""
Tree formatting utilities.

This module provides helper utilities for formatting arbitrary tree structures
into a text-based representation using Unicode box-drawing characters or ASCII
fallback characters. The core public API is :func:`format_tree`, which accepts
custom formatting and child-fetching callbacks to support a wide range of data
structures.

The module is a modified variant of `jml/tree-format` with the following changes:

* The newline character used in the internal formatting is an empty string to
  match the expected final tree output format.
* The original ``print_tree`` helper is removed.
* ``\\n`` strings are replaced with :data:`os.linesep` to respect the host
  operating system's line separator.
* Code is reformatted for readability.

The module contains the following main component:

* :func:`format_tree` - Format a tree structure into a human-readable string.

Example::

    >>> from operator import itemgetter
    >>> from hbutils.string.tree import format_tree
    >>>
    >>> tree = (
    ...     'root', [
    ...         ('child', []),
    ...         ('branch', [
    ...             ('leaf', []),
    ...         ]),
    ...     ],
    ... )
    >>> print(format_tree(tree, format_node=itemgetter(0), get_children=itemgetter(1)))
    root
    ├── child
    └── branch
        └── leaf

.. note::
   The :func:`format_tree` function uses UTF-8 box-drawing characters by default
   and falls back to ASCII characters if the encoding indicates ASCII usage.

"""

import itertools
import os
import sys
from typing import Callable, Any, Iterable, Optional, Tuple

__all__ = [
    'format_tree',
]

_DEFAULT_ENCODING = os.environ.get("PYTHONIOENCODING", sys.getdefaultencoding())

_UTF8_CHARS = (u'\u251c', u'\u2514', u'\u2502', u'\u2500', u'')
_ASCII_CHARS = (u'+', u'`', u'|', u'-', u'')


def _format_newlines(prefix: str, formatted_node: str, chars: Tuple[str, str, str, str, str]) -> str:
    """
    Convert newlines into tree-prefixed lines.

    This helper replaces the line breaks in ``formatted_node`` with the provided
    prefix, ensuring that subsequent lines are aligned with the tree branch
    indentation.

    :param prefix: The prefix string to add before each continuation line.
    :type prefix: str
    :param formatted_node: The formatted node string that may contain newlines.
    :type formatted_node: str
    :param chars: Tuple of characters used for tree formatting
                  ``(FORK, LAST, VERTICAL, HORIZONTAL, NEWLINE)``.
    :type chars: tuple[str, str, str, str, str]
    :return: The formatted string with newlines replaced by tree prefixes.
    :rtype: str
    """
    FORK, LAST, VERTICAL, HORIZONTAL, NEWLINE = chars
    replacement = u''.join([NEWLINE, os.linesep, prefix])
    return replacement.join(formatted_node.splitlines())


def _format_tree(node: Any, format_node: Callable[[Any], str], get_children: Callable[[Any], Iterable[Any]],
                 prefix: str = u'', chars: Tuple[str, str, str, str, str] = _UTF8_CHARS) -> Iterable[str]:
    """
    Recursively format a tree structure into a sequence of formatted strings.

    This function traverses the tree defined by ``node`` and yields formatted
    lines representing each branch and leaf using the provided formatting
    characters.

    :param node: The current node to format.
    :type node: Any
    :param format_node: Function to format a node into a string.
    :type format_node: Callable[[Any], str]
    :param get_children: Function to get children of a node.
    :type get_children: Callable[[Any], Iterable[Any]]
    :param prefix: The prefix string for the current level of indentation.
    :type prefix: str
    :param chars: Tuple of characters used for tree formatting
                  ``(FORK, LAST, VERTICAL, HORIZONTAL, NEWLINE)``.
    :type chars: tuple[str, str, str, str, str]
    :return: Generator yielding formatted strings for the tree structure.
    :rtype: Iterable[str]
    """
    FORK, LAST, VERTICAL, HORIZONTAL, NEWLINE = chars
    children = list(get_children(node))
    next_prefix = u''.join([prefix, VERTICAL, u'   '])
    for child in children[:-1]:
        yield u''.join([
            prefix, FORK, HORIZONTAL, HORIZONTAL, u' ',
            _format_newlines(next_prefix, format_node(child), chars)])
        for result in _format_tree(child, format_node, get_children, next_prefix, chars):
            yield result
    if children:
        last_prefix = u''.join([prefix, u'    '])
        yield u''.join([
            prefix, LAST, HORIZONTAL, HORIZONTAL, u' ',
            _format_newlines(last_prefix, format_node(children[-1]), chars)])
        for result in _format_tree(children[-1], format_node, get_children, last_prefix, chars):
            yield result


def format_tree(node: Any, format_node: Callable[[Any], str], get_children: Callable[[Any], Iterable[Any]],
                encoding: Optional[str] = None) -> str:
    r"""
    Format the given tree structure into a string representation with tree-like visual formatting.

    :param node: The root node of the tree to format.
    :type node: Any
    :param format_node: Function that takes a node and returns its string representation.
    :type format_node: Callable[[Any], str]
    :param get_children: Function that takes a node and returns an iterable of its children.
    :type get_children: Callable[[Any], Iterable[Any]]
    :param encoding: Encoding to be used. Default is ``None`` which means system encoding.
        When ASCII encoding is used, ASCII chars will be used instead of UTF-8 box-drawing characters.
    :type encoding: str, optional

    :return: Formatted tree string with visual tree structure.
    :rtype: str

    Example::
        >>> from operator import itemgetter
        >>>
        >>> from hbutils.string import format_tree
        >>>
        >>> tree = (
        ...     'foo', [
        ...         ('bar', [
        ...             ('a', []),
        ...             ('b', []),
        ...         ]),
        ...         ('baz', []),
        ...         ('qux', [
        ...             ('c\nd', []),
        ...         ]),
        ...     ],
        ... )
        >>> print(format_tree(tree, format_node=itemgetter(0), get_children=itemgetter(1)))
        foo
        ├── bar
        │   ├── a
        │   └── b
        ├── baz
        └── qux
            └── c
                d
    """
    if 'ASCII' in (encoding or _DEFAULT_ENCODING).upper():
        _chars = _ASCII_CHARS
    else:
        _chars = _UTF8_CHARS

    return os.linesep.join(itertools.chain(
        [format_node(node)],
        _format_tree(node, format_node, get_children, u'', _chars),
        [u''],
    ))
