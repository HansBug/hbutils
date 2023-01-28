"""
Overview:
    Functions to deal with encoding binary data easily.
"""
import sys
from typing import Optional, List

import chardet

from ..collection import unique

_DEFAULT_ENCODING = 'utf-8'
_DEFAULT_PREFERRED_ENCODINGS = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']  # common encodings for chinese

__all__ = [
    'auto_decode'
]


def _decode(data: bytes, encoding: str) -> str:
    return data.decode(encoding)


def auto_decode(data: bytes, encoding: Optional[str] = None, prefers: Optional[List[str]] = None) -> str:
    r"""
    Overview:
        Auto decode binary data to string, the encoding mode will be automatically detected.

    Arguments:
        - data (:obj:`bytes`): Original binary data to be decoded.
        - encoding (:obj:`Optional[str]`): Encoding mode to be used, default is ``None`` which \
            means this function need to automatically detect the encoding.
        - prefers (:obj:`Optional[List[str]]`): Prefered encodings.

    Returns:
        - str (:obj:`str`): Decoded string.

    Examples::

        >>> auto_decode(b'kdsfjldsjflkdsmgds')  # 'kdsfjldsjflkdsmgds'
        >>> auto_decode(b'\xd0\x94\xd0\xbe\xd0\xb1\xd1\x80\xd1\x8b\xd0\xb9 \xd0'
        ...             b'\xb2\xd0\xb5\xd1\x87\xd0\xb5\xd1\x80')  # "Добрый вечер"
        >>> auto_decode(b'\xa4\xb3\xa4\xf3\xa4\xd0\xa4\xf3\xa4\xcf')  # "こんばんは"
        >>> auto_decode(b'\xcd\xed\xc9\xcf\xba\xc3')  # "晚上好"
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

        last_err = None
        for enc in _elist:
            try:
                return _decode(data, enc)
            except UnicodeDecodeError as err:
                if last_err is None or err.start > last_err.start:
                    last_err = err

        raise last_err
