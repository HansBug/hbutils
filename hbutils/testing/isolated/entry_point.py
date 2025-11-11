"""
This module provides utilities for isolating and mocking entry points in Python packages.

It supports multiple entry point systems including pkg_resources, importlib.metadata,
and importlib_metadata (backport for Python 3.7). The main functionality allows for
creating isolated environments where entry points can be mocked or cleared for testing purposes.
"""

import inspect
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from itertools import chain
from typing import Iterator, Tuple, Any, Union, List, Dict
from unittest.mock import patch, MagicMock

from hbutils.reflection import quick_import_object, nested_with

__all__ = [
    'isolated_entry_points',
]


@dataclass
class _FakeEntryPoint:
    """
    A fake entry point class that mimics the behavior of real entry points.
    
    :param name: The name of the entry point.
    :type name: str
    :param group: The group name that this entry point belongs to.
    :type group: str
    :param dist: The distribution object or callable that this entry point represents.
    :type dist: object
    """
    name: str
    group: str
    dist: object

    def load(self):
        """
        Load and return the distribution object.
        
        :return: The distribution object.
        :rtype: object
        """
        return self.dist


_max_fake_id = 0


def _fake_id() -> int:
    """
    Generate a unique fake ID for unnamed entry points.
    
    :return: A unique integer ID.
    :rtype: int
    """
    global _max_fake_id
    _max_fake_id += 1
    return _max_fake_id


def _fake_entry_name() -> str:
    """
    Generate a unique fake entry point name.
    
    :return: A unique entry point name in the format 'unnamed_fake_entry_{id}'.
    :rtype: str
    """
    return f'unnamed_fake_entry_{_fake_id()}'


def _yield_from_units(fes, auto_import: bool = True) -> Iterator[Tuple[str, Any]]:
    """
    Yield name-distribution pairs from various input formats.
    
    This function processes different input formats (list, tuple, dict) and yields
    standardized (name, dist) tuples. It can automatically import objects from strings
    if auto_import is enabled.
    
    :param fes: Fake entry specifications in list, tuple, or dict format.
    :type fes: Union[list, tuple, dict]
    :param auto_import: Whether to automatically import objects from string paths.
    :type auto_import: bool
    
    :return: Iterator yielding (name, distribution) tuples.
    :rtype: Iterator[Tuple[str, Any]]
    :raises TypeError: If the input format is not recognized.
    
    Example::
        >>> list(_yield_from_units([('name', object), 'module.func']))
        [('name', <object>), ('func', <function>)]
    """
    if isinstance(fes, (list, tuple)):
        for item in fes:
            if isinstance(item, tuple) and len(item) == 2:
                name, dist = item
                if auto_import and isinstance(dist, str):
                    dist, _, _ = quick_import_object(dist)
            elif auto_import and isinstance(item, str):
                dist, _, name = quick_import_object(item)
            elif hasattr(item, '__name__'):
                name, dist = item.__name__, item
            else:
                name, dist = _fake_entry_name(), item

            yield name, dist

    elif isinstance(fes, dict):
        for name, dist in fes.items():
            if auto_import and isinstance(dist, str):
                dist, _, _ = quick_import_object(dist)

            yield name, dist

    else:
        raise TypeError(f'Unknown type of fake entries - {fes!r}.')  # pragma: no cover


def _yield_fake_entries(group, fes, auto_import: bool = True) -> Iterator[_FakeEntryPoint]:
    """
    Yield fake entry point objects for a specific group.
    
    :param group: The group name for the entry points.
    :type group: str
    :param fes: Fake entry specifications.
    :type fes: Union[list, tuple, dict]
    :param auto_import: Whether to automatically import objects from string paths.
    :type auto_import: bool
    
    :return: Iterator yielding _FakeEntryPoint objects.
    :rtype: Iterator[_FakeEntryPoint]
    """
    for name, dist in _yield_from_units(fes, auto_import):
        yield _FakeEntryPoint(name, group, dist)


@contextmanager
def isolated_entry_points(group: str, fakes: Union[List, Dict[str, Any], None] = None,
                          auto_import: bool = True, clear: bool = False):
    """
    Isolation context manager for entry points functions.
    
    This context manager allows for mocking or clearing entry points during testing.
    It supports pkg_resources.iter_entry_points, importlib.metadata.entry_points,
    and importlib_metadata.entry_points.
    
    :param group: The entry point group name to isolate.
    :type group: str
    :param fakes: Fake entry points to inject. Can be a list, tuple, or dict.
                  List/tuple format: [(name, dist), object, 'import.path', ...]
                  Dict format: {name: dist, name: 'import.path', ...}
    :type fakes: Union[List, Dict[str, Any], None]
    :param auto_import: Auto import objects from string paths. Default is ``True``.
    :type auto_import: bool
    :param clear: Clear original entry points if ``True``. Default is ``False``.
    :type clear: bool
    
    :raises TypeError: If fakes parameter is not of type list, tuple, dict, or None.
    
    Example::
        >>> from hbutils.testing import isolated_entry_points
        >>> 
        >>> # Mock plugins with a list
        >>> with isolated_entry_points('my_plugin', [
        ...     ('quick_import_object', 'hbutils.reflection.quick_import_object'),
        ...     ('func_filter', filter),
        ...     map,
        ...     'hbutils.system.is_binary_file',
        ... ]):
        ...     # Entry points are mocked within this context
        ...     pass
        >>> 
        >>> # Mock plugins with a dict
        >>> with isolated_entry_points('my_plugin', {
        ...     'func_map': map,
        ...     'func_binary': 'hbutils.system.is_binary_file'
        ... }):
        ...     # Entry points are mocked within this context
        ...     pass
        >>> 
        >>> # Clear all entry points for a group
        >>> with isolated_entry_points('my_plugin', clear=True):
        ...     # No entry points available in this context
        ...     pass
    
    .. warning::
        The ``pkg_resources`` package is no longer officially supported.
        However, certain libraries that rely on hbutils are still in use,
        hence temporary support will be provided. The official guidance must be followed to
        migrate to ``importlib.metadata`` at the earliest opportunity.
        In addition, support for the ``pkg_resources`` package in this function will be
        discontinued in the next major version.
    """
    if fakes is not None and not isinstance(fakes, (list, tuple, dict)):
        raise TypeError(f'Unknown entry point type - {fakes!r}.')

    from pkg_resources import iter_entry_points as _origin_iep
    group_name = group

    # noinspection PyShadowingNames
    @wraps(_origin_iep)
    def _new_iter_func(group, name=None):
        """
        Replacement function for pkg_resources.iter_entry_points.
        
        :param group: The entry point group to query.
        :type group: str
        :param name: Optional specific entry point name to filter.
        :type name: str or None
        
        :return: Iterator of entry points.
        :rtype: Iterator
        """
        _exist_names = set()

        def _check_name(x) -> bool:
            """
            Check if an entry point should be included based on name filtering.
            
            :param x: The entry point to check.
            :type x: _FakeEntryPoint or EntryPoint
            
            :return: True if the entry point should be included.
            :rtype: bool
            """
            if (name is None or x.name == name) and x.name not in _exist_names:
                _exist_names.add(x.name)
                return True
            else:
                return False

        if group == group_name:
            mocked = _yield_fake_entries(group_name, fakes or [], auto_import)
            if not clear:
                mocked = chain(mocked, _origin_iep(group, name))
            yield from filter(_check_name, mocked)
        else:
            yield from _origin_iep(group, name)

    try:
        import importlib_metadata as _py37_metadata
    except (ModuleNotFoundError, ImportError):
        _py37_metadata = None
    else:
        _py37_origin_entry_points = _py37_metadata.entry_points

        @wraps(_py37_origin_entry_points)
        def _py37_entry_points(**kwargs):
            """
            Replacement function for importlib_metadata.entry_points (Python 3.7 backport).
            
            :param kwargs: Keyword arguments for filtering entry points (group, name, etc.).
            :type kwargs: dict
            
            :return: List of entry points matching the criteria.
            :rtype: list
            """
            kwargs = {key: value for key, value in kwargs.items() if value}
            group_ = kwargs.get('group', None)
            name = kwargs.get('name', None)
            _exist_names = set()

            def _check_name(x) -> bool:
                """
                Check if an entry point should be included based on filtering criteria.
                
                :param x: The entry point to check.
                :type x: _FakeEntryPoint or EntryPoint
                
                :return: True if the entry point should be included.
                :rtype: bool
                """
                if ((isinstance(x, _py37_metadata.EntryPoint) and x.matches(**kwargs)) or
                    (not isinstance(x, _py37_metadata.EntryPoint) and (name is None or x.name == name))) and \
                        x.name not in _exist_names:
                    _exist_names.add(x.name)
                    return True
                else:
                    return False

            if group_ is None or group_ == group_name:
                mocked = _yield_fake_entries(group_name, fakes or [], auto_import)
                if not clear:
                    mocked = chain(mocked, _py37_origin_entry_points(**kwargs))
                # noinspection PyTypeChecker
                return list(filter(_check_name, mocked))
            else:
                return list(_py37_origin_entry_points(**kwargs))

    try:
        import importlib.metadata as _py38_metadata
    except (ModuleNotFoundError, ImportError):
        _py38_metadata = None
    else:
        _py38_origin_entry_points = _py38_metadata.entry_points
        _py38_func_has_params = bool(inspect.signature(_py38_metadata.entry_points).parameters)

        @wraps(_py38_origin_entry_points)
        def _py38_entry_points(**kwargs):
            """
            Replacement function for importlib.metadata.entry_points (Python 3.8+).
            
            :param kwargs: Keyword arguments for filtering entry points (group, name, etc.).
            :type kwargs: dict
            
            :return: Dict or list of entry points depending on Python version.
            :rtype: Union[dict, list]
            """
            kwargs = {key: value for key, value in kwargs.items() if value}
            group_ = kwargs.get('group', None)
            name = kwargs.get('name', None)
            _exist_names = set()

            def _check_name(x) -> bool:
                """
                Check if an entry point should be included based on filtering criteria.
                
                :param x: The entry point to check.
                :type x: _FakeEntryPoint or EntryPoint
                
                :return: True if the entry point should be included.
                :rtype: bool
                """
                if ((isinstance(x, _py38_metadata.EntryPoint) and x.matches(**kwargs)) or
                    (not isinstance(x, _py38_metadata.EntryPoint) and (name is None or x.name == name))) and \
                        x.name not in _exist_names:
                    _exist_names.add(x.name)
                    return True
                else:
                    return False

            # noinspection PyArgumentList
            _base_result = _py38_origin_entry_points(**kwargs)
            if isinstance(_base_result, dict):  # kwargs must be empty
                _retval = _base_result.copy()
                mocked = _yield_fake_entries(group_name, fakes or [], auto_import)
                if not clear:
                    mocked = chain(mocked, (_retval.get(group_name, None) or []))

                # noinspection PyTypeChecker
                _retval[group_name] = (list if _py38_func_has_params else tuple)(filter(_check_name, mocked))
                return _retval
            else:
                if group_ is None or group_ == group_name:
                    mocked = _yield_fake_entries(group_name, fakes or [], auto_import)
                    if not clear:
                        mocked = chain(mocked, _base_result)

                    # noinspection PyTypeChecker
                    return list(filter(_check_name, mocked))
                else:

                    return _base_result

    mocks = []
    mocks.append(patch('pkg_resources.iter_entry_points', MagicMock(side_effect=_new_iter_func)))
    if _py37_metadata:
        mocks.append(patch('importlib_metadata.entry_points', MagicMock(side_effect=_py37_entry_points)))
    if _py38_metadata:
        mocks.append(patch('importlib.metadata.entry_points', MagicMock(side_effect=_py38_entry_points)))

    with nested_with(*mocks):
        yield
