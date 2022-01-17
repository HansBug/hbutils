"""
Overview:
    Useful utilities for template a string.
"""
from string import Template
from typing import Optional, Mapping

__all__ = ['env_template']


def env_template(template: str, environ: Optional[Mapping[str, str]] = None, safe: bool = False) -> str:
    """
    Overview:
        Mapping all the environment values (not system environment variables) into a template string.

    Arguments:
        - template (:obj:`str`): Template string.
        - environ (:obj:`Optional[Mapping[str, str]]`): Environment values, should be a mapping.
        - safe (:obj:`bool`): Safe substitute, default is ``False`` which means \
            all the value used in template should be able to found in the given ``environ``.

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
    """
    _template = Template(template)
    _func = _template.safe_substitute if safe else _template.substitute
    return _func(**(environ or {}))
