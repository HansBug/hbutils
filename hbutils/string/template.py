"""
Overview:
    Useful utilities for template a string.
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
    Overview:
        Mapping all the environment values (not system environment variables) into a template string.

    Arguments:
        - template (:obj:`str`): Template string.
        - environ (:obj:`Optional[Mapping[str, str]]`): Environment values, should be a mapping.
        - safe (:obj:`bool`): Safe substitute, default is ``False`` which means \
            all the value used in template should be able to found in the given ``environ``.
        - default (:obj:`Any`): Default value when no variable provided. Default is ``_NO_DEFAULT_VALUE``, which \
            means ``KeyError`` will be raised.

    Returns:
        - result (:obj:`str`): Substituted string.

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
        def __getitem__(self, item):
            return dict.get(self, item, default)

    _template = Template(template)
    env = environ or {}
    if default is not _NO_DEFAULT_VALUE:
        env = _DefaultDict(env)

    _func = _template.safe_substitute if safe else _template.substitute
    # noinspection PyArgumentList
    return _func(env)
