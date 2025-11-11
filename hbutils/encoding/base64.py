"""
Overview:
    Base64 encode and decode utilities.
    
    This module provides convenient wrapper functions for base64 encoding and decoding operations,
    supporting both standard and URL-safe base64 formats. It simplifies the usage of Python's
    built-in base64 module by providing a cleaner interface with optional URL-safe mode.
"""
import base64
import warnings
from typing import Optional

__all__ = [
    'base64_encode', 'base64_decode',
]


def base64_encode(data: bytes, altchars: Optional[bytes] = None, urlsafe: bool = False) -> str:
    r"""
    Encoding the given binary data to base64 string.
    
    This function encodes binary data into a base64-encoded string. It supports both standard
    base64 encoding and URL-safe base64 encoding. When URL-safe mode is enabled, the characters
    '+' and '/' in standard base64 are replaced with '-' and '_' respectively.

    :param data: Binary data to be encoded.
    :type data: bytes
    :param altchars: Characters to be altered in standard base64 encoding. This parameter is
                     ignored when urlsafe is True. Default is ``None``.
    :type altchars: Optional[bytes]
    :param urlsafe: Enable URL-safe mode. When True, uses URL-safe base64 encoding which
                    replaces '+' with '-' and '/' with '_'. Default is ``False``.
    :type urlsafe: bool
    
    :return: Base64-encoded string representation of the input data.
    :rtype: str
    
    :raises UserWarning: When both urlsafe is True and altchars is provided, a warning is issued
                         indicating that altchars will be ignored.

    Examples::

        >>> base64_encode(b'jvMIQ?K;]kNn2?1KD5H>')
        'anZNSVE/Sztda05uMj8xS0Q1SD4='
        >>> base64_encode(b'jvMIQ?K;]kNn2?1KD5H>', urlsafe=True)
        'anZNSVE_Sztda05uMj8xS0Q1SD4='
    """
    if urlsafe and altchars:
        warnings.warn(UserWarning('Urlsafe enabled in base64_encode, '
                                  'value altchars argument will be ignored.'), stacklevel=2)

    if urlsafe:
        return base64.urlsafe_b64encode(data).decode()
    else:
        return base64.b64encode(data, altchars).decode()


def base64_decode(base64_str: str, altchars: Optional[bytes] = None, urlsafe: bool = False) -> bytes:
    r"""
    Decode the given base64 string back to binary data.
    
    This function decodes a base64-encoded string back into its original binary form. It supports
    both standard base64 decoding and URL-safe base64 decoding. When URL-safe mode is enabled,
    it properly handles the URL-safe characters '-' and '_' used in place of '+' and '/'.

    :param base64_str: Base64-encoded string to be decoded.
    :type base64_str: str
    :param altchars: Characters to be altered in standard base64 decoding. This parameter is
                     ignored when urlsafe is True. Default is ``None``.
    :type altchars: Optional[bytes]
    :param urlsafe: Enable URL-safe mode. When True, uses URL-safe base64 decoding which
                    handles '-' and '_' characters. Default is ``False``.
    :type urlsafe: bool
    
    :return: Decoded binary data from the base64 string.
    :rtype: bytes
    
    :raises UserWarning: When both urlsafe is True and altchars is provided, a warning is issued
                         indicating that altchars will be ignored.

    Examples::

        >>> base64_decode('anZNSVE/Sztda05uMj8xS0Q1SD4=')
        b'jvMIQ?K;]kNn2?1KD5H>'
        >>> base64_decode('anZNSVE_Sztda05uMj8xS0Q1SD4=', urlsafe=True)
        b'jvMIQ?K;]kNn2?1KD5H>'
    """
    if urlsafe and altchars:
        warnings.warn(UserWarning('Urlsafe enabled in base64_decode, '
                                  'value altchars argument will be ignored.'), stacklevel=2)

    if urlsafe:
        return base64.urlsafe_b64decode(base64_str)
    else:
        return base64.b64decode(base64_str, altchars)
