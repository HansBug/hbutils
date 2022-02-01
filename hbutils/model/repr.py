"""
Overview:
    Useful functions for build representation format of object.
"""
from typing import List, Tuple

__all__ = [
    'get_repr_info',
]


def get_repr_info(cls: type, args: List[Tuple]) -> str:
    """
    Overview:
        Get representation information for object.
        Can be used in ``__repr__`` method for class.

    Arguments:
        - cls (:obj:`type`): Object's type.
        - args (:obj:`List[Tuple]`): Argument display information.

    Returns:
        - repr (:obj:`str`): Representation string.

    Examples::
        >>> from hbutils.model import get_repr_info
        >>> class Sum:
        ...     def __init__(self, a, b):
        ...         self.__a = a
        ...         self.__b = b
        ...     def __repr__(self):
        ...         return get_repr_info(
        ...             cls=self.__class__,
        ...             args=[
        ...                 ('b', lambda: self.__b, lambda: self.__b is not None),
        ...                 ('a', lambda: self.__a),
        ...             ]
        ...         )
        ...
        >>> Sum(1, 2)
        <Sum b: 2, a: 1>
        >>> Sum(1, None)
        <Sum a: 1>
        >>> Sum(None, None)
        <Sum a: None>
    """
    _data_items = []
    for item in args:
        if isinstance(item, tuple):
            if len(item) == 2:
                name, fd = item
                if isinstance(fd, tuple):
                    _data_func, _present_func = fd
                else:
                    _data_func, _present_func = fd, lambda: True
            elif len(item) == 3:
                name, _data_func, _present_func = item
            else:
                raise ValueError('Tuple\'s length should be 2 or 3 but {actual} found.'.format(actual=repr(len(item))))

            if _present_func():
                _data_items.append('{name}: {data}'.format(name=name, data=_data_func()))
        else:
            raise TypeError(
                'Argument item should be tuple but {actual} found.'.format(actual=repr(type(item).__name__)))

    if _data_items:
        return '<{cls} {data}>'.format(cls=cls.__name__, data=', '.join(_data_items))
    else:
        return '<{cls}>'.format(cls=cls.__name__)
