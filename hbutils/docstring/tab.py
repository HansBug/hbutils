"""
Overview:
    Processing of docstring.
"""
import os
import re

__all__ = [
    'untab',
]

_WHILE_CHARS_PREFIX = re.compile(r'^([ \t]*)')


def untab(doc: str) -> str:
    """
    Overview:
        Untab the docstring.

    Args:
        - doc (:obj:`str`): Original doc string.

    Returns:
        - untabbed (:obj:`str`): Untabbed doc string.

    Examples::
        >>> def func(a, b):
        ...     '''
        ...     Overview:
        ...         This is function ``func``.
        ...
        ...     Args:
        ...         - a: First argument
        ...         - b: Second argument
        ...     '''
        ...     pass
        ...
        >>> print(func.__doc__)
            Overview:
                This is function ``func``.
            Args:
                - a: First argument
                - b: Second argument

        >>>
        >>> from hbutils.docstring import untab
        >>> print(untab(func.__doc__))
        Overview:
            This is function ``func``.
        Args:
            - a: First argument
            - b: Second argument

        .. note::
            In these cases, the empty lines are preserved in their original position. \
            They were removed from the documentation due to a typographical problem.

    """
    prefixes = []
    lines = []
    for line in doc.splitlines():
        if line.strip():
            prefixes.append(_WHILE_CHARS_PREFIX.match(line).group(1))
            lines.append(line)
        else:
            lines.append(None)

    mlen = min(map(len, prefixes)) if prefixes else 0
    return os.linesep.join([
        line[mlen:] if line is not None else ''
        for line in lines
    ])
