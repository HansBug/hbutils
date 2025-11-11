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

r"""
Overview:
    Library for formatting trees.

    This is a copy of https://github.com/jml/tree-format, with a few modifications,
    its based commit id is 4c6de1074d96129b7e03eecdf42fac2cde3b5151.

Changes:
    - The ``NEWLINE`` value is modified to empty string for the vision of final tree.
    - The ``print_tree`` function is removed because it is nowhere to be used in our case.
    - Add ``__doc__`` for ``format_tree`` function.
    - All the ``\n`` strings are replaced to ``os.linesep``.
    - The code is reformatted.
"""

import itertools
import os
import sys
from typing import Callable, Any, Iterable

__all__ = [
    'format_tree',
]

_DEFAULT_ENCODING = os.environ.get("PYTHONIOENCODING", sys.getdefaultencoding())

_UTF8_CHARS = (u'\u251c', u'\u2514', u'\u2502', u'\u2500', u'')
_ASCII_CHARS = (u'+', u'`', u'|', u'-', u'')


def _format_newlines(prefix: str, formatted_node: str, chars: tuple) -> str:
    """
    Convert newlines into U+23EC characters, followed by an actual newline and
    then a tree prefix so as to position the remaining text under the previous line.

    :param prefix: The prefix string to add before each line.
    :type prefix: str
    :param formatted_node: The formatted node string that may contain newlines.
    :type formatted_node: str
    :param chars: Tuple of characters used for tree formatting (FORK, LAST, VERTICAL, HORIZONTAL, NEWLINE).
    :type chars: tuple

    :return: The formatted string with newlines replaced by tree prefixes.
    :rtype: str
    """
    FORK, LAST, VERTICAL, HORIZONTAL, NEWLINE = chars
    replacement = u''.join([NEWLINE, os.linesep, prefix])
    return replacement.join(formatted_node.splitlines())


def _format_tree(node: Any, format_node: Callable[[Any], str], get_children: Callable[[Any], Iterable[Any]],
                 prefix: str = u'', chars: tuple = _UTF8_CHARS) -> Iterable[str]:
    """
    Recursively format a tree structure into a list of formatted strings.

    :param node: The current node to format.
    :type node: Any
    :param format_node: Function to format a node into a string.
    :type format_node: Callable[[Any], str]
    :param get_children: Function to get children of a node.
    :type get_children: Callable[[Any], Iterable[Any]]
    :param prefix: The prefix string for the current level of indentation.
    :type prefix: str
    :param chars: Tuple of characters used for tree formatting (FORK, LAST, VERTICAL, HORIZONTAL, NEWLINE).
    :type chars: tuple

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
                encoding: str = None) -> str:
    r"""
    Format the given tree structure into a string representation with tree-like visual formatting.

    :param node: The root node of the tree to format.
    :type node: Any
    :param format_node: Function that takes a node and returns its string representation.
    :type format_node: Callable[[Any], str]
    :param get_children: Function that takes a node and returns an iterable of its children.
    :type get_children: Callable[[Any], Iterable[Any]]
    :param encoding: Encoding to be used. Default is ``None`` which means system encoding. \
        When ASCII encoding is used, ASCII chars will be used instead of UTF-8 box-drawing characters.
    :type encoding: str

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
