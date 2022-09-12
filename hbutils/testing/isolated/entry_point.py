from contextlib import contextmanager
from functools import wraps
from itertools import chain
from typing import Iterator, Tuple, Any, Union, List, Dict
from unittest.mock import patch, MagicMock

from hbutils.reflection import quick_import_object

__all__ = [
    'isolated_entry_points',
]


class _FakeEntryPoint:
    def __init__(self, name, dist):
        self.__name = name
        self.__dist = dist

    @property
    def name(self) -> str:
        return self.__name

    def load(self):
        return self.__dist


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


def _yield_fake_entries(fes, auto_import: bool = True) -> Iterator[_FakeEntryPoint]:
    for name, dist in _yield_from_units(fes, auto_import):
        yield _FakeEntryPoint(name, dist)


@contextmanager
def isolated_entry_points(group: str, fakes: Union[List, Dict[str, Any], None] = None,
                          auto_import: bool = True, clear: bool = False):
    """
    Overview:
        Isolation for :func:`pkg_resources.iter_entry_points` function.
        Can be used to fake the plugins, or just disable the installed plugins.

    :param group: Group name.
    :param fakes: Fake entry points. Dict or list are accepted.
    :param auto_import: Auto import the object from string. Default is ``True`` which means if \
        a string is given, dynamic import will be performed.
    :param clear: Clear the original entry points or not. Default is ``False`` which means the original \
        entry points will be kept and be able to be iterated.

    Examples::
        >>> import pkg_resources
        >>> from hbutils.testing import isolated_entry_points
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
        {'quick_import_object': <function quick_import_object at 0x7fb17f4e5170>, 'func_filter': <class 'filter'>, 'map': <class 'map'>, 'is_binary_file': <function is_binary_file at 0x7fb17f55eef0>}

        >>> with isolated_entry_points('my_plugin', {
        ...     'func_map': map, 'func_binary': 'hbutils.system.is_binary_file'}):
        ...     print({ep.name: ep.load() for ep in
        ...            pkg_resources.iter_entry_points('my_plugin')})
        {'func_map': <class 'map'>, 'func_binary': <function is_binary_file at 0x7fb17f55eef0>}
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
            mocked = _yield_fake_entries(fakes or [], auto_import)
            if not clear:
                mocked = chain(mocked, _origin_iep(group, name))
            yield from filter(_check_name, mocked)
        else:
            yield from _origin_iep(group, name)

    with patch('pkg_resources.iter_entry_points', MagicMock(side_effect=_new_iter_func)):
        yield
