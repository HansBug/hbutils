"""
Overview:
    Base64 encode and decode.
"""
import base64
import warnings
from typing import Optional

__all__ = [
    'base64_encode', 'base64_decode',
]


def base64_encode(data: bytes, altchars: Optional[bytes] = None, urlsafe: bool = False) -> str:
    r"""
    Overview:
        Encoding the given binary ``data`` to base64 string.

    Arguments:
        - data (:obj:`bytes`): Binary data to be encoded.
        - altchars (:obj:`Optional[bytes]`): Characters to be altered, default is ``None``.
        - urlsafe (:obj:`bool`): Enable urlsafe mode, default is ``False``.

    Examples::

        >>> base64_encode(b'jvMIQ?K;]kNn2?1KD5H>')
        anZNSVE/Sztda05uMj8xS0Q1SD4=
        >>> base64_encode(b'jvMIQ?K;]kNn2?1KD5H>', urlsafe=True)
        anZNSVE_Sztda05uMj8xS0Q1SD4=
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
    Overview:
        Decode the given base64 string ``base64_str`` back to binary data.

    Arguments:
        - base64_str (:obj:`str`): Base64 string to be decoded.
        - altchars (:obj:`Optional[bytes]`): Characters to be altered, default is ``None``.
        - urlsafe (:obj:`bool`): Enable urlsafe mode, default is ``False``.

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
