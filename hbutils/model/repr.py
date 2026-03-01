"""
Representation formatting utilities for model-like objects.

This module provides a small but flexible utility for generating consistent
``__repr__`` output across custom classes. It is designed to simplify the
construction of informative object representations while allowing conditional
display of attributes.

The module contains the following public function:

* :func:`get_repr_info` - Build a formatted representation string for an object

Example::

    >>> from hbutils.model.repr import get_repr_info
    >>> class Point:
    ...     def __init__(self, x, y=None):
    ...         self._x = x
    ...         self._y = y
    ...     def __repr__(self):
    ...         return get_repr_info(
    ...             cls=self.__class__,
    ...             args=[
    ...                 ('y', (lambda: self._y, lambda: self._y is not None)),
    ...                 ('x', lambda: self._x),
    ...             ]
    ...         )
    ...
    >>> Point(3, 4)
    <Point y: 4, x: 3>
    >>> Point(3)
    <Point x: 3>

.. note::
   This utility does not access object state directly; all data access is done
   through the provided callables. This makes it safe to use for lazily computed
   properties or sensitive attributes.
"""
from typing import List, Tuple, Callable, Union, Any, Sequence

__all__ = [
    'get_repr_info',
]


def get_repr_info(
    cls: type,
    args: Sequence[
        Union[
            Tuple[str, Callable[[], Any]],
            Tuple[str, Tuple[Callable[[], Any], Callable[[], bool]]],
            Tuple[str, Callable[[], Any], Callable[[], bool]],
        ]
    ],
) -> str:
    """
    Get representation information for object.

    This function generates a formatted string representation of an object based on
    the provided class type and argument information. It can be used in ``__repr__``
    methods to create consistent and informative object representations.

    :param cls: The class type of the object to represent.
    :type cls: type
    :param args: A sequence of tuples describing how each field should be shown.
        Each item must be one of the following forms:

        - ``(name, data_func)``: Always display ``name`` with value from ``data_func``.
        - ``(name, (data_func, present_func))``: Display only if ``present_func`` is ``True``.
        - ``(name, data_func, present_func)``: Equivalent to the previous form.

        Where:

        - ``name`` (str): The name of the field to display.
        - ``data_func`` (Callable): Callable returning the value to display.
        - ``present_func`` (Callable): Callable returning ``True`` if the field should be displayed.
    :type args: Sequence[Union[Tuple[str, Callable[[], Any]], Tuple[str, Tuple[Callable[[], Any], Callable[[], bool]]], Tuple[str, Callable[[], Any], Callable[[], bool]]]]

    :return: A formatted representation string in the format ``<ClassName arg1: value1, arg2: value2>``.
        If no fields are displayed, the format is ``<ClassName>``.
    :rtype: str

    :raises ValueError: If a tuple's length is not 2 or 3.
    :raises TypeError: If an argument item is not a tuple.

    Example::

        >>> from hbutils.model.repr import get_repr_info
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
