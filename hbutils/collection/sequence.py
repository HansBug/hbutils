from typing import Union, TypeVar, Sequence

__all__ = [
    'unique',
]

_ElementType = TypeVar('_ElementType')


def unique(s: Union[Sequence[_ElementType]]) -> Sequence[_ElementType]:
    """
    Overview:
        Unique all the values in the given ``s``, preserving its original order.

    :param s: Original sequence.
    :return: Unique sequence, with the original type.

    Examples::
        >>> from hbutils.collection import unique
        >>>
        >>> unique([1, 2, 3, 1])
        [1, 2, 3]
        >>> unique(('a', 'b', 'a', 'c', 'd', 'e', 'b'))
        ('a', 'b', 'c', 'd', 'e')
        >>> unique([3, 1, 2, 1, 4, 3])
        [3, 1, 2, 4]
    """
    _set, _result = set(), []
    for element in s:
        if element not in _set:
            _result.append(element)
            _set.add(element)

    return type(s)(_result)
