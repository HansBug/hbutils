"""
Utilities for capturing program exit behavior and output streams in tests.

This module provides a convenient namespace that re-exports capture utilities
implemented in the :mod:`hbutils.testing.capture.exit` and
:mod:`hbutils.testing.capture.output` submodules. These tools are typically
used in unit tests to intercept system exits or capture stdout/stderr streams
without affecting the surrounding test environment.

The module exposes the public APIs from its submodules, including:

* :mod:`hbutils.testing.capture.exit` - Utilities for capturing and testing
  system exit behavior.
* :mod:`hbutils.testing.capture.output` - Utilities for capturing stdout/stderr
  output streams.

Example::

    >>> from hbutils.testing.capture import capture_exit, capture_output  # doctest: +SKIP
    >>> # Use capture_exit in a test to intercept sys.exit()
    >>> # Use capture_output in a test to capture printed output

.. note::
   The exact functions and classes provided by this module depend on the
   public API of the re-exported submodules.

"""
from .exit import *
from .output import *
