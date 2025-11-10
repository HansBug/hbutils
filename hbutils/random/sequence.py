"""
Overview:
    Random function utilities for sequences, providing shuffle and multiple choice operations
    with support for custom random instances and various collection types.
"""
import random as random_module
from typing import Collection, TypeVar, Optional

__all__ = ['shuffle', 'multiple_choice']

_random_inst = getattr(random_module, '_inst')
_ElementType = TypeVar('_ElementType')


def shuffle(seq: Collection[_ElementType], *, random: Optional[random_module.Random] = None) -> Collection[
    _ElementType]:
    """
    Shuffle the given collection and return a new shuffled collection of the same type.

    :param seq: Original sequence to be shuffled.
    :type seq: Collection[_ElementType]
    :param random: Random instance for shuffling. If None, uses the native instance from ``random`` module.
    :type random: Optional[random_module.Random]

    :return: A new shuffled collection of the same type as input.
    :rtype: Collection[_ElementType]

    Examples::
        >>> shuffle([1, 2, 3])
        [3, 1, 2]  # just one of the possibilities
        >>> shuffle(('a', 1, 'b', 2))
        ('b', 1, 2, 'a')  # the tuple type will be kept
    """
    random = random or _random_inst
    seq_type, seq = type(seq), list(seq)
    ids = list(range(len(seq)))
    random.shuffle(ids)

    # noinspection PyArgumentList
    return seq_type([seq[i] for i in ids])


def multiple_choice(seq: Collection[_ElementType], count: int, *,
                    put_back: bool = False, random: Optional[random_module.Random] = None) -> Collection[_ElementType]:
    """
    Choose multiple items from the given sequence with or without replacement.

    :param seq: Original sequence to choose items from.
    :type seq: Collection[_ElementType]
    :param count: Number of items to choose. Should be no more than length of ``seq`` when put_back is False.
    :type count: int
    :param put_back: Whether to put back the chosen items (sampling with replacement). 
        If False, chosen items will be unique. Default is False.
    :type put_back: bool
    :param random: Random instance for selection. If None, uses the native instance from ``random`` module.
    :type random: Optional[random_module.Random]

    :return: A new collection of the same type as input containing the chosen items.
    :rtype: Collection[_ElementType]
    :raises ValueError: If put_back is False and count exceeds the length of seq.

    Examples::
        >>> multiple_choice([1, 2, 3], 2)
        [2, 3]  # one of the possibilities
        >>> multiple_choice([1, 2, 3], 2, put_back=True)
        [2, 2]  # this is possible when put back option is on
    """
    random = random or _random_inst
    seq_type, seq = type(seq), list(seq)
    n = len(seq)
    if not put_back and count > n:
        raise ValueError(f'Choice put back disabled, count must be no more than {repr(n)} but {repr(count)} found.')

    if put_back:
        ids = [random.randint(0, n - 1) for _ in range(count)]
    else:
        ids = shuffle(list(range(n)), random=random)[:count]

    # noinspection PyArgumentList
    return seq_type([seq[i] for i in ids])
