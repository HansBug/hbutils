import inspect

import pkg_resources
import pytest

from hbutils.reflection import quick_import_object
from hbutils.system import is_binary_file
from hbutils.testing import isolated_entry_points

try:
    import importlib_metadata as _py37_metadata
except (ModuleNotFoundError, ImportError):
    _py37_metadata = None

try:
    import importlib.metadata as _py38_metadata
except (ModuleNotFoundError, ImportError):
    _py38_metadata = None
    _py38_func_has_params = False
else:
    _py38_func_has_params = bool(inspect.signature(_py38_metadata.entry_points).parameters)


def _test_for_all(group, name=None, expected=None):
    assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points(group, name)} == expected

    _metadata_kwargs = {'group': group}
    if name:
        _metadata_kwargs['name'] = name
    if _py37_metadata:
        assert {entry.name: entry.load() for entry in _py37_metadata.entry_points(**_metadata_kwargs)} == expected
    if _py38_metadata:
        if _py38_func_has_params:
            assert {entry.name: entry.load() for entry in _py38_metadata.entry_points(**_metadata_kwargs)} == expected
        else:
            assert {
                       entry.name: entry.load()
                       for _, entries in _py38_metadata.entry_points().items()
                       for entry in entries
                       if (group is None or entry.group == group) and (name is None or entry.name == name)
                   } == expected


def _test_for_unnamed_set(group, name=None, expected=None):
    assert {entry.load() for entry in pkg_resources.iter_entry_points(group, name)} == expected
    _metadata_kwargs = {'group': group}
    if name:
        _metadata_kwargs['name'] = name
    if _py37_metadata:
        assert {entry.load() for entry in _py37_metadata.entry_points(**_metadata_kwargs)} == expected
    if _py38_metadata:
        if _py38_func_has_params:
            assert {entry.load() for entry in _py38_metadata.entry_points(**_metadata_kwargs)} == expected
        else:
            assert {
                       entry.load()
                       for _, entries in _py38_metadata.entry_points().items()
                       for entry in entries
                       if (group is None or entry.group == group) and (name is None or entry.name == name)
                   } == expected


@pytest.mark.unittest
class TestTestingIsolatedEntryPoint:
    def test_isolated_entry_points(self):
        with isolated_entry_points('my_plugin', [
            ('quick_import_object', 'hbutils.reflection.quick_import_object'),
            ('func_filter', filter),
            map,
            'hbutils.system.is_binary_file',
        ]):
            _test_for_all('my_plugin', None, {
                'quick_import_object': quick_import_object,
                'func_filter': filter,
                'map': map,
                'is_binary_file': is_binary_file,
            })

    def test_isolated_entry_points_dict(self):
        with isolated_entry_points('my_plugin', {
            'quick_import_object': 'hbutils.reflection.quick_import_object',
            'func_filter': filter,
            'func_map': map,
            'system.is_binary_file': 'hbutils.system.is_binary_file'
        }):
            _test_for_all('my_plugin', None, {
                'quick_import_object': quick_import_object,
                'func_filter': filter,
                'func_map': map,
                'system.is_binary_file': is_binary_file,
            })

    def test_isolated_entry_points_nested(self):
        with isolated_entry_points('my_plugin', [
            ('quick_import_object', 'hbutils.reflection.quick_import_object'),
        ]):
            _test_for_all('my_plugin', None, {
                'quick_import_object': quick_import_object,
            })

            with isolated_entry_points('my_plugin', {'func_filter': filter}):
                _test_for_all('my_plugin', None, {
                    'quick_import_object': quick_import_object,
                    'func_filter': filter,
                })

                with isolated_entry_points('my_plugin', {
                    'func_map': map,
                    'system.is_binary_file': 'hbutils.system.is_binary_file'
                }):
                    _test_for_all('my_plugin', None, {
                        'quick_import_object': quick_import_object,
                        'func_filter': filter,
                        'func_map': map,
                        'system.is_binary_file': is_binary_file,
                    })
                    _test_for_all('my_plugin', 'func_map', {'func_map': map})

                with isolated_entry_points('my_plugin', {
                    'func_map': map,
                    'system.is_binary_file': 'hbutils.system.is_binary_file'
                }, clear=True):
                    _test_for_all('my_plugin', None, {
                        'func_map': map,
                        'system.is_binary_file': is_binary_file,
                    })

                with isolated_entry_points('my_plugin', {
                    'func_filter': map,
                    'system.is_binary_file': 'hbutils.system.is_binary_file'
                }):
                    _test_for_all('my_plugin', None, {
                        'quick_import_object': quick_import_object,
                        'func_filter': map,
                        'system.is_binary_file': is_binary_file,
                    })

    def test_isolated_entry_points_unnamed(self):
        with isolated_entry_points('my_pluginx', [
            1, 2, 3,
        ]):
            _test_for_unnamed_set('my_pluginx', None, {1, 2, 3})

            with isolated_entry_points('my_plugin', [
                ('quick_import_object', 'hbutils.reflection.quick_import_object'),
            ]):
                _test_for_all('my_plugin', None, {
                    'quick_import_object': quick_import_object,
                })
                _test_for_unnamed_set('my_pluginx', None, {1, 2, 3})

                with isolated_entry_points('my_pluginx', clear=True):
                    _test_for_all('my_plugin', None, {
                        'quick_import_object': quick_import_object,
                    })
                    _test_for_unnamed_set('my_pluginx', None, set())

    def test_isolated_entry_points_invalid_type(self):
        with pytest.raises(TypeError):
            with isolated_entry_points('my_pluginx', 233):
                pytest.fail('Should not reach here!')
