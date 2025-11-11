"""
Overview:
    Useful utilities for pluralizing and singularizing words. This module provides
    convenient functions to convert words between singular and plural forms, and to
    format words with their counts in grammatically correct forms.
"""

from .inflection import pluralize, singularize

__all__ = [
    'plural_form', 'plural_word', 'singular_form'
]


def plural_form(word: str) -> str:
    """
    Get the pluralized form of the given word.

    The same as :func:`hbutils.string.inflection.pluralize`.

    :param word: The given word to be pluralized.
    :type word: str

    :return: Pluralized word.
    :rtype: str

    Examples::
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

    The same as :func:`hbutils.string.inflection.singularize`.

    :param word: The given word to be singularized.
    :type word: str

    :return: Singular form of word.
    :rtype: str

    Examples::
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
    Get plural form of the whole word, with the number before the word.

    This function formats a word with its count in a grammatically correct way.
    If the count is 1, the singular form is used; otherwise, the plural form is used.

    :param count: Count of the word, should be a non-negative integer.
    :type count: int
    :param word: Word to be pluralized.
    :type word: str

    :return: Pluralized word with the number.
    :rtype: str

    Examples::
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
