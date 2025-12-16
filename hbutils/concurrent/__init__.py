"""
This module provides concurrent utilities for managing read-write locks.

The module exports read-write lock implementations that allow multiple concurrent readers
or a single exclusive writer. This is useful for scenarios with frequent read operations
and occasional write operations, enabling better performance through concurrent reads
while maintaining data consistency.

The lock follows these rules:
- Read-Read: Non-exclusive, allows concurrent access
- Read-Write: Exclusive, write operations wait for all read operations to complete
- Write-Write: Exclusive, write operations execute serially
- Write-Read: Exclusive, read operations wait for write operations to complete
"""

from .readwrite import *
