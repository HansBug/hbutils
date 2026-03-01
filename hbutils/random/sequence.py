"""
Random utilities for sequence-like collections.

This module provides utilities for shuffling sequences and selecting multiple
items, with optional control of the random number generator. The functions
preserve the input collection type by reconstructing a new instance from
shuffled or selected elements.

The module contains the following public functions:

* :func:`shuffle` - Shuffle a collection and return a new collection of the same type.
* :func:`multiple_choice` - Select multiple elements with or without replacement.

.. note::
   The returned collection is constructed by calling ``type(seq)`` with a list
   of items, so the input type must be constructible from a list of elements.

Example::

    >>> from hbutils.random.sequence import shuffle, multiple_choice
    >>> shuffle([1, 2, 3])  # doctest: +SKIP
    [3, 1, 2]
    >>> multiple_choice(('a', 'b', 'c'), 2)  # doctest: +SKIP
    ('b', 'a')

"""
import random as random_module
from typing import Collection, TypeVar, Optional

__all__ = ['shuffle', 'multiple_choice']

_random_inst = getattr(random_module, '_inst')
_ElementType = TypeVar('_ElementType')


def shuffle(seq: Collection[_ElementType], *, random: Optional[random_module.Random] = None) -> Collection[_ElementType]:
    """
    Shuffle the given collection and return a new shuffled collection of the same type.

    The function converts the input collection to a list, creates a shuffled
    index order using the provided random instance, and then reconstructs a new
    collection using ``type(seq)`` from the reordered elements.

    :param seq: Original collection to be shuffled.
    :type seq: Collection[_ElementType]
    :param random: Random instance for shuffling. If ``None``, uses the native
        instance from the :mod:`random` module.
    :type random: Optional[random_module.Random]
    :return: A new shuffled collection of the same type as ``seq``.
    :rtype: Collection[_ElementType]

    .. note::
       The input collection is not modified.

    Example::

        >>> shuffle([1, 2, 3])  # doctest: +SKIP
        [3, 1, 2]
        >>> shuffle(('a', 1, 'b', 2))  # doctest: +SKIP
        ('b', 1, 2, 'a')

    """
    random = random or _random_inst
    seq_type, seq = type(seq), list(seq)
    ids = list(range(len(seq)))
    random.shuffle(ids)

    # noinspection PyArgumentList
    return seq_type([seq[i] for i in ids])


def multiple_choice(
    seq: Collection[_ElementType],
    count: int,
    *,
    put_back: bool = False,
    random: Optional[random_module.Random] = None
) -> Collection[_ElementType]:
    """
    Choose multiple items from the given collection with or without replacement.

    When ``put_back`` is ``False``, the selection is performed without replacement
    and ``count`` must not exceed the collection length. When ``put_back`` is
    ``True``, sampling is done with replacement, allowing repeated items.

    :param seq: Original collection to choose items from.
    :type seq: Collection[_ElementType]
    :param count: Number of items to choose. Must be no more than ``len(seq)``
        when ``put_back`` is ``False``.
    :type count: int
    :param put_back: Whether to put back the chosen items (sampling with
        replacement). If ``False``, chosen items will be unique.
    :type put_back: bool
    :param random: Random instance for selection. If ``None``, uses the native
        instance from the :mod:`random` module.
    :type random: Optional[random_module.Random]
    :return: A new collection of the same type as ``seq`` containing the chosen items.
    :rtype: Collection[_ElementType]
    :raises ValueError: If ``put_back`` is ``False`` and ``count`` exceeds
        the length of ``seq``.

    Example::

        >>> multiple_choice([1, 2, 3], 2)  # doctest: +SKIP
        [2, 3]
        >>> multiple_choice([1, 2, 3], 2, put_back=True)  # doctest: +SKIP
        [2, 2]

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
