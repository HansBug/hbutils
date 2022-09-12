import pkg_resources
import pytest

from hbutils.reflection import quick_import_object
from hbutils.system import is_binary_file
from hbutils.testing import isolated_entry_points


@pytest.mark.unittest
class TestTestingIsolatedEntryPoint:
    def test_isolated_entry_points(self):
        with isolated_entry_points('my_plugin', [
            ('quick_import_object', 'hbutils.reflection.quick_import_object'),
            ('func_filter', filter),
            map,
            'hbutils.system.is_binary_file',
        ]):
            assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                'quick_import_object': quick_import_object,
                'func_filter': filter,
                'map': map,
                'is_binary_file': is_binary_file,
            }

    def test_isolated_entry_points_dict(self):
        with isolated_entry_points('my_plugin', {
            'quick_import_object': 'hbutils.reflection.quick_import_object',
            'func_filter': filter,
            'func_map': map,
            'system.is_binary_file': 'hbutils.system.is_binary_file'
        }):
            assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                'quick_import_object': quick_import_object,
                'func_filter': filter,
                'func_map': map,
                'system.is_binary_file': is_binary_file,
            }

    def test_isolated_entry_points_nested(self):
        with isolated_entry_points('my_plugin', [
            ('quick_import_object', 'hbutils.reflection.quick_import_object'),
        ]):
            assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                'quick_import_object': quick_import_object,
            }

            with isolated_entry_points('my_plugin', {'func_filter': filter}):
                assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                    'quick_import_object': quick_import_object,
                    'func_filter': filter,
                }

                with isolated_entry_points('my_plugin', {
                    'func_map': map,
                    'system.is_binary_file': 'hbutils.system.is_binary_file'
                }):
                    assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                        'quick_import_object': quick_import_object,
                        'func_filter': filter,
                        'func_map': map,
                        'system.is_binary_file': is_binary_file,
                    }
                    assert {entry.name: entry.load() for entry in
                            pkg_resources.iter_entry_points('my_plugin', 'func_map')} == {'func_map': map}

                with isolated_entry_points('my_plugin', {
                    'func_map': map,
                    'system.is_binary_file': 'hbutils.system.is_binary_file'
                }, clear=True):
                    assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                        'func_map': map,
                        'system.is_binary_file': is_binary_file,
                    }

                with isolated_entry_points('my_plugin', {
                    'func_filter': map,
                    'system.is_binary_file': 'hbutils.system.is_binary_file'
                }):
                    assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                        'quick_import_object': quick_import_object,
                        'func_filter': map,
                        'system.is_binary_file': is_binary_file,
                    }

    def test_isolated_entry_points_unnamed(self):
        with isolated_entry_points('my_pluginx', [
            1, 2, 3,
        ]):
            assert {entry.load() for entry in pkg_resources.iter_entry_points('my_pluginx')} == {1, 2, 3}

            with isolated_entry_points('my_plugin', [
                ('quick_import_object', 'hbutils.reflection.quick_import_object'),
            ]):
                assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                    'quick_import_object': quick_import_object,
                }
                assert {entry.load() for entry in pkg_resources.iter_entry_points('my_pluginx')} == {1, 2, 3}

                with isolated_entry_points('my_pluginx', clear=True):
                    assert {entry.name: entry.load() for entry in pkg_resources.iter_entry_points('my_plugin')} == {
                        'quick_import_object': quick_import_object,
                    }
                    assert {entry.load() for entry in pkg_resources.iter_entry_points('my_pluginx')} == set()

    def test_isolated_entry_points_invalid_type(self):
        with pytest.raises(TypeError):
            with isolated_entry_points('my_pluginx', 233):
                pytest.fail('Should not reach here!')
