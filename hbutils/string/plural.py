"""
Overview:
    Useful utilities for pluralize your words.
"""

from .inflection import pluralize, singularize

__all__ = [
    'plural_form', 'plural_word', 'singular_form'
]


def plural_form(word: str) -> str:
    """
    Overview:
        Get the pluralized form of the given ``word``.

        The same as :func:`hbutils.string.inflection.pluralize`.

    Arguments:
        - word (:obj:`str`): The given word to be pluralized.

    Returns:
        - pluralized (:obj:`str`): Pluralized word.

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
    Overview:
        Get the singular form of the given ``word``.

        The same as :func:`hbutils.string.inflection.singularize`.

    Arguments:
        - word (:obj:`str`): The given word to be singularized.

    Returns:
        - single (:obj:`str`): Singular form of word.

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
    Overview:
        Get plural form of the whole word, with the number before the word.

    Arguments:
        - count (:obj:`int`): Count of the word, should be a non-negative integer.
        - word (:obj:`str`): Word to be pluralized.

    Returns:
        - plural_word (:obj:`str`): Pluralized word, with the number.

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
