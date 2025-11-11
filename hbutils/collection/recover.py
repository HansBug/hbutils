"""
This module provides a flexible recovery system for Python objects, allowing objects to be restored to their original state after modifications.

The recovery system supports various built-in types (dict, list, tuple, etc.) and can be extended to support custom types through registration. It works by creating recovery objects that store the original state and can restore it when needed.

Key Features:
    - Recursive recovery of nested data structures
    - Support for built-in types (dict, list, tuple, primitives)
    - Extensible through custom recovery classes
    - Generic object recovery via __dict__ attribute

Example::
    >>> from hbutils.collection import get_recovery_func
    >>> l = [1, {'a': 1, 'b': 2}, 3, 4, 5]
    >>> f = get_recovery_func(l)
    >>> l[3] = 1
    >>> l.pop()
    >>> recovered = f()  # Restores original state
"""

from typing import TypeVar, Type, List, Callable, Optional, Any, Dict

__all__ = [
    'BaseRecovery',
    'DictRecovery', 'ListRecovery', 'TupleRecovery',
    'NullRecovery', 'GenericObjectRecovery',
    'register_recovery', 'get_recovery_func',
]

_OriginType = TypeVar('_OriginType')


class BaseRecovery:
    """
    Base class for all recovery implementations.
    
    This abstract class defines the interface for recovery objects that can restore
    Python objects to their original state. Subclasses should implement the ``_recover``
    and ``from_origin`` methods to provide specific recovery logic for different types.
    
    :ivar __rtype__: The type(s) that this recovery class can handle.
    :type __rtype__: type or tuple of types
    :ivar origin: The original object to be recovered.
    :type origin: _OriginType
    """
    __rtype__ = object

    def __init__(self, origin: _OriginType):
        """
        Constructor of :class:`BaseRecovery`.

        :param origin: Origin object to be recovered.
        :type origin: _OriginType
        """
        self.origin = origin

    def _recover(self):
        """
        Implementation for recovery.
        
        This method should be overridden by subclasses to provide the actual
        recovery logic for restoring the object to its original state.
        
        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover

    def recover(self) -> _OriginType:
        """
        Recover the given object.

        This method calls the internal ``_recover`` method to perform the actual
        recovery operation and then returns the recovered object.

        :return: Recovered object.
        :rtype: _OriginType
        """
        self._recover()
        return self.origin

    @classmethod
    def _recover_child(cls, child):
        """
        Get recovered child-level object.

        This method handles the recovery of child objects, which may themselves
        be recovery objects or native Python objects.

        :param child: Child object, should be a :class:`BaseRecovery` or native object.
        :type child: Union[BaseRecovery, Any]
        :return: Recovered child-level object.
        :rtype: Any
        """
        if isinstance(child, BaseRecovery):
            return child.recover()
        else:
            return child

    @classmethod
    def from_origin(cls, origin: _OriginType, recursive: bool = True) -> 'BaseRecovery':
        """
        Create a recovery object by the given original object.

        This method should be overridden by subclasses to create an appropriate
        recovery object for the given original object.

        :param origin: Original object to recover.
        :type origin: _OriginType
        :param recursive: Recursive or not. Default is ``True`` which means the child-level object \
            contained in ``origin`` will be recovered as well.
        :type recursive: bool
        :return: Recovery object.
        :rtype: BaseRecovery
        :raises NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def _create_child(cls, child, recursive: bool = True):
        """
        Create child-level object for storage usage.

        This method determines whether to create a recovery object for a child
        element or store it directly, based on the recursive flag.

        :param child: Original child-level object.
        :type child: Any
        :param recursive: Recursive or not. Default is ``True`` which means the child-level object \
            contained in ``origin`` will be recovered as well.
        :type recursive: bool
        :return: Object for storage (either a recovery object or the original child).
        :rtype: Union[BaseRecovery, Any]
        """
        if recursive:
            clazz = _get_recovery_class(child)
            if clazz is not None:
                return clazz.from_origin(child, recursive)

        return child


_REC_CLASSES: Optional[List[Type[BaseRecovery]]] = None


def register_recovery(cls: Type[BaseRecovery]):
    """
    Register recovery class.

    This function registers a custom recovery class to the global registry,
    allowing it to be used for recovering objects of the types specified in
    the class's ``__rtype__`` attribute.

    :param cls: Recovery class to register.
    :type cls: Type[BaseRecovery]

    .. note::
        This API is used for customize recovery for other classes. \
        For more details, you may take a look at the source code of :class:`BaseRecovery`.
    """
    _REC_CLASSES.append(cls)


_DictType = TypeVar('_DictType', bound=dict)


class DictRecovery(BaseRecovery):
    """
    Recovery class for dictionary objects.
    
    This class handles the recovery of dictionary objects by storing their
    key-value pairs and restoring them when recovery is triggered.
    
    :ivar mapping: Dictionary mapping of keys to values (or recovery objects).
    :type mapping: Dict
    """
    __rtype__ = dict

    def __init__(self, origin: _DictType, mp: Dict):
        """
        Constructor of :class:`DictRecovery`.

        :param origin: Origin object to be recovered.
        :type origin: _DictType
        :param mp: Dictionary mapping of keys to values or recovery objects.
        :type mp: Dict
        """
        BaseRecovery.__init__(self, origin)
        self.mapping = mp

    def _recover(self):
        """
        Recover the dictionary to its original state.
        
        This method restores all key-value pairs in the dictionary, removing
        any keys that were added and restoring original values.
        """
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
        """
        Create a DictRecovery object from a dictionary.
        
        :param origin: Original dictionary to recover.
        :type origin: _DictType
        :param recursive: Whether to recursively create recovery objects for values.
        :type recursive: bool
        :return: DictRecovery object.
        :rtype: DictRecovery
        """
        return cls(origin, {key: cls._create_child(value, recursive) for key, value in origin.items()})


_TupleType = TypeVar('_TupleType', bound=tuple)


class TupleRecovery(BaseRecovery):
    """
    Recovery class for tuple objects.
    
    Since tuples are immutable, this class primarily handles recovery of
    mutable objects contained within the tuple.
    
    :ivar items: List of items (or recovery objects) in the tuple.
    :type items: List[Any]
    """
    __rtype__ = tuple

    def __init__(self, origin: _TupleType, items: List[Any]):
        """
        Constructor of :class:`TupleRecovery`.

        :param origin: Origin object to be recovered.
        :type origin: _TupleType
        :param items: List of items or recovery objects from the tuple.
        :type items: List[Any]
        """
        BaseRecovery.__init__(self, origin)
        self.items = items

    def _recover(self):
        """
        Recover the tuple's contained objects.
        
        Since tuples are immutable, this method only recovers the mutable
        objects contained within the tuple.
        """
        for item in self.items:
            self._recover_child(item)

    @classmethod
    def from_origin(cls, origin: _TupleType, recursive: bool = True) -> 'TupleRecovery':
        """
        Create a TupleRecovery object from a tuple.
        
        :param origin: Original tuple to recover.
        :type origin: _TupleType
        :param recursive: Whether to recursively create recovery objects for items.
        :type recursive: bool
        :return: TupleRecovery object.
        :rtype: TupleRecovery
        """
        return cls(origin, [cls._create_child(item, recursive) for item in origin])


_ListType = TypeVar('_ListType', bound=list)


class ListRecovery(BaseRecovery):
    """
    Recovery class for list objects.
    
    This class handles the recovery of list objects by storing their
    elements and restoring them when recovery is triggered.
    
    :ivar items: List of items (or recovery objects) from the original list.
    :type items: List
    """
    __rtype__ = list

    def __init__(self, origin: _ListType, items: List):
        """
        Constructor of :class:`ListRecovery`.

        :param origin: Origin object to be recovered.
        :type origin: _ListType
        :param items: List of items or recovery objects from the original list.
        :type items: List
        """
        BaseRecovery.__init__(self, origin)
        self.items = items

    def _recover(self):
        """
        Recover the list to its original state.
        
        This method restores all elements in the list, replacing the current
        contents with the original elements.
        """
        target = [
            self._recover_child(item)
            for item in self.items
        ]
        self.origin[:] = target

    @classmethod
    def from_origin(cls, origin: _ListType, recursive: bool = True) -> 'ListRecovery':
        """
        Create a ListRecovery object from a list.
        
        :param origin: Original list to recover.
        :type origin: _ListType
        :param recursive: Whether to recursively create recovery objects for items.
        :type recursive: bool
        :return: ListRecovery object.
        :rtype: ListRecovery
        """
        return cls(origin, [cls._create_child(item, recursive) for item in origin])


class NullRecovery(BaseRecovery):
    """
    Empty recovery class for builtin immutable types.
    
    This class is used for immutable types that cannot be modified and
    therefore do not need any recovery logic. It simply stores a reference
    to the original object.
    """
    __rtype__ = (int, float, str, bool, bytes, complex, range, slice)

    def _recover(self):
        """
        Just do nothing.
        
        Immutable types do not need recovery as they cannot be modified.
        """
        pass

    @classmethod
    def from_origin(cls, origin: _OriginType, recursive: bool = True) -> 'NullRecovery':
        """
        Just do nothing.
        
        Create a NullRecovery object for an immutable type.
        
        :param origin: Original immutable object.
        :type origin: _OriginType
        :param recursive: Ignored for immutable types.
        :type recursive: bool
        :return: NullRecovery object.
        :rtype: NullRecovery
        """
        return cls(origin)


class GenericObjectRecovery(BaseRecovery):
    """
    Recovery class for generic objects.
    
    The ``__dict__`` will be recovered.

    This class provides recovery for arbitrary Python objects by storing
    and restoring their ``__dict__`` attribute. This works for most custom
    classes but may not be sufficient for objects with special state storage.

    :ivar dict_: Recovery object for the object's __dict__, or None if no __dict__ exists.
    :type dict_: Optional[DictRecovery]

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
        :type origin: _OriginType
        :param dict_: Recovery object of ``__dict__``, ``None`` when ``origin`` do not have ``__dict__``.
        :type dict_: Optional[DictRecovery]
        """
        BaseRecovery.__init__(self, origin)
        self.dict_ = dict_

    def _recover(self):
        """
        Recover the ``__dict__``.
        
        This method restores the object's ``__dict__`` attribute to its
        original state if it exists.
        """
        if self.dict_ is not None:
            self.dict_.recover()

    @classmethod
    def from_origin(cls, origin: _OriginType, recursive: bool = True) -> 'BaseRecovery':
        """
        Create recovery object.
        
        Creates a GenericObjectRecovery by storing the object's ``__dict__``
        if it exists.
        
        :param origin: Original object to recover.
        :type origin: _OriginType
        :param recursive: Whether to recursively create recovery objects for __dict__ values.
        :type recursive: bool
        :return: GenericObjectRecovery object.
        :rtype: GenericObjectRecovery
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
    """
    Get the appropriate recovery class for a given object.
    
    This function searches through registered recovery classes to find
    the most specific one that can handle the given object type.
    
    :param origin: Object to find a recovery class for.
    :type origin: _OriginType
    :return: Recovery class that can handle the object, or None if not found.
    :rtype: Optional[Type[BaseRecovery]]
    :raises AssertionError: If no recovery class can handle the object.
    """
    for cls in reversed(_REC_CLASSES):
        if isinstance(origin, cls.__rtype__):
            return cls

    assert False, f'The object cannot be wrapped by recoveries - {origin!r}'  # pragma: no cover


def get_recovery_func(origin: _OriginType, recursive: bool = True) -> Callable[[], _OriginType]:
    """
    Get recovery function for given object.
    
    Dict, list and tuple object are natively supported.

    This function creates a recovery object for the given object and returns
    a callable that will restore the object to its original state when invoked.

    :param origin: Original object to recover.
    :type origin: _OriginType
    :param recursive: Recursive or not. Default is ``True`` which means the child-level object \
        contained in ``origin`` will be recovered as well.
    :type recursive: bool
    :return: Recovery function that restores the object when called.
    :rtype: Callable[[], _OriginType]

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
