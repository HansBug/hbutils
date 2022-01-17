"""
Overview:
    Useful utilities for pluralize your words.
"""
import warnings
from functools import lru_cache
from typing import Optional

import inflect

__all__ = ['plural_form', 'plural_word', 'singular_form']


@lru_cache()
def _default_engine():
    return inflect.engine()


def plural_form(word: str, engine: Optional[inflect.engine] = None) -> str:
    """
    Overview:
        Get the pluralized form of the given ``word``.

    Arguments:
        - word (:obj:`str`): The given word to be pluralized.
        - engine (:obj:`Optional[inflect.engine]`): Engine to be used, \
            default is ``None`` which means just use the default one.

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
    engine = engine or _default_engine()
    return engine.plural(word)


def singular_form(word: str, engine: Optional[inflect.engine] = None) -> str:
    """
    Overview:
        Get the singular form of the given ``word``.

    Arguments:
        - word (:obj:`str`): The given word to be singularized.
        - engine (:obj:`Optional[inflect.engine]`): Engine to be used, \
            default is ``None`` which means just use the default one.

    Returns:
        - single (:obj:`str`): Singular form of word.

    Examples::
        >>> from hbutils.string import singular_form
        >>> singular_form('they')
        'it'
        >>> singular_form('them')
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
    engine = engine or _default_engine()
    result = engine.singular_noun(word)
    if not result:  # already a singular form
        return word
    else:
        return result


def plural_word(count: int, word: str,
                num_text: bool = False, num_threshold: Optional[int] = None,
                engine: Optional[inflect.engine] = None) -> str:
    """
    Overview:
        Get plural form of the whole word, with the number before the word.

    Arguments:
        - count (:obj:`int`): Count of the word, should be a non-negative integer.
        - word (:obj:`str`): Word to be pluralized.
        - num_text (:obj:`bool`): Show the number as text format or not, \
            default is ``False`` which means just use the arabic number for all the cases.
        - num_threshold (:obj:`Optional[int]`): Threshold value when the number is shown as text, \
            default is ``None`` which means just use english text format for all the cases.
        - engine (:obj:`Optional[inflect.engine]`): Engine to be used, \
            default is ``None`` which means just use the default one.

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
        >>> plural_word(20, 'word', num_text=True)
        'twenty words'
        >>> plural_word(233, 'word', num_text=True)
        'two hundred and thirty-three words'
        >>> plural_word(20, 'word', num_text=True, num_threshold=99)
        'twenty words'
        >>> plural_word(233, 'word', num_text=True, num_threshold=99)
        '233 words'
    """
    engine = engine or _default_engine()
    if num_text:
        number = engine.number_to_words(count, threshold=num_threshold)
    else:
        if num_threshold is not None:
            warnings.warn(UserWarning('Text-formatted number is not enabled, '
                                      'so the num_threshold argument will be ignored.'), stacklevel=2)
        number = str(count)

    single_word = singular_form(word, engine)
    final_word = engine.plural(single_word, count)
    return f'{number} {final_word}'
