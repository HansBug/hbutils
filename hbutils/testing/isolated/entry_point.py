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
    name: str
    group: str
    dist: object

    def load(self):
        return self.dist


_max_fake_id = 0


def _fake_id() -> int:
    global _max_fake_id
    _max_fake_id += 1
    return _max_fake_id


def _fake_entry_name() -> str:
    return f'unnamed_fake_entry_{_fake_id()}'


def _yield_from_units(fes, auto_import: bool = True) -> Iterator[Tuple[str, Any]]:
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
    for name, dist in _yield_from_units(fes, auto_import):
        yield _FakeEntryPoint(name, group, dist)


@contextmanager
def isolated_entry_points(group: str, fakes: Union[List, Dict[str, Any], None] = None,
                          auto_import: bool = True, clear: bool = False):
    """
    Overview:
        Isolation for :func:`pkg_resources.iter_entry_points` function.
        Can be used to fake the plugins, or just disable the installed plugins.

        ``importlib.metadata`` and ``importlib_metadata`` are supported now.

    :param group: Group name.
    :param fakes: Fake entry points. Dict or list are accepted.
    :param auto_import: Auto import the object from string. Default is ``True`` which means if \
        a string is given, dynamic import will be performed.
    :param clear: Clear the original entry points or not. Default is ``False`` which means the original \
        entry points will be kept and be able to be iterated.

    Examples::
        >>> import importlib.metadata
        >>> import importlib_metadata  # backport for py3.7
        >>> import pkg_resources  # deprecated
        >>>
        >>> from hbutils.testing import isolated_entry_points
        >>>
        >>> # nothing at the beginning
        >>> print({ep.name: ep.load() for ep in
        ...        pkg_resources.iter_entry_points('my_plugin')})
        {}
        >>> print(importlib.metadata.entry_points().get('my_plugin', None))
        None
        >>> print(importlib_metadata.entry_points(group='my_plugin'))
        ()
        >>>
        >>> # mock the plugins
        >>> with isolated_entry_points('my_plugin', [
        ...     (
        ...             'quick_import_object',  # name import
        ...             'hbutils.reflection.quick_import_object'
        ...     ),
        ...     ('func_filter', filter),  # named entry object
        ...     map,  # simple function
        ...     'hbutils.system.is_binary_file',  # simple import
        ... ]):
        ...     print({ep.name: ep.load() for ep in
        ...            pkg_resources.iter_entry_points('my_plugin')})
        ...     print(importlib.metadata.entry_points()['my_plugin'])
        ...     print(importlib_metadata.entry_points(group='my_plugin'))
        ...
        {'quick_import_object': <function quick_import_object at 0x7f6d0dd5ad40>, 'func_filter': <class 'filter'>, 'map': <class 'map'>, 'is_binary_file': <function is_binary_file at 0x7f6d0dcd8550>}
        [_FakeEntryPoint(name='quick_import_object', group='my_plugin', dist=<function quick_import_object at 0x7f6d0dd5ad40>), _FakeEntryPoint(name='func_filter', group='my_plugin', dist=<class 'filter'>), _Fak
        eEntryPoint(name='map', group='my_plugin', dist=<class 'map'>), _FakeEntryPoint(name='is_binary_file', group='my_plugin', dist=<function is_binary_file at 0x7f6d0dcd8550>)]
        [_FakeEntryPoint(name='quick_import_object', group='my_plugin', dist=<function quick_import_object at 0x7f6d0dd5ad40>), _FakeEntryPoint(name='func_filter', group='my_plugin', dist=<class 'filter'>), _Fak
        eEntryPoint(name='map', group='my_plugin', dist=<class 'map'>), _FakeEntryPoint(name='is_binary_file', group='my_plugin', dist=<function is_binary_file at 0x7f6d0dcd8550>)]
        >>> with isolated_entry_points('my_plugin', {
        ...     'func_map': map,
        ...     'func_binary': 'hbutils.system.is_binary_file'
        ... }):
        ...     print({ep.name: ep.load() for ep in
        ...            pkg_resources.iter_entry_points('my_plugin')})
        ...     print(importlib.metadata.entry_points()['my_plugin'])
        ...     print(importlib_metadata.entry_points(group='my_plugin'))
        ...
        {'func_map': <class 'map'>, 'func_binary': <function is_binary_file at 0x7f6d0dcd8550>}
        [_FakeEntryPoint(name='func_map', group='my_plugin', dist=<class 'map'>), _FakeEntryPoint(name='func_binary', group='my_plugin', dist=<function is_binary_file at 0x7f6d0dcd8550>)]
        [_FakeEntryPoint(name='func_map', group='my_plugin', dist=<class 'map'>), _FakeEntryPoint(name='func_binary', group='my_plugin', dist=<function is_binary_file at 0x7f6d0dcd8550>)]
        >>> # nothing at the ending
        >>> print({ep.name: ep.load() for ep in
        ...        pkg_resources.iter_entry_points('my_plugin')})
        {}
        >>> print(importlib.metadata.entry_points().get('my_plugin', None))
        None
        >>> print(importlib_metadata.entry_points(group='my_plugin'))
        ()

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
        _exist_names = set()

        def _check_name(x) -> bool:
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
            kwargs = {key: value for key, value in kwargs.items() if value}
            group_ = kwargs.get('group', None)
            name = kwargs.get('name', None)
            _exist_names = set()

            def _check_name(x) -> bool:
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
            kwargs = {key: value for key, value in kwargs.items() if value}
            group_ = kwargs.get('group', None)
            name = kwargs.get('name', None)
            _exist_names = set()

            def _check_name(x) -> bool:
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
