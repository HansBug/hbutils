"""
Dynamic import utilities for runtime object resolution.

This module provides helper functions to dynamically import Python modules,
objects, and nested attributes by name or by patterns. It is designed for
runtime resolution scenarios such as CLI plugins, configuration-based object
construction, or exploratory tooling where import targets are not known
ahead of time.

The module contains the following public components:

* :func:`import_object` - Import a single object from a specified module.
* :func:`quick_import_object` - Resolve an object from a dotted name and return
  the resolved module/name pair.
* :func:`iter_import_objects` - Iterate over all objects matching a dotted
  name pattern with wildcard support.

.. note::
   Pattern-based imports rely on attribute traversal and may access a large
   number of attributes when wildcard matching is used.

Example::

    >>> from hbutils.reflection.imports import import_object, quick_import_object
    >>> import_object('zip')  # Builtin function
    <class 'zip'>
    >>> quick_import_object('json.loads')[0]  # Resolve from a dotted name
    <function loads at ...>
"""
import builtins
import fnmatch
import importlib
from itertools import islice
from queue import Queue
from types import ModuleType
from typing import Optional, Callable, Any, Tuple, Iterator

from .func import dynamic_call

__all__ = [
    'import_object',
    'quick_import_object',
    'iter_import_objects',
]


def _import_module(module_name: Optional[str] = None) -> ModuleType:
    """
    Import a module by name or return the builtins module.

    :param module_name: Name of the module to import. If ``None``, returns the
        :mod:`builtins` module.
    :type module_name: Optional[str]
    :return: The imported module or the :mod:`builtins` module.
    :rtype: types.ModuleType
    :raises ModuleNotFoundError: If ``module_name`` is provided but cannot be found.

    Example::

        >>> _import_module('os')  # Returns os module
        >>> _import_module(None)  # Returns builtins module
    """
    if module_name:
        return importlib.import_module(module_name)
    else:
        return builtins


def import_object(obj_name: str, module_name: Optional[str] = None) -> Any:
    """
    Dynamically import an object from a module.

    This function imports a specific object (class, function, variable, etc.)
    from a given module. If no module name is provided, it searches in the
    :mod:`builtins` module.

    :param obj_name: Name of the object to import.
    :type obj_name: str
    :param module_name: Name of the module containing the object.
        Defaults to ``None``, which means the :mod:`builtins` module.
    :type module_name: Optional[str]
    :return: The imported object.
    :rtype: Any
    :raises AttributeError: If the object does not exist in the module.
    :raises ModuleNotFoundError: If the module cannot be found.

    Example::

        >>> import_object('zip')               # <class 'zip'>
        >>> import_object('ndarray', 'numpy')  # <class 'numpy.ndarray'>
    """
    return getattr(_import_module(module_name), obj_name)


def quick_import_object(full_name: str, predicate: Optional[Callable] = None) -> Tuple[Any, str, str]:
    """
    Quickly dynamically import an object with a single name.

    This function attempts to import an object using its full dotted name,
    supporting nested attributes. It returns the first matching object along
    with its module and object name.

    :param full_name: Full dotted name of the object, attribute access is
        supported.
    :type full_name: str
    :param predicate: Optional predicate function to filter results.
        The callable should accept ``(obj, module_name, obj_name)`` and return
        ``True`` or ``False``. Defaults to ``None``, which means no filtering.
    :type predicate: Optional[Callable[[Any, str, str], bool]]
    :return: A tuple containing ``(imported_object, module_name, object_name)``.
    :rtype: Tuple[Any, str, str]
    :raises ImportError: If the object cannot be imported.

    Example::

        >>> quick_import_object('zip')                     # (<class 'zip'>, '', 'zip')
        >>> quick_import_object('numpy.ndarray')           # (<class 'numpy.ndarray'>, 'numpy', 'ndarray')
        >>> quick_import_object('numpy.ndarray.__name__')  # ('ndarray', 'numpy', 'ndarray.__name__')
    """
    _iter = islice(iter_import_objects(full_name, predicate), 1)

    try:
        # noinspection PyTupleAssignmentBalance
        _obj, _module, _name = next(_iter)
        return _obj, _module, _name
    except (StopIteration, StopAsyncIteration):
        raise ImportError(f'Cannot import object {repr(full_name)}.')


def iter_import_objects(full_pattern: str, predicate: Optional[Callable] = None) \
        -> Iterator[Tuple[Any, str, str]]:
    """
    Dynamically import all objects matching a full name pattern.

    This function yields all objects that match the given pattern, supporting
    wildcards in attribute names. It performs a breadth-first search through
    module attributes to find all matching objects.

    :param full_pattern: Full pattern of the object with wildcard support.
        Supports :mod:`fnmatch`-style patterns (e.g., ``'numpy.array*'``).
    :type full_pattern: str
    :param predicate: Optional predicate function to filter results.
        The callable should accept ``(obj, module_name, obj_name)`` and return
        ``True`` or ``False``. Defaults to ``None``, which means no filtering.
    :type predicate: Optional[Callable[[Any, str, str], bool]]
    :return: Iterator yielding tuples of ``(imported_object, module_name,
        object_name)``.
    :rtype: Iterator[Tuple[Any, str, str]]

    Example::

        >>> list(iter_import_objects('os.path'))  # Yields all matching objects
        >>> list(iter_import_objects('numpy.array*'))  # Yields all numpy objects starting with 'array'
    """
    predicate = dynamic_call(predicate or (lambda: True))

    segments = full_pattern.split('.')
    length = len(segments)
    _errs = []
    for i in reversed(range(length + 1)):
        module_name = '.'.join(segments[:i])
        attrs = tuple(segments[i:])
        attrs_count = len(attrs)

        try:
            module = importlib.import_module(module_name or 'builtins')
        except (ModuleNotFoundError, ImportError):
            continue

        queue = Queue()
        queue.put((module, 0, ()))
        exist = False

        while not queue.empty():
            root, pos, ats = queue.get()

            if pos >= attrs_count:
                obj_name = '.'.join(ats)
                if predicate(root, module_name, obj_name):
                    yield root, module_name, obj_name
            elif hasattr(root, attrs[pos]):
                queue.put((getattr(root, attrs[pos]), pos + 1, ats + (attrs[pos],)))
                exist = True
            elif hasattr(root, '__dict__'):
                for key, value in sorted(root.__dict__.items()):
                    if fnmatch.fnmatch(key, attrs[pos]):
                        queue.put((value, pos + 1, ats + (key,)))
                        exist = True

        if exist:
            break
