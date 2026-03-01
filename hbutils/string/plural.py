"""
Pluralization and singularization helpers for English words.

This module provides thin wrappers around the underlying inflection utilities
for converting words between singular and plural forms. It also exposes a
helper for formatting a word with its count using grammatically correct forms.

The module contains the following public components:

* :func:`plural_form` - Convert a word to its plural form.
* :func:`singular_form` - Convert a word to its singular form.
* :func:`plural_word` - Format a word with its count using correct plurality.

Example::

    >>> from hbutils.string.plural import plural_form, singular_form, plural_word
    >>> plural_form('woman')
    'women'
    >>> singular_form('women')
    'woman'
    >>> plural_word(3, 'word')
    '3 words'

.. note::
   These helpers delegate to :func:`hbutils.string.inflection.pluralize` and
   :func:`hbutils.string.inflection.singularize`, which implement both regular
   and irregular English inflection rules.

"""

from .inflection import pluralize, singularize

__all__ = [
    'plural_form', 'plural_word', 'singular_form'
]


def plural_form(word: str) -> str:
    """
    Get the pluralized form of the given word.

    This function is a thin wrapper around
    :func:`hbutils.string.inflection.pluralize` and therefore supports the same
    irregular and uncountable noun handling as the underlying implementation.

    :param word: The word to be pluralized.
    :type word: str
    :return: Pluralized word.
    :rtype: str

    Example::

        >>> from hbutils.string import plural_form
        >>> plural_form('it')
        'they'
        >>> plural_form('word')
        'words'
        >>> plural_form('woman')
        'women'
    """
    return pluralize(word)


def singular_form(word: str) -> str:
    """
    Get the singular form of the given word.

    This function is a thin wrapper around
    :func:`hbutils.string.inflection.singularize` and therefore supports the
    same irregular and uncountable noun handling as the underlying
    implementation.

    :param word: The word to be singularized.
    :type word: str
    :return: Singular form of the word.
    :rtype: str

    Example::

        >>> from hbutils.string import singular_form
        >>> singular_form('they')
        'it'
        >>> singular_form('it')
        'it'
        >>> singular_form('women')
        'woman'
        >>> singular_form('words')
        'word'
        >>> singular_form('themselves')
        'itself'
    """
    return singularize(word)


def plural_word(count: int, word: str) -> str:
    """
    Format a word with its count using correct plurality.

    If ``count`` is 1, the singular form is used; otherwise, the plural form is
    used. The singular form is derived from :func:`singular_form` and the
    plural form from :func:`plural_form`, which handle irregular inflections.

    :param count: Count of the word.
    :type count: int
    :param word: Word to be pluralized.
    :type word: str
    :return: Formatted string with the count and correct word form.
    :rtype: str

    Example::

        >>> from hbutils.string import plural_word
        >>> plural_word(0, 'word')
        '0 words'
        >>> plural_word(1, 'word')
        '1 word'
        >>> plural_word(2, 'word')
        '2 words'
        >>> plural_word(20, 'word')
        '20 words'
        >>> plural_word(233, 'word')
        '233 words'
    """
    single_word = singular_form(word)
    if count != 1:
        return f'{count} {plural_form(single_word)}'
    else:
        return f'{count} {single_word}'
