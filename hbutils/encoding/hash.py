import hashlib

__all__ = [
    'md5', 'sha1',
    'sha224', 'sha256', 'sha384', 'sha512',
    'sha3',
]


def _hash_algorithm(algo, binary: bytes):
    p = algo()
    p.update(binary)
    return p.hexdigest()
    pass


def md5(binary: bytes):
    return _hash_algorithm(hashlib.md5, binary)


def sha1(binary: bytes):
    return _hash_algorithm(hashlib.sha1, binary)


def sha224(binary: bytes):
    return _hash_algorithm(hashlib.sha224, binary)


def sha256(binary: bytes):
    return _hash_algorithm(hashlib.sha256, binary)


def sha384(binary: bytes):
    return _hash_algorithm(hashlib.sha384, binary)


def sha512(binary: bytes):
    return _hash_algorithm(hashlib.sha512, binary)


def sha3(binary: bytes, n: int = 256):
    return _hash_algorithm(getattr(hashlib, f'sha3_{n}'), binary)
