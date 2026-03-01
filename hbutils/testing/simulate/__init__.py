"""
Simulation utilities for specialized Python runtime behaviors.

This module provides helpers for simulating and testing special Python
behaviors in controlled environments. It primarily re-exports the public API
from :mod:`hbutils.testing.simulate.entry`, which contains utilities focused
on simulating CLI entry point execution and related runtime characteristics.

The module contains the following main components (re-exported):

* :class:`EntryRunResult` - Result container for simulated CLI entry execution.

.. note::
   This module is intended for testing usage. It re-exports utilities from
   :mod:`hbutils.testing.simulate.entry` to provide a convenient import path.

Example::

    >>> from hbutils.testing.simulate import EntryRunResult
    >>> result = EntryRunResult(0, "ok", "", None)
    >>> result.exitcode
    0
"""
from .entry import *
