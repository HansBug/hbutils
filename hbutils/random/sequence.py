"""
Overview:
    Random function about the sequences.
"""
import random as random_module
from typing import Collection, TypeVar

__all__ = ['shuffle', 'multiple_choice']

_random_inst = getattr(random_module, '_inst')
_ElementType = TypeVar('_ElementType')


def shuffle(seq: Collection[_ElementType], *, random=None):
    """
    Overview:
        Shuffle the given collection.

    Arguments:
        - seq (:obj:`Collection[_ElementType]`): Original sequence to be shuffled.
        - random: Random instance, default is ``None`` which means use the native instance \
            from ``random`` module.

    Examples::
        >>> shuffle([1, 2, 3])
        [3, 1, 2]  # just one of the possiblities
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
                    put_back: bool = False, random=None):
    r"""
    Overview:
        Choose multiple items from the given sequence ``seq``.

    Arguments:
        - seq (:obj:`Collection[_ElementType]`): Original sequence to be chosen.
        - count (:obj:`int`): Choose count. Should be no more than length of ``seq`` \
            when put back is disabled.
        - put\_back (:obj:`bool`): Put back the chosen items or not, default is ``False`` \
            which means do not put back, the chosen items will be unique.
        - random: Random instance, default is ``None`` which means use the native instance \
            from ``random`` module.

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
