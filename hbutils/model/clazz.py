"""
Overview:
    Useful functions for build class models.
"""
import os
import textwrap
from typing import Optional, Iterable

from ._info import _PACKAGE_RST
from ..config.meta import __VERSION__
from ..design.singleton import SingletonMark
from ..reflection import fassign

__all__ = [
    'get_field',
    'asitems', 'visual', 'constructor', 'hasheq', 'accessor',
]

CLASS_WRAPPER_UPDATES = ()


def _cls_field_name(cls: type, name: str):
    if name.startswith('__'):
        return f'_{cls.__name__.lstrip("_")}__{name[2:]}'
    else:
        return name


_NO_DEFAULT_VALUE = SingletonMark('no_default_value')


def get_field(obj, name: str, default=_NO_DEFAULT_VALUE):
    """
    Overview:
        Get field from object.
        Private field is supported.

    :param obj: The given object.
    :param name: Field to be got.
    :param default: Default value when failed.
    :return: Field value of the field.
    """
    _field_name = _cls_field_name(type(obj), name)
    if default is _NO_DEFAULT_VALUE:
        return getattr(obj, _field_name)
    else:
        return getattr(obj, _field_name, default)


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
        >>>         return self.__first
        >>>
        >>>     @property
        >>>     def y(self):
        >>>         return self.__second
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
        ...         self.__first = x
        ...         self.__second = y
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
            f"""
            Get representation format of class {cls.__name__}.

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
        >>>         return self.__first
        >>>
        >>>     @property
        >>>     def y(self):
        >>>         return self.__second
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
        >>>         self.__first = x
        >>>         self.__second = y

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
            f"""
            Hash value of class {cls.__name__}'s instances.

            .. note::
                Created by {_PACKAGE_RST}, v{__VERSION__}.

                The return value is calculated based on the \
                values of the internally specified fields.
            """
            return hash(_get_obj_values(self))

        def __eq__(self, other):
            f"""
            Equality between class {cls.__name__}'s instances.

            .. note::
                Created by {_PACKAGE_RST}, v{__VERSION__}.

                Currently, the return value is True only if both objects \\
                are of class {cls.__name__} (subclasses are not permitted) and the \\
                values of the internally specified fields are all equal; \\
                otherwise, it is always False.
            """
            if self is other:
                return True
            elif type(self) == type(other):
                return _get_obj_values(self) == _get_obj_values(other)
            else:
                return False

        def __ne__(self, other):
            f"""
            Non-equality between class {cls.__name__}'s instances.

            .. note::
                Created by {_PACKAGE_RST}, v{__VERSION__}.

                Currently, the return value is False only if both objects \\
                are of class {cls.__name__} (subclasses are not permitted) and the \\
                values of the internally specified fields are all equal; \\
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


def _is_writable(mark: str):
    if mark.lower() in _READONLY_MARKS:
        return False
    elif mark.lower() in _WRITABLE_MARKS:
        return True
    else:
        raise ValueError(f'Unknown accessible mark - {repr(mark)}.')


def accessor(items: Optional[Iterable] = None, readonly: bool = False):
    """
    Overview:
        Decorate class to be accessible by the accessors.

    Arguments:
        - items (:obj:`Optional[Iterable]`): Items to be hashed and compared. Default is `None`, \
            which means automatically find the private fields and display them.
        - readonly (:obj:`bool`): Default readonly or not. Default is `False`, which means make \
            the accessor be writable when ``rw`` option is not given.

    Returns:
        - decorator: Decorator to decorate the given class.

    Examples::
        >>> @accessor(readonly=True)
        >>> @asitems(['x', 'y'])
        >>> class T:
        >>>     def __init__(self, x, y):
        >>>         self.__first = x
        >>>         self.__second = y
        >>>
        >>> t = T(2, 100)
        >>> t.x  # 2
        >>> t.y  # 100
    """

    def _decorator(cls):
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

                {'Both reading and writing are' if itv else 'Only reading is'} \\
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
