"""
String template utilities with environment-like substitution.

This module provides utilities to perform string templating using a mapping
of values that behave similarly to environment variables. It supports both
strict and safe substitution modes and allows supplying a default value for
missing keys.

The module exposes the following public API:

* :func:`env_template` - Apply template substitution using a mapping

.. note::
   This module does not read from system environment variables. The mapping
   must be provided explicitly.

Example::

    >>> from hbutils.string.template import env_template
    >>> env_template('${A} + 1 = ${B}', {'A': '1', 'B': '2'})
    '1 + 1 = 2'
    >>> env_template('${A} + 1 = ${B}', {'A': '1'}, safe=True)
    '1 + 1 = ${B}'
    >>> env_template('${A} + 1 = ${B}', {'A': '1'}, default='')
    '1 + 1 = '

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
    Map values from a provided mapping into a template string.

    This function substitutes variables in a template string with values from
    ``environ``. It supports strict substitution (raising on missing keys) and
    safe substitution (leaving missing keys unchanged). A default value may be
    provided to substitute for missing keys even in strict mode.

    :param template: Template string containing variables in ``${VAR}`` format.
    :type template: str
    :param environ: Mapping for variable substitution. If ``None``, an empty
        mapping is used.
    :type environ: Optional[Mapping[str, Any]]
    :param safe: Whether to use safe substitution. If ``True``, missing
        variables are left as-is. If ``False``, missing variables raise
        :class:`KeyError` unless a default is provided. Defaults to ``False``.
    :type safe: bool
    :param default: Default value to use when a variable is not found in
        ``environ``. If set to ``_NO_DEFAULT_VALUE`` (the default), missing
        variables raise :class:`KeyError` when ``safe`` is ``False``.
    :type default: Any

    :return: Substituted string with variables replaced by their values.
    :rtype: str
    :raises KeyError: If a variable is not found in ``environ`` and ``safe``
        is ``False`` and no default is provided.

    Example::

        >>> from hbutils.string.template import env_template
        >>> env_template('${A} + 1 = ${B}', {'A': '1', 'B': '2'})
        '1 + 1 = 2'
        >>> env_template('${A} + 1 = ${B}', {'A': '1'})
        Traceback (most recent call last):
            ...
        KeyError: 'B'
        >>> env_template('${A} + 1 = ${B}', {'A': '1'}, safe=True)
        '1 + 1 = ${B}'
        >>> env_template('${A} + 1 = ${B}', {'A': '1'}, default='')
        '1 + 1 = '

    """

    class _DefaultDict(dict):
        """
        Internal dictionary class that returns a default value for missing keys.

        This class extends :class:`dict` to provide a fixed default value when
        a key is not found. It is used internally to emulate environment-like
        default values during template substitution.
        """

        def __getitem__(self, item: Any) -> Any:
            """
            Get a value for the key, returning the default when missing.

            :param item: The key to look up in the dictionary.
            :type item: Any
            :return: The value for the key, or the provided default when the key
                is not present.
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
