"""
Final class enforcement utilities.

This module provides the :class:`FinalMeta` metaclass, which can be used to define
classes that cannot be subclassed. It is designed for situations where you want
to explicitly prevent inheritance to preserve a class's integrity or guarantee
certain behaviors remain unchanged.

The module contains the following main components:

* :class:`FinalMeta` - Metaclass that makes classes final (non-inheritable)

.. note::
   The inheritance check is performed at class definition time. Any attempt to
   subclass a final class raises a :exc:`TypeError`.

Example::

    >>> from hbutils.design.final import FinalMeta
    >>> class FinalClass(metaclass=FinalMeta):
    ...     pass
    ...
    >>> class TryToExtendFinalClass(FinalClass):
    ...     pass
    Traceback (most recent call last):
        ...
    TypeError: Type 'FinalClass' is a final class, which is not an acceptable common type.
"""

from typing import Any, Dict, Tuple

__all__ = ['FinalMeta']


class FinalMeta(type):
    """
    A metaclass for making a class final (unable to be extended by other classes).

    This metaclass prevents any class from inheriting from classes that use it as their metaclass.
    When a class attempts to inherit from a final class, a TypeError will be raised at class
    definition time.

    Example::
        >>> class FinalClass(metaclass=FinalMeta):  # this is a final class
        ...     pass
        ...
        >>> class TryToExtendFinalClass(FinalClass):  # TypeError will be raised at compile time
        ...     pass
        Traceback (most recent call last):
            ...
        TypeError: Type 'FinalClass' is a final class, which is not an acceptable common type.
    """

    def __new__(mcs: type, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]) -> type:
        """
        Create a new finalized class and validate that it doesn't inherit from any final classes.

        This method is called when a new class is being created. It checks all base classes
        to ensure none of them are final classes. If any base class is final, it raises
        a TypeError to prevent the inheritance.

        :param mcs: The metaclass itself (FinalMeta).
        :type mcs: type
        :param name: Name of the new class being created.
        :type name: str
        :param bases: Tuple of base classes for the new class.
        :type bases: Tuple[type, ...]
        :param attrs: Dictionary of attributes (methods and fields) for the new class.
        :type attrs: Dict[str, Any]

        :return: The newly created class object.
        :rtype: type

        :raises TypeError: If any base class is a final class (uses FinalMeta as metaclass).

        Example::
            >>> class FinalClass(metaclass=FinalMeta):  # this is a final class
            ...     pass
            ...
            >>> class TryToExtendFinalClass(FinalClass):  # TypeError will be raised at compile time
            ...     pass
            Traceback (most recent call last):
                ...
            TypeError: Type 'FinalClass' is a final class, which is not an acceptable common type.
        """
        for b in bases:
            if isinstance(b, FinalMeta):
                raise TypeError("Type {name} is a final class, which is not an acceptable common type."
                                .format(name=repr(b.__name__)))
        return type.__new__(mcs, name, bases, attrs)
