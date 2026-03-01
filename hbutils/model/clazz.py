"""
Class modeling utilities for declarative Python objects.

This module provides decorators and helper functions that simplify the creation
of lightweight data-centric classes. It focuses on generating commonly needed
behaviors such as automatic field access, visual representations, constructor
generation, hash/equality support, and property accessors, all while supporting
name-mangled private attributes.

The module contains the following main public components:

* :func:`get_field` - Retrieve attributes with support for private name mangling
* :func:`asitems` - Declare class-level field names
* :func:`visual` - Generate a human-friendly ``__repr__`` implementation
* :func:`constructor` - Generate an ``__init__`` constructor from field specs
* :func:`hasheq` - Generate ``__hash__``, ``__eq__``, and ``__ne__`` methods
* :func:`accessor` - Generate property accessors for private fields

Example::

    >>> @accessor(readonly=True)
    >>> @visual()
    >>> @constructor(['x', ('y', 2)])
    >>> class Point:
    ...     pass
    >>> p = Point(1)
    >>> p
    <Point x: 1, y: 2>
    >>> p.x
    1

.. note::
   These decorators are designed to cooperate. For example, using
   :func:`asitems` enables automatic field discovery by :func:`constructor`,
   :func:`visual`, and :func:`hasheq`.

"""
import os
import textwrap
from typing import Optional, Iterable, Callable, Any, List, Tuple, Union, Type

from ._info import _PACKAGE_RST
from ..config.meta import __VERSION__
from ..design.singleton import SingletonMark
from ..reflection import fassign

__all__ = [
    'get_field',
    'asitems', 'visual', 'constructor', 'hasheq', 'accessor',
]

CLASS_WRAPPER_UPDATES = ()


def _cls_field_name(cls: Type[Any], name: str) -> str:
    """
    Get the mangled field name for a class.

    This function applies Python's name mangling rules to private attributes
    (names starting with ``__``) so that the correct attribute name can be used
    for reflection or attribute access.

    :param cls: The class type.
    :type cls: type
    :param name: The field name.
    :type name: str
    :return: The mangled field name.
    :rtype: str

    .. note::
        Private attributes are transformed into ``_{ClassName}__{name}``.
    """
    if name.startswith('__'):
        return f'_{cls.__name__.lstrip("_")}__{name[2:]}'
    else:
        return name


_NO_DEFAULT_VALUE = SingletonMark('no_default_value')


def get_field(obj: Any, name: str, default: Any = _NO_DEFAULT_VALUE) -> Any:
    """
    Get field from object with support for private attributes.

    This function resolves name-mangled private attributes and uses ``getattr``
    to fetch the field. When a ``default`` is provided, it will be returned
    instead of raising :class:`AttributeError`.

    :param obj: The given object.
    :type obj: object
    :param name: Field to be retrieved.
    :type name: str
    :param default: Default value to return if the field does not exist.
        If not provided, the absence of the field raises :class:`AttributeError`.
    :type default: Any, optional
    :return: Field value for the requested field.
    :rtype: Any
    :raises AttributeError: If the field does not exist and no default is provided.

    Example::

        >>> class MyClass:
        ...     def __init__(self):
        ...         self.__private_field = 42
        >>> obj = MyClass()
        >>> get_field(obj, '__private_field')
        42
        >>> get_field(obj, 'nonexistent', default='default_value')
        'default_value'
    """
    _field_name = _cls_field_name(type(obj), name)
    if default is _NO_DEFAULT_VALUE:
        return getattr(obj, _field_name)
    else:
        return getattr(obj, _field_name, default)


def _cls_private_prefix(cls: Type[Any]) -> str:
    """
    Get the private field prefix for a class.

    This prefix is the internal name-mangling prefix used for private
    attributes, e.g., ``_ClassName__``.

    :param cls: The class type.
    :type cls: type
    :return: The private field prefix string.
    :rtype: str
    """
    cls_name = cls.__name__.lstrip('_')
    return f'_{cls_name}__'


def _auto_get_items_from_cls(cls: Type[Any]) -> List[str]:
    """
    Get items from class's ``__items__`` attribute.

    :param cls: The class type.
    :type cls: type
    :return: The items list.
    :rtype: list[str]
    :raises AttributeError: If the class does not have ``__items__`` attribute.
    """
    return cls.__items__


def _auto_get_items(obj: Any, cls_prefix: Optional[str] = None) -> List[str]:
    """
    Automatically determine item names from an object.

    The function first tries to retrieve items from ``__items__`` on the class.
    If not available, it inspects the object's attributes and extracts private
    attribute names based on the class's private prefix.

    :param obj: The object to inspect.
    :type obj: object
    :param cls_prefix: The class private prefix. Defaults to None.
    :type cls_prefix: Optional[str]
    :return: Sorted list of item names.
    :rtype: list[str]
    """
    _type = type(obj)
    try:
        return _auto_get_items_from_cls(_type)
    except AttributeError:
        cls_prefix = cls_prefix or _cls_private_prefix(_type)

        items = []
        for name in dir(obj):
            if name.startswith(cls_prefix):
                items.append(name[len(cls_prefix):])

        return sorted(items)


def _get_value(self: Any, vname: str, cls_prefix: Optional[str] = None) -> Any:
    """
    Get value from object by name, supporting both regular and private attributes.

    :param self: The object instance.
    :type self: object
    :param vname: The value name.
    :type vname: str
    :param cls_prefix: The class private prefix. Defaults to None.
    :type cls_prefix: Optional[str]
    :return: The attribute value.
    :rtype: Any
    :raises AttributeError: If the attribute does not exist.
    """
    cls_prefix = cls_prefix or _cls_private_prefix(type(self))
    try:
        return getattr(self, vname)
    except AttributeError:
        return getattr(self, cls_prefix + vname)


def asitems(items: Iterable[str]) -> Callable[[Type[Any]], Type[Any]]:
    """
    Define fields in the class level.

    This decorator assigns the provided field names to ``__items__``, which
    can be consumed by other decorators such as :func:`constructor`,
    :func:`visual`, :func:`hasheq`, and :func:`accessor`.

    :param items: Field name items.
    :type items: Iterable[str]
    :return: Decorator to decorate the given class.
    :rtype: Callable

    Example::

        >>> @visual()
        >>> @constructor(doc='''
        ...     Overview:
        ...         This is the constructor of class :class:`T`.
        ... ''')
        >>> @asitems(['x', 'y'])
        >>> class T:
        ...     @property
        ...     def x(self):
        ...         return self.__first
        ...
        ...     @property
        ...     def y(self):
        ...         return self.__second

    .. note::
        This decorator sets ``__items__`` on the class, which is used by
        other decorators to determine which fields to process.
    """

    def _decorator(cls: Type[Any]) -> Type[Any]:
        """
        Attach the given item list to ``cls.__items__``.

        :param cls: Class to decorate.
        :type cls: type
        :return: The decorated class.
        :rtype: type
        """
        _cls_prefix = _cls_private_prefix(cls)
        cls.__items__ = list(items)
        return cls

    return _decorator


def visual(items: Optional[Iterable[Union[str, Tuple[str, Callable[[Any], str]]]]] = None,
           show_id: bool = False) -> Callable[[Type[Any]], Type[Any]]:
    """
    Decorate class to be visible by ``repr``.

    :param items: Items to be displayed. Default is None, which means
        automatically find the private fields and display them. Items can be
        strings (field names) or ``(name, repr_func)`` pairs.
    :type items: Optional[Iterable[Union[str, Tuple[str, Callable[[Any], str]]]]]
    :param show_id: Show hex id in representation string or not. Defaults to False.
    :type show_id: bool
    :return: Decorator to decorate the given class.
    :rtype: Callable

    Example::

        >>> @visual()
        >>> class T:
        ...     def __init__(self, x, y):
        ...         self.__first = x
        ...         self.__second = y
        >>> repr(T(1, 2))
        '<T first: 1, second: 2>'

        >>> @visual(show_id=True)
        >>> class T2:
        ...     def __init__(self, x):
        ...         self.__x = x
        >>> repr(T2(42))
        '<T2 0x... x: 42>'

    .. note::
        This decorator generates a ``__repr__`` method that displays
        the specified fields or all private fields if none are specified.
    """

    def _decorator(cls: Type[Any]) -> Type[Any]:
        """
        Add a dynamic ``__repr__`` implementation to ``cls``.

        :param cls: Class to decorate.
        :type cls: type
        :return: The decorated class.
        :rtype: type
        """
        _cls_prefix = _cls_private_prefix(cls)

        def _get_items(self: Any) -> Iterable[Union[str, Tuple[str, Callable[[Any], str]]]]:
            """
            Resolve items for representation.

            :param self: Instance of the decorated class.
            :type self: object
            :return: Iterable of field names or ``(name, repr_func)`` pairs.
            :rtype: Iterable[Union[str, Tuple[str, Callable[[Any], str]]]]
            """
            if items is None:
                return _auto_get_items(self, _cls_prefix)
            else:
                return items

        def __repr__(self: Any) -> str:
            """
            Return representation format of the decorated class.

            .. note::
                Created by {_PACKAGE_RST}, v{__VERSION__}.
            """
            str_items = []
            for item in _get_items(self):
                if isinstance(item, str):
                    _name, _repr = item, repr
                else:
                    _name, _repr = item

                _value = _get_value(self, _name, _cls_prefix)
                try:
                    _vrepr = _repr(_value)
                except ValueError:
                    pass
                else:
                    str_items.append(f'{_name}: {_vrepr}')

            sentences = []
            if show_id:
                sentences.append(hex(id(self)))
            if str_items:
                sentences.append(', '.join(str_items))
            if sentences:
                str_sentences = ' ' + ' '.join(sentences)
            else:
                str_sentences = ''
            return f'<{type(self).__name__}{str_sentences}>'

        cls.__repr__ = __repr__
        return cls

    return _decorator


_INDENT = ' ' * 4


def constructor(params: Optional[Iterable[Union[str, Tuple[str, Any]]]] = None,
                doc: Optional[str] = None) -> Callable[[Type[Any]], Type[Any]]:
    r"""
    Decorate class to create an init function.

    :param params: Parameters of constructor. Each item should be a string
        (argument name) or a tuple of ``(name, default_value)``. Default is None,
        which means no arguments (unless ``__items__`` is defined on the class).
    :type params: Optional[Iterable[Union[str, Tuple[str, Any]]]]
    :param doc: Documentation of constructor function. Defaults to None.
    :type doc: Optional[str]
    :return: Decorator to decorate the given class.
    :rtype: Callable

    Example::

        >>> @constructor(['x', ('y', 2)], '''
        ...     Overview:
        ...         This is the constructor of class :class:`T`.
        ... ''')
        >>> class T:
        ...     # the same as:
        ...     # def __init__(self, x, y=2):
        ...     #     self.__x = x
        ...     #     self.__y = y
        ...
        ...     @property
        ...     def x(self):
        ...         return self.__x
        ...
        ...     @property
        ...     def y(self):
        ...         return self.__y
        >>> t = T(1)
        >>> t.x, t.y
        (1, 2)

    .. note::
        This decorator generates an ``__init__`` method that stores
        argument values into private attributes using name mangling.
    """

    def _decorator(cls: Type[Any]) -> Type[Any]:
        """
        Create and attach an ``__init__`` method to ``cls``.

        :param cls: Class to decorate.
        :type cls: type
        :return: The decorated class.
        :rtype: type
        """
        _cls_prefix = _cls_private_prefix(cls)

        if params is None:
            items = _auto_get_items_from_cls(cls)
        else:
            items = params or []
        actual_items = []
        arg_items = []
        for it in items:
            if isinstance(it, str):
                itn, itv = it, _NO_DEFAULT_VALUE
            else:
                itn, itv = it

            actual_items.append((itn, itv))
            if itv is _NO_DEFAULT_VALUE:
                arg_items.append(itn)
            else:
                arg_items.append(f'{itn}={repr(itv)}')

        _init_func_str = f"""
def __init__(self, {', '.join(arg_items)}):
{os.linesep.join(f'{_INDENT}self.{_cls_prefix}{name} = {name}' for name, _ in actual_items)}
        """
        fres = {}
        exec(_init_func_str, fres)

        _init_func = fres['__init__']
        _init_func = fassign(__doc__=doc or textwrap.dedent(f'''
        Constructor of class {cls.__name__}.

        .. note::
            Created by {_PACKAGE_RST}, v{__VERSION__}.

            The values of arguments supplied to this constructor \
            will be put into the fields specified.
        '''))(_init_func)
        cls.__init__ = _init_func

        return cls

    return _decorator


def hasheq(items: Optional[Iterable[str]] = None) -> Callable[[Type[Any]], Type[Any]]:
    """
    Decorate class to support hashing and equality comparison.

    :param items: Items to be hashed and compared. Default is None, which means
        automatically find the private fields and use them.
    :type items: Optional[Iterable[str]]
    :return: Decorator to decorate the given class.
    :rtype: Callable

    Example::

        >>> @hasheq(['x', 'y'])
        >>> class T:
        ...     def __init__(self, x, y):
        ...         self.__first = x
        ...         self.__second = y
        >>> t1 = T(1, 2)
        >>> t2 = T(1, 2)
        >>> t1 == t2
        True
        >>> hash(t1) == hash(t2)
        True

        Using with :func:`asitems`::

        >>> @hasheq()
        >>> @constructor()
        >>> @asitems(['x', 'y'])
        >>> class T1:
        ...     pass
        >>> t1 = T1(1, 2)
        >>> t2 = T1(1, 2)
        >>> t1 == t2
        True

    .. note::
        This decorator generates ``__hash__``, ``__eq__``, and ``__ne__`` methods
        for the class based on the specified fields.
    """

    def _decorator(cls: Type[Any]) -> Type[Any]:
        """
        Add hash and equality methods to ``cls``.

        :param cls: Class to decorate.
        :type cls: type
        :return: The decorated class.
        :rtype: type
        """
        _cls_prefix = _cls_private_prefix(cls)

        def _get_items(self: Any) -> Iterable[str]:
            """
            Resolve items to be used for hashing and equality.

            :param self: Instance of the decorated class.
            :type self: object
            :return: Iterable of field names.
            :rtype: Iterable[str]
            """
            if items is None:
                return _auto_get_items(self, _cls_prefix)
            else:
                return items

        def _get_obj_values(self: Any) -> Tuple[Any, ...]:
            """
            Collect values of fields participating in hash/equality.

            :param self: Instance of the decorated class.
            :type self: object
            :return: Tuple of field values.
            :rtype: tuple
            """
            return tuple(_get_value(self, name, _cls_prefix) for name in _get_items(self))

        def __hash__(self: Any) -> int:
            """
            Hash value of class {cls.__name__}'s instances.

            .. note::
                Created by {_PACKAGE_RST}, v{__VERSION__}.

                The return value is calculated based on the \
                values of the internally specified fields.
            """
            return hash(_get_obj_values(self))

        def __eq__(self: Any, other: Any) -> bool:
            """
            Equality between class {cls.__name__}'s instances.

            .. note::
                Created by {_PACKAGE_RST}, v{__VERSION__}.

                Currently, the return value is True only if both objects \
                are of class {cls.__name__} (subclasses are not permitted) and the \
                values of the internally specified fields are all equal; \
                otherwise, it is always False.
            """
            if self is other:
                return True
            elif type(self) == type(other):
                return _get_obj_values(self) == _get_obj_values(other)
            else:
                return False

        def __ne__(self: Any, other: Any) -> bool:
            """
            Non-equality between class {cls.__name__}'s instances.

            .. note::
                Created by {_PACKAGE_RST}, v{__VERSION__}.

                Currently, the return value is False only if both objects \
                are of class {cls.__name__} (subclasses are not permitted) and the \
                values of the internally specified fields are all equal; \
                otherwise, it is always True.
            """
            return not __eq__(self, other)

        cls.__hash__ = __hash__
        cls.__eq__ = __eq__
        cls.__ne__ = __ne__

        return cls

    return _decorator


_READONLY_MARKS = {'r', 'ro', 'readonly'}
_WRITABLE_MARKS = {'w', 'rw', 'writable'}


def _is_writable(mark: str) -> bool:
    """
    Check if an accessibility mark indicates writable access.

    :param mark: The accessibility mark string.
    :type mark: str
    :return: True if writable, False if readonly.
    :rtype: bool
    :raises ValueError: If the mark is not recognized.

    .. note::
        Valid readonly marks: ``'r'``, ``'ro'``, ``'readonly'``.
        Valid writable marks: ``'w'``, ``'rw'``, ``'writable'``.
    """
    if mark.lower() in _READONLY_MARKS:
        return False
    elif mark.lower() in _WRITABLE_MARKS:
        return True
    else:
        raise ValueError(f'Unknown accessible mark - {repr(mark)}.')


def accessor(items: Optional[Iterable[Union[str, Tuple[str, str]]]] = None,
             readonly: bool = False) -> Callable[[Type[Any]], Type[Any]]:
    """
    Decorate class to be accessible by property accessors.

    :param items: Items to be accessed. Default is None, which means automatically
        find the private fields and create accessors for them. Each item can be a
        string (field name) or a ``(name, access_mode)`` tuple.
    :type items: Optional[Iterable[Union[str, Tuple[str, str]]]]
    :param readonly: Default readonly or not. Default is False, which means make
        the accessor writable when ``rw`` option is not given.
    :type readonly: bool
    :return: Decorator to decorate the given class.
    :rtype: Callable

    Example::

        >>> @accessor(readonly=True)
        >>> @asitems(['x', 'y'])
        >>> class T:
        ...     def __init__(self, x, y):
        ...         self.__x = x
        ...         self.__y = y
        >>> t = T(2, 100)
        >>> t.x  # 2
        2
        >>> t.y  # 100
        100

        With writable access::

        >>> @accessor(readonly=False)
        >>> @asitems(['x', 'y'])
        >>> class T2:
        ...     def __init__(self, x, y):
        ...         self.__x = x
        ...         self.__y = y
        >>> t = T2(2, 100)
        >>> t.x = 42
        >>> t.x
        42

        With mixed access control::

        >>> @accessor([('x', 'ro'), ('y', 'rw')])
        >>> class T3:
        ...     def __init__(self, x, y):
        ...         self.__x = x
        ...         self.__y = y
        >>> t = T3(1, 2)
        >>> t.y = 42  # OK
        >>> # t.x = 10  # This would raise AttributeError

    .. note::
        This decorator automatically generates property accessors for the
        specified fields. Access modes: ``'r'``/``'ro'``/``'readonly'`` for
        read-only, ``'w'``/``'rw'``/``'writable'`` for read-write.
    """

    def _decorator(cls: Type[Any]) -> Type[Any]:
        """
        Add property accessors to ``cls``.

        :param cls: Class to decorate.
        :type cls: type
        :return: The decorated class.
        :rtype: type
        """
        _cls_prefix = _cls_private_prefix(cls)

        if items is None:
            actual_items = _auto_get_items_from_cls(cls)
        elif isinstance(items, str):
            actual_items = [items]
        else:
            actual_items = items or []

        pitems = []
        for it in actual_items:
            if isinstance(it, str):
                itn, itv = it, ('ro' if readonly else 'rw')
            else:
                itn, itv = it

            itv = _is_writable(itv)
            pitems.append((itn, itv))

        for itn, itv in pitems:
            _getter_func_str = f"""
def get_{itn}(self):
{_INDENT}return self.{_cls_prefix}{itn}
            """
            fres = {}
            exec(_getter_func_str, fres)
            getter_func = fres[f'get_{itn}']
            getter_func = fassign(__doc__=f"""
            Property {itn}.

            .. note::
                Created by {_PACKAGE_RST}, v{__VERSION__}.

                {'Both reading and writing are' if itv else 'Only reading is'} \
                permitted with the accessor ``{itn}``.
            """)(getter_func)

            if itv:
                _setter_func_str = f"""
def set_{itn}(self, new_value):
{_INDENT}self.{_cls_prefix}{itn} = new_value
                """
                fres = {}
                exec(_setter_func_str, fres)
                setter_func = fres[f'set_{itn}']

                p = property(getter_func, setter_func)
            else:
                p = property(getter_func)

            setattr(cls, itn, p)

        return cls

    return _decorator
