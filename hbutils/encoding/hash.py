"""
This module provides convenient wrapper functions for various cryptographic hash algorithms.

It offers easy-to-use interfaces for MD5, SHA1, SHA2 family (SHA224, SHA256, SHA384, SHA512),
and SHA3 hash functions. All functions take binary data as input and return hexadecimal digest strings.

The module simplifies the usage of Python's hashlib by providing a consistent interface across
different hash algorithms.

Examples::
    >>> from hbutils.encoding import md5, sha256
    >>> md5(b'hello world')
    '5eb63bbbe01eeed093cb22bb8f5acdc3'
    >>> sha256(b'hello world')
    'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
"""

import hashlib
from typing import Callable

__all__ = [
    'md5', 'sha1',
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3',
]


def _hash_algorithm(algo: Callable, binary: bytes) -> str:
    """
    Internal helper function to compute hash digest using the specified algorithm.

    :param algo: Hash algorithm constructor from hashlib module.
    :type algo: Callable
    :param binary: Binary data to be hashed.
    :type binary: bytes
    :return: Hexadecimal digest string of the hashed data.
    :rtype: str
    """
    p = algo()
    p.update(binary)
    return p.hexdigest()


def md5(binary: bytes) -> str:
    """
    Compute MD5 hash of binary data.

    :param binary: Binary data to be hashed.
    :type binary: bytes
    :return: MD5 digest string in hexadecimal format.
    :rtype: str

    Examples::
        >>> from hbutils.encoding import md5
        >>> md5(b'')
        'd41d8cd98f00b204e9800998ecf8427e'
        >>> md5(b'this is a word')
        'cdfc9527f76e296c76cdb331ac2d1d88'
    """
    return _hash_algorithm(hashlib.md5, binary)


def sha1(binary: bytes) -> str:
    """
    Compute SHA1 hash of binary data.

    :param binary: Binary data to be hashed.
    :type binary: bytes
    :return: SHA1 digest string in hexadecimal format.
    :rtype: str

    Examples::
        >>> from hbutils.encoding import sha1
        >>> sha1(b'')
        'da39a3ee5e6b4b0d3255bfef95601890afd80709'
        >>> sha1(b'this is a word')
        '7bf417a6503e185ea6352525b96a4d6ef3b9609b'
    """
    return _hash_algorithm(hashlib.sha1, binary)


def sha224(binary: bytes) -> str:
    """
    Compute SHA224 hash of binary data.

    :param binary: Binary data to be hashed.
    :type binary: bytes
    :return: SHA224 digest string in hexadecimal format.
    :rtype: str

    Examples::
        >>> from hbutils.encoding import sha224
        >>> sha224(b'')
        'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f'
        >>> sha224(b'this is a word')
        '7b994bcffbc9a3689941e541a2e639c20e321b763b744c0d84f6899c'
    """
    return _hash_algorithm(hashlib.sha224, binary)


def sha256(binary: bytes) -> str:
    """
    Compute SHA256 hash of binary data.

    :param binary: Binary data to be hashed.
    :type binary: bytes
    :return: SHA256 digest string in hexadecimal format.
    :rtype: str

    Examples::
        >>> from hbutils.encoding import sha256
        >>> sha256(b'')
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        >>> sha256(b'this is a word')
        '91ccca153f5d3739af1f0d304d033f193b25208d44d371c1304877a6503471bf'
    """
    return _hash_algorithm(hashlib.sha256, binary)


def sha384(binary: bytes) -> str:
    """
    Compute SHA384 hash of binary data.

    :param binary: Binary data to be hashed.
    :type binary: bytes
    :return: SHA384 digest string in hexadecimal format.
    :rtype: str

    Examples::
        >>> from hbutils.encoding import sha384
        >>> sha384(b'')
        '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b'
        >>> sha384(b'this is a word')
        '37ae885a635d78e9067fdfe297e2d50d70de3670e4066bd541ac259b3ecdffb39a4c7b97211cb3967eac2188bb4b95f6'
    """
    return _hash_algorithm(hashlib.sha384, binary)


def sha512(binary: bytes) -> str:
    """
    Compute SHA512 hash of binary data.

    :param binary: Binary data to be hashed.
    :type binary: bytes
    :return: SHA512 digest string in hexadecimal format.
    :rtype: str

    Examples::
        >>> from hbutils.encoding import sha512
        >>> sha512(b'')
        'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
        >>> sha512(b'this is a word')
        '6e80a2fd5dcf382b443ddaa619833208a4f4ac9bbedb760d6c8aac26a12da8dc6e2f6bc809091915db2e2d19bb66682db89e46c646a8ea7a5c6da57bf1a42b5c'
    """
    return _hash_algorithm(hashlib.sha512, binary)


def sha3(binary: bytes, n: int = 256) -> str:
    """
    Compute SHA3 hash of binary data with configurable bit length.

    :param binary: Binary data to be hashed.
    :type binary: bytes
    :param n: Bit length of SHA3 hash. Valid values are 224, 256, 384, or 512. Default is 256.
    :type n: int
    :return: SHA3 digest string in hexadecimal format.
    :rtype: str

    Examples::
        >>> from hbutils.encoding import sha3
        >>> sha3(b'')
        'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a'
        >>> sha3(b'this is a word')
        '3e5a3507f625c8464fb282b451c8d82d78c3a232645e55c846d55551a7fe667c'
        >>> sha3(b'this is a word', n=224)
        'e0271d2734fc2c1a6dfcb6051bec6dc59e5f7fbec4b0d42ef1faee64'
    """
    return _hash_algorithm(getattr(hashlib, f'sha3_{n}'), binary)
