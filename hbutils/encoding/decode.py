"""
Overview:
    Functions to deal with encoding binary data easily.
"""
from typing import Optional

import chardet

_DEFAULT_ENCODING = 'utf-8'
_ENCODING_LIST = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']  # common encodings for chinese

__all__ = [
    'auto_decode'
]


def auto_decode(data: bytes, encoding: Optional[str] = None) -> str:
    r"""
    Overview:
        Auto decode binary data to string, the encoding mode will be automatically detected.

    Arguments:
        - data (:obj:`bytes`): Original binary data to be decoded.
        - encoding (:obj:`Optional[str]`): Encoding mode to be used, default is ``None`` which \
            means this function need to automatically detect the encoding.

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
        return data.decode(encoding)
    else:
        auto_encoding = chardet.detect(data)['encoding']
        if auto_encoding and auto_encoding not in _ENCODING_LIST:
            _list = _ENCODING_LIST + [auto_encoding]
        else:
            _list = _ENCODING_LIST

        last_err = None
        for enc in _list:
            try:
                return data.decode(encoding=enc)
            except UnicodeDecodeError as err:
                last_err = err

        raise last_err
