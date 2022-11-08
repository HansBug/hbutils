from typing import TypeVar, Type, List, Callable, Optional, Any, Dict

__all__ = [
    'BaseRecovery',
    'DictRecovery', 'ListRecovery', 'TupleRecovery',
    'NullRecovery', 'GenericObjectRecovery',
    'register_recovery', 'get_recovery_func',
]

_OriginType = TypeVar('_OriginType')


class BaseRecovery:
    __rtype__ = object

    def __init__(self, origin: _OriginType):
        """
        Constructor of :class:`BaseRecovery`.

        :param origin: Origin object to be recovered.
        """
        self.origin = origin

    def _recover(self):
        """
        Implementation for recovery.
        """
        raise NotImplementedError  # pragma: no cover

    def recover(self) -> _OriginType:
        """
        Recover the given object.

        :return: Recovered object.
        """
        self._recover()
        return self.origin

    @classmethod
    def _recover_child(cls, child):
        """
        Get recovered child-level object.

        :param child: Child object, should be a :class:`BaseRecovery` or native object.
        :return: Recovered child-level object.
        """
        if isinstance(child, BaseRecovery):
            return child.recover()
        else:
            return child

    @classmethod
    def from_origin(cls, origin: _OriginType, recursive: bool = True) -> 'BaseRecovery':
        """
        Create a recovery object by the given original object.

        :param origin: Original object to recover.
        :param recursive: Recursive or not. Default is ``True`` which means the child-level object \
            contained in ``origin`` will be recovered as well.
        :return: Recovery object.
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def _create_child(cls, child, recursive: bool = True):
        """
        Create child-level object for storage usage.

        :param child: Original child-level object.
        :param recursive: Recursive or not. Default is ``True`` which means the child-level object \
            contained in ``origin`` will be recovered as well.
        :return: Object for storage.
        """
        if recursive:
            clazz = _get_recovery_class(child)
            if clazz is not None:
                return clazz.from_origin(child, recursive)

        return child


_REC_CLASSES: Optional[List[Type[BaseRecovery]]] = None


def register_recovery(cls: Type[BaseRecovery]):
    """
    Overview:
        Register recovery class.

    :param cls: Recovery class.

    .. note::
        This API is used for customize recovery for other classes. \
        For more details, you may take a look at the source code of :class:`BaseRecovery`.
    """
    _REC_CLASSES.append(cls)


_DictType = TypeVar('_DictType', bound=dict)


class DictRecovery(BaseRecovery):
    __rtype__ = dict

    def __init__(self, origin: _DictType, mp: Dict):
        """
        Constructor of :class:`DictRecovery`.

        :param origin: Origin object to be recovered.
        """
        BaseRecovery.__init__(self, origin)
        self.mapping = mp

    def _recover(self):
        target = {
            key: self._recover_child(value)
            for key, value in self.mapping.items()
        }
        keys = set(self.origin.keys()) | set(target.keys())
        for key in keys:
            if key not in target:
                del self.origin[key]
            else:
                self.origin[key] = target[key]

    @classmethod
    def from_origin(cls, origin: _DictType, recursive: bool = True) -> 'DictRecovery':
        return cls(origin, {key: cls._create_child(value, recursive) for key, value in origin.items()})


_TupleType = TypeVar('_TupleType', bound=tuple)


class TupleRecovery(BaseRecovery):
    __rtype__ = tuple

    def __init__(self, origin: _TupleType, items: List[Any]):
        """
        Constructor of :class:`TupleRecovery`.

        :param origin: Origin object to be recovered.
        """
        BaseRecovery.__init__(self, origin)
        self.items = items

    def _recover(self):
        for item in self.items:
            self._recover_child(item)

    @classmethod
    def from_origin(cls, origin: _TupleType, recursive: bool = True) -> 'TupleRecovery':
        return cls(origin, [cls._create_child(item, recursive) for item in origin])


_ListType = TypeVar('_ListType', bound=list)


class ListRecovery(BaseRecovery):
    __rtype__ = list

    def __init__(self, origin: _ListType, items: List):
        """
        Constructor of :class:`ListRecovery`.

        :param origin: Origin object to be recovered.
        """
        BaseRecovery.__init__(self, origin)
        self.items = items

    def _recover(self):
        target = [
            self._recover_child(item)
            for item in self.items
        ]
        self.origin[:] = target

    @classmethod
    def from_origin(cls, origin: _ListType, recursive: bool = True) -> 'ListRecovery':
        return cls(origin, [cls._create_child(item, recursive) for item in origin])


class NullRecovery(BaseRecovery):
    """
    Overview:
        Empty recovery class for builtin immutable types.
    """
    __rtype__ = (int, float, str, bool, bytes, complex, range, slice)

    def _recover(self):
        """
        Just do nothing.
        """
        pass

    @classmethod
    def from_origin(cls, origin: _OriginType, recursive: bool = True) -> 'NullRecovery':
        """
        Just do nothing.
        """
        return cls(origin)


class GenericObjectRecovery(BaseRecovery):
    """
    Overview:
        Recovery class for generic objects.
        The ``__dict__`` will be recovered.

        .. note::
            If what you need to recover is not only ``__dict__``, may be you need to custom \
            recovery class by inheriting :class:`BaseRecovery` class, and register it by \
            :func:`register_recovery` function.
    """
    __rtype__ = object

    def __init__(self, origin: _OriginType, dict_: Optional['DictRecovery']):
        """
        Constructor of :class:`GenericObjectRecovery`.

        :param origin: Original object to recover.
        :param dict_: Recovery object of ``__dict__``, ``None`` when ``origin`` do not have ``__dict__``
        """
        BaseRecovery.__init__(self, origin)
        self.dict_ = dict_

    def _recover(self):
        """
        Recover the ``__dict__``.
        """
        if self.dict_ is not None:
            self.dict_.recover()

    @classmethod
    def from_origin(cls, origin: _OriginType, recursive: bool = True) -> 'BaseRecovery':
        """
        Create recovery object.
        """
        dict_ = DictRecovery.from_origin(origin.__dict__, recursive) if hasattr(origin, '__dict__') else None
        return cls(origin, dict_)


if _REC_CLASSES is None:
    _REC_CLASSES = []
    register_recovery(GenericObjectRecovery)
    register_recovery(NullRecovery)
    register_recovery(TupleRecovery)
    register_recovery(DictRecovery)
    register_recovery(ListRecovery)


def _get_recovery_class(origin: _OriginType) -> Optional[Type[BaseRecovery]]:
    for cls in reversed(_REC_CLASSES):
        if isinstance(origin, cls.__rtype__):
            return cls

    assert False, f'The object cannot be wrapped by recoveries - {origin!r}'  # pragma: no cover


def get_recovery_func(origin: _OriginType, recursive: bool = True) -> Callable[[], _OriginType]:
    """
    Overview:
        Get recovery function for given object.
        Dict, list and tuple object are natively supported.

    :param origin: Original object to recover.
    :param recursive: Recursive or not. Default is ``True`` which means the child-level object \
        contained in ``origin`` will be recovered as well.
    :return: Recovery function.

    Examples::
        >>> from hbutils.collection import get_recovery_func
        >>> l = [1, {'a': 1, 'b': 2}, 3, 4, 5]
        >>> print(id(l), l)
        140146367304720 [1, {'a': 1, 'b': 2}, 3, 4, 5]
        >>> f = get_recovery_func(l)

        >>> l[3] = 1
        >>> l.pop()
        >>> l.append('sdklfj')
        >>> l.append('sdkfhjksd')
        >>> l[1]['c'] = 2
        >>> l[1]['a'] = 100
        >>> print(id(l), l)
        140146367304720 [1, {'a': 100, 'b': 2, 'c': 2}, 3, 1, 'sdklfj', 'sdkfhjksd']

        >>> lx = f()
        >>> print(id(lx), lx)  # lx is l
        140146367304720 [1, {'a': 1, 'b': 2}, 3, 4, 5]
        >>> print(id(l), l)  # the value is recovered
        140146367304720 [1, {'a': 1, 'b': 2}, 3, 4, 5]

    """
    cls = _get_recovery_class(origin)
    return cls.from_origin(origin, recursive).recover
