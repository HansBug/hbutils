"""
Testing utilities package entry point.

This module serves as the public entry point for the :mod:`hbutils.testing`
package. It re-exports common testing utilities from its submodules to provide
a convenient, flat import surface for unit test authors. The utilities cover
output capturing, flexible text comparisons, parameterized test generation,
isolated execution environments, requirement checks, and CLI simulation.

The module provides access to functionality from these submodules:

* :mod:`hbutils.testing.capture` - Capture stdout/stderr and exit behavior
* :mod:`hbutils.testing.compare` - Text and structured comparison helpers
* :mod:`hbutils.testing.generator` - Test case generation utilities
* :mod:`hbutils.testing.isolated` - Isolated directories and environment helpers
* :mod:`hbutils.testing.requires` - Requirement checks for external tools
* :mod:`hbutils.testing.simulate` - CLI and entry-point simulation

.. note::
   This module only re-exports public utilities. Refer to individual submodules
   for detailed behavior and additional helpers.

Example::

    >>> from hbutils.testing import capture_output, TextAligner, isolated_directory
    >>> with capture_output() as (stdout, stderr):
    ...     print("test output")
    >>> stdout.getvalue()
    'test output\\n'
"""
from .capture import *
from .compare import *
from .generator import *
from .isolated import *
from .requires import *
from .simulate import *
