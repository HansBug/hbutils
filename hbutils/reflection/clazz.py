"""
Overview:
    Useful functions for processing python classes and types.
"""
import os
from functools import WRAPPER_ASSIGNMENTS as CLASS_WRAPPER_ASSIGNMENTS
from functools import update_wrapper, partial
from typing import Tuple, Optional, Iterable

from .func import fassign
from ..design.singleton import SingletonMark

__all__ = [
    'class_wraps',
    'asitems', 'visual', 'constructor', 'hasheq',
]

CLASS_WRAPPER_UPDATES = ()


def class_wraps(wrapped: type,
                assigned: Tuple[str] = CLASS_WRAPPER_ASSIGNMENTS,
                updated: Tuple[str] = CLASS_WRAPPER_UPDATES):
    r"""
    Overview:
        Wrapper decorator for class.

    Arguments:
        - wrapped (:obj:`type`): Wrapped class.
        - assigned (:obj:`Tuple[str]`): Wrapper assignments, equal to :func:`functools.wraps`'s \
            ``WRAPPER_ASSIGNMENTS``.
        - updated (:obj:`Tuple[str]`): Wrapper updates, default is ``()``, no update will be done.

    Examples:
        >>> def cls_dec(clazz):
        >>>     @class_wraps(clazz)
        >>>     class _NewClazz(clazz):
        >>>         pass
        >>>
        >>>     return _NewClazz
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)


def _cls_private_prefix(cls):
    cls_name = cls.__name__.lstrip('_')
    return f'_{cls_name}__'


def _auto_get_items_from_cls(cls):
    return cls.__items__


def _auto_get_items(obj, cls_prefix=None):
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


def _get_value(self, vname: str, cls_prefix=None):
    cls_prefix = cls_prefix or _cls_private_prefix(type(self))
    try:
        return getattr(self, vname)
    except AttributeError:
        return getattr(self, cls_prefix + vname)


def asitems(items: Iterable[str]):
    """
    Overview:
        Define fields in the class level.

    Arguments:
        - items (:obj:`Iterable[str]`): Field name items.

    Returns:
        - decorator: Decorator to decorate the given class.

    Examples::
        >>> @visual()
        >>> @constructor(doc='''
        >>>     Overview:
        >>>         This is the constructor of class :class:`T`.
        >>> ''')
        >>> @asitems(['x', 'y'])
        >>> class T:
        >>>     @property
        >>>     def x(self):
        >>>         return self.__x
        >>>
        >>>     @property
        >>>     def y(self):
        >>>         return self.__y
    """

    def _decorator(cls):
        _cls_prefix = _cls_private_prefix(cls)
        cls.__items__ = list(items)
        return cls

    return _decorator


def visual(items: Optional[Iterable] = None, show_id: bool = False):
    """
    Overview:
        Decorate class to be visible by `repr`.

    Arguments:
        - items (:obj:`Optional[Iterable]`): Items to be displayed. Default is `None`, which means \
            automatically find the private fields and display them.
        - show_id (:obj:`bool`): Show hex id in representation string or not.

    Returns:
        - decorator: Decorator to decorate the given class.

    Examples::
        >>> @visual()
        >>> class T:
        ...     def __init__(self, x, y):
        ...         self.__x = x
        ...         self.__y = y
        >>> repr(T(1, 2))
        <T x: 1, y: 2>
    """

    def _decorator(cls):
        _cls_prefix = _cls_private_prefix(cls)

        def _get_items(self):
            if items is None:
                return _auto_get_items(self, _cls_prefix)
            else:
                return items

        def __repr__(self):
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


_NO_DEFAULT_VALUE = SingletonMark('no_default_value')
_INDENT = ' ' * 4


def constructor(params: Optional[Iterable] = None, doc: Optional[str] = None):
    r"""
    Overview:
        Decorate class to create a init function.
    
    Arguments:
        - params (:obj:`Optional[Iterable]`): Parameters of constructor, should be a iterator of items, \
            each item should be a single string or a tuple of string and default value. Default is `None`, \
            which means no arguments.
        - doc (:obj:`Optional[str]`): Documentation of constructor function.

    Returns:
        - decorator: Decorator to decorate the given class.

    Examples::
        >>> @constructor(['x', ('y', 2)], '''
        >>>     Overview:
        >>>         This is the constructor of class :class:`T`.
        >>> ''')
        >>> class T:
        >>>     # the same as:
        >>>     # def __init__(self, x, y=2):
        >>>     #     self.__x = x
        >>>     #     self.__y = y
        >>>
        >>>     @property
        >>>     def x(self):
        >>>         return self.__x
        >>>
        >>>     @property
        >>>     def y(self):
        >>>         return self.__y
    """

    def _decorator(cls):
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
        _init_func = fassign(__doc__=doc)(_init_func)
        cls.__init__ = _init_func

        return cls

    return _decorator


def hasheq(items: Optional[Iterable] = None):
    """
    Overview:
        Decorate class to be visible by `repr`.

    Arguments:
        - items (:obj:`Optional[Iterable]`): Items to be hashed and compared. Default is `None`, \
            which means automatically find the private fields and display them.

    Returns:
        - decorator: Decorator to decorate the given class.

    Examples::
        >>> @hasheq(['x', 'y'])
        >>> class T:
        >>>     def __init__(self, x, y):
        >>>         self.__x = x
        >>>         self.__y = y

        Using with :func:`asitems`

        >>> @hasheq()
        >>> @constructor()
        >>> @asitems(['x', 'y'])
        >>> class T1:
        >>>     pass
    """

    def _decorator(cls):
        _cls_prefix = _cls_private_prefix(cls)

        def _get_items(self):
            if items is None:
                return _auto_get_items(self, _cls_prefix)
            else:
                return items

        def _get_obj_values(self):
            return tuple(_get_value(self, name, _cls_prefix) for name in _get_items(self))

        def __hash__(self):
            return hash(_get_obj_values(self))

        def __eq__(self, other):
            if self is other:
                return True
            elif type(self) == type(other):
                return _get_obj_values(self) == _get_obj_values(other)
            else:
                return False

        cls.__hash__ = __hash__
        cls.__eq__ = __eq__

        return cls

    return _decorator
