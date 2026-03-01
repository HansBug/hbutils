"""
Automatic binary decoding utilities.

This module provides helpers for decoding binary data into text by attempting
multiple encodings. The primary entry point is :func:`auto_decode`, which
tries an explicit encoding if provided, then a list of preferred encodings,
and finally uses system defaults and the :mod:`chardet` detector.

The module contains the following main components:

* :func:`auto_decode` - Automatically decode bytes into text using multiple strategies

.. note::
   Decoding results depend on the provided byte stream and the available
   encodings in the runtime environment.

Example::

    >>> from hbutils.encoding.decode import auto_decode
    >>> auto_decode(b'kdsfjldsjflkdsmgds')
    'kdsfjldsjflkdsmgds'
    >>> auto_decode(b'\\xd0\\x94\\xd0\\xbe\\xd0\\xb1\\xd1\\x80\\xd1\\x8b\\xd0\\xb9')
    'Добрый'

"""
import sys
from typing import Optional, List

import chardet

from ..collection import unique

_DEFAULT_ENCODING = 'utf-8'
_DEFAULT_PREFERRED_ENCODINGS = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']  # common encodings for Chinese text

__all__ = [
    'auto_decode'
]


def _decode(data: bytes, encoding: str) -> str:
    """
    Decode binary data using the specified encoding.

    :param data: Binary data to decode.
    :type data: bytes
    :param encoding: Encoding to use for decoding.
    :type encoding: str
    :return: Decoded string.
    :rtype: str
    :raises UnicodeDecodeError: If decoding fails with the specified encoding.
    :raises LookupError: If the specified encoding is unknown.

    Example::

        >>> _decode(b'hello', 'utf-8')
        'hello'
    """
    return data.decode(encoding)


def auto_decode(data: bytes, encoding: Optional[str] = None, prefers: Optional[List[str]] = None) -> str:
    r"""
    Automatically decode binary data into text.

    This function attempts to decode binary data using multiple strategies:

    1. If an ``encoding`` is explicitly specified, it is used directly.
    2. Otherwise, preferred encodings are tried in order.
    3. The system default encoding is tried next.
    4. Finally, the :mod:`chardet` library is used to detect a likely encoding.

    The function tries each encoding until one succeeds. If all attempts fail,
    the :class:`UnicodeDecodeError` with the longest successful decode position
    is raised.

    :param data: Original binary data to be decoded.
    :type data: bytes
    :param encoding: Encoding to use explicitly. If ``None``, the encoding will
        be automatically detected using the described strategy.
    :type encoding: Optional[str]
    :param prefers: Preferred encodings to try first. If ``None``, the default
        preferred encodings (``utf-8``, ``gbk``, ``gb2312``, ``gb18030``,
        ``big5``) are used.
    :type prefers: Optional[List[str]]
    :return: Decoded string.
    :rtype: str
    :raises UnicodeDecodeError: If all decoding attempts fail.
    :raises LookupError: If any attempted encoding is unknown.

    .. note::
       The detection step uses :func:`chardet.detect`, which may return ``None``
       as the detected encoding; such values are ignored.

    Examples::

        >>> auto_decode(b'kdsfjldsjflkdsmgds')
        'kdsfjldsjflkdsmgds'
        >>> auto_decode(b'\\xd0\\x94\\xd0\\xbe\\xd0\\xb1\\xd1\\x80\\xd1\\x8b\\xd0\\xb9 \\xd0'
        ...             b'\\xb2\\xd0\\xb5\\xd1\\x87\\xd0\\xb5\\xd1\\x80')
        'Добрый вечер'
        >>> auto_decode(b'\\xa4\\xb3\\xa4\\xf3\\xa4\\xd0\\xa4\\xf3\\xa4\\xcf')
        'こんばんは'
        >>> auto_decode(b'\\xcd\\xed\\xc9\\xcf\\xba\\xc3')
        '晚上好'
    """
    if encoding:
        return _decode(data, encoding)
    else:
        if prefers is None:
            prefers = _DEFAULT_PREFERRED_ENCODINGS
        _elist = filter(bool, unique([
            *prefers,
            sys.getdefaultencoding(),
            chardet.detect(data)['encoding']
        ]))

        last_err: Optional[UnicodeDecodeError] = None
        for enc in _elist:
            try:
                return _decode(data, enc)
            except UnicodeDecodeError as err:
                if last_err is None or err.start > last_err.start:
                    last_err = err

        raise last_err
