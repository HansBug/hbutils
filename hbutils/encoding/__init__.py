"""
Encoding utilities for ANSI formatting, base64, decoding, and hashing.

This package-level module aggregates a collection of encoding/decoding helpers
from submodules under :mod:`hbutils.encoding`. It re-exports their public APIs
for convenient access, covering the following areas:

* ANSI escape code handling for terminal styling (:mod:`hbutils.encoding.ansi`)
* Base64 encoding and decoding (:mod:`hbutils.encoding.base64`)
* Automatic decoding helpers (:mod:`hbutils.encoding.decode`)
* Cryptographic hash wrappers (:mod:`hbutils.encoding.hash`)
* Non-cryptographic integer hash algorithms (:mod:`hbutils.encoding.int_hash`)
* Hash validation utilities (:mod:`hbutils.encoding.int_hash_val`)

The module itself does not define functions or classes directly. Instead, it
acts as a unified import surface for the encoding toolkit.

Example::

    >>> from hbutils.encoding import md5, sha256
    >>> md5(b'hello world')
    '5eb63bbbe01eeed093cb22bb8f5acdc3'
    >>> sha256(b'hello world')
    'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'

    >>> from hbutils.encoding import int_hash
    >>> int_hash("hello", method='FNV-1a-32')
    1335831723

.. note::
   All public names from the listed submodules are re-exported. Refer to the
   respective submodule documentation for detailed usage and parameter
   descriptions.

"""
from .ansi import *
from .base64 import *
from .decode import *
from .hash import *
from .int_hash import *
from .int_hash_val import *
