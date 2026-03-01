"""
Binary data serialization and deserialization utilities.

This module provides a unified interface for binary serialization and
deserialization utilities implemented in the following submodules:

* :mod:`hbutils.binary.bool` - Boolean type serialization helpers
* :mod:`hbutils.binary.buffer` - Binary buffer read/write helpers
* :mod:`hbutils.binary.float` - Floating-point serialization helpers
* :mod:`hbutils.binary.int` - Signed integer serialization helpers
* :mod:`hbutils.binary.str` - String encoding and decoding helpers
* :mod:`hbutils.binary.uint` - Unsigned integer serialization helpers

All public interfaces from the submodules are re-exported, enabling
consumers to import the most common binary types and helpers directly
from :mod:`hbutils.binary`.

Example::

    >>> from hbutils.binary import CBoolType
    >>> import io
    >>> c_bool = CBoolType(1)
    >>> with io.BytesIO(b'\\x01\\x00') as file:
    ...     c_bool.read(file), c_bool.read(file)
    (True, False)

.. note::
   The actual public API depends on the contents of the imported submodules.
   Refer to each submodule's documentation for detailed usage and type-specific
   behaviors.

"""

from .bool import *
from .buffer import *
from .float import *
from .int import *
from .str import *
from .uint import *
