"""
Overview:
    Useful utilities for template a string.
    
This module provides functionality for string templating with environment variable substitution.
It allows flexible template string processing with configurable safety and default value handling.
"""
from string import Template
from typing import Optional, Mapping, Any

from ..design import SingletonMark

__all__ = [
    'env_template'
]

_NO_DEFAULT_VALUE = SingletonMark('_NO_DEFAULT_VALUE')


def env_template(template: str, environ: Optional[Mapping[str, Any]] = None,
                 safe: bool = False, default: Any = _NO_DEFAULT_VALUE) -> str:
    """
    Mapping all the environment values (not system environment variables) into a template string.
    
    This function substitutes variables in a template string with values from a provided mapping.
    It supports both strict and safe substitution modes, and allows setting default values for
    missing variables.

    :param template: Template string containing variables in ${VAR} format.
    :type template: str
    :param environ: Environment values mapping for variable substitution. If None, an empty dict is used.
    :type environ: Optional[Mapping[str, Any]]
    :param safe: If True, missing variables are left as-is in the template. If False, KeyError is raised
        for missing variables (unless default is provided). Default is False.
    :type safe: bool
    :param default: Default value to use when a variable is not found in environ. If set to _NO_DEFAULT_VALUE
        (the default), KeyError will be raised for missing variables in non-safe mode.
    :type default: Any
    
    :return: The substituted string with all variables replaced by their values.
    :rtype: str
    :raises KeyError: If a variable is not found in environ and safe is False and no default is provided.
    
    Examples::
        >>> from hbutils.string import env_template
        >>> env_template('${A} + 1 = ${B}', {'A': '1', 'B': '2'})
        '1 + 1 = 2'
        >>> env_template('${A} + 1 = ${B}', {'A': '1'})
        KeyError: 'B'
        >>> env_template('${A} + 1 = ${B}', {'A': '1'}, safe=True)
        '1 + 1 = ${B}'
        >>> env_template('${A} + 1 = ${B}', {'A': '1'}, default='')  # like environment variable
        '1 + 1 = '
    """

    class _DefaultDict(dict):
        """
        Internal dictionary class that returns a default value for missing keys.
        
        This class extends dict to provide default value functionality when a key
        is not found, similar to collections.defaultdict but with a fixed default value.
        """

        def __getitem__(self, item):
            """
            Get an item from the dictionary, returning the default value if not found.
            
            :param item: The key to look up in the dictionary.
            :type item: Any
            
            :return: The value associated with the key, or the default value if key is not found.
            :rtype: Any
            """
            return dict.get(self, item, default)

    _template = Template(template)
    env = environ or {}
    if default is not _NO_DEFAULT_VALUE:
        env = _DefaultDict(env)

    _func = _template.safe_substitute if safe else _template.substitute
    # noinspection PyArgumentList
    return _func(env)
