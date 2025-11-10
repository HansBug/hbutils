"""
Overview:
    Useful functions for building representation format of objects.
    
This module provides utilities to generate string representations for custom classes,
particularly useful for implementing ``__repr__`` methods with flexible display options.
"""
from typing import List, Tuple, Callable, Union, Any

__all__ = [
    'get_repr_info',
]


def get_repr_info(cls: type, args: List[
    Tuple[str, Union[Callable[[], Any], Tuple[Callable[[], Any], Callable[[], bool]]], Callable[[], bool]]]) -> str:
    """
    Get representation information for object.
    
    This function generates a formatted string representation of an object based on
    the provided class type and argument information. It can be used in ``__repr__``
    methods to create consistent and informative object representations.

    :param cls: The class type of the object to represent.
    :type cls: type
    :param args: A list of tuples containing argument display information. Each tuple can have:
        
        - 2 elements: (name, data_func) or (name, (data_func, present_func))
        - 3 elements: (name, data_func, present_func)
        
        Where:
        
        - name (str): The name of the argument to display
        - data_func (Callable): A callable that returns the value to display
        - present_func (Callable): A callable that returns True if the argument should be displayed
    :type args: List[Tuple]
    
    :return: A formatted representation string in the format ``<ClassName arg1: value1, arg2: value2>``
    :rtype: str
    
    :raises ValueError: If a tuple's length is not 2 or 3.
    :raises TypeError: If an argument item is not a tuple.

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
