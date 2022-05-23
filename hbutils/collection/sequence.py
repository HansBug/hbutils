from typing import Union, TypeVar, Sequence, Callable, Optional, Dict, List, Iterable

__all__ = [
    'unique',
    'group_by',
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


_GroupType = TypeVar('_GroupType')
_ResultType = TypeVar('_ResultType')


def group_by(s: Iterable[_ElementType],
             key: Callable[[_ElementType], _GroupType],
             gfunc: Optional[Callable[[List[_ElementType]], _ResultType]] = None) -> Dict[_GroupType, _ResultType]:
    """
    Overview:
        Divide the elements into groups.

    :param s: Elements.
    :param key: Group key, should be a callable object.
    :param gfunc: Post-process function for groups, should be a callable object. Default is ``None`` which means \
        no post-processing will be performed.
    :return: Grouping result.

    Examples::
        >>> from hbutils.collection import group_by
        >>>
        >>> foods = [
        ...     'apple', 'orange', 'pear',
        ...     'banana', 'fish', 'pork', 'milk',
        ... ]
        >>> group_by(foods, len)  # group by length
        {5: ['apple'], 6: ['orange', 'banana'], 4: ['pear', 'fish', 'pork', 'milk']}
        >>> group_by(foods, len, len)  # group and get length
        {5: 1, 6: 2, 4: 4}
        >>> group_by(foods, lambda x: x[0])  # group by first letter
        {'a': ['apple'], 'o': ['orange'], 'p': ['pear', 'pork'], 'b': ['banana'], 'f': ['fish'], 'm': ['milk']}
        >>> group_by(foods, lambda x: x[0], len)  # group and get length
        {'a': 1, 'o': 1, 'p': 2, 'b': 1, 'f': 1, 'm': 1}
    """

    gfunc = gfunc or (lambda x: x)

    _result_dict: Dict[_GroupType, List[_ElementType]] = {}
    for item in s:
        _item_key = key(item)
        if _item_key not in _result_dict:
            _result_dict[_item_key] = []
        _result_dict[_item_key].append(item)

    return {
        key: gfunc(grps)
        for key, grps in _result_dict.items()
    }
