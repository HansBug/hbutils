"""
Overview:
    Useful utilities for ordinal words, such as ``1st``, ``2nd``, etc.
"""
from functools import lru_cache

__all__ = [
    'ordinal', 'ordinalize',
]


@lru_cache()
def _get_inflection():
    try:
        import inflection
    except ImportError:
        from ..system import pip_install
        pip_install(['inflection>=0.5'], silent=True)
        import inflection

    return inflection


def ordinal(n: int) -> str:
    """
    Overview:
        Get ordinal suffix of one number.

    :param n: The given number.
    :return suffix: Ordinal suffix for number ``n``.

    Examples::
        >>> from hbutils.string import ordinal
        >>> ordinal(1)
        'st'
        >>> ordinal(2)
        'nd'
        >>> ordinal(3)
        'rd'
        >>> ordinal(4)
        'th'
        >>> ordinal(11)
        'th'
        >>> ordinal(21)
        'st'
        >>> ordinal(1001)
        'st'

    .. note::
        This function is intergratted from `inflection <https://github.com/jpvanhal/inflection>`_ package.
        It will be automatically installed once you use :func:`ordinal`.
    """
    inflection = _get_inflection()
    return inflection.ordinal(n)


def ordinalize(n: int) -> str:
    """
    Overview:
        Get full ordinal word of one number.

    :param n: The given number.
    :return word: Full ordinal word for number ``n``.

    Examples::
        >>> from hbutils.string import ordinalize
        >>> ordinalize(1)
        '1st'
        >>> ordinalize(2)
        '2nd'
        >>> ordinalize(3)
        '3rd'
        >>> ordinalize(4)
        '4th'
        >>> ordinalize(11)
        '11th'
        >>> ordinalize(21)
        '21st'
        >>> ordinalize(1001)
        '1001st'

    .. note::
        This function is intergratted from `inflection <https://github.com/jpvanhal/inflection>`_ package.
        It will be automatically installed once you use :func:`ordinalize`.
    """
    inflection = _get_inflection()
    return inflection.ordinalize(n)
