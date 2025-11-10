"""
Overview:
    Implementation of singleton design pattern.
    
    This module provides metaclasses and utilities for implementing singleton patterns in Python.
    It includes:
    
    - :class:`SingletonMeta`: A metaclass for creating traditional singleton classes
    - :class:`ValueBasedSingletonMeta`: A metaclass for creating value-based singleton classes
    - :class:`SingletonMark`: A utility class for creating unique singleton marker objects
"""
__all__ = [
    'SingletonMeta',
    'ValueBasedSingletonMeta',
    'SingletonMark',
]


class SingletonMeta(type):
    """
    Meta class for singleton mode.

    This metaclass ensures that only one instance of a class is created throughout
    the application's lifetime. Subsequent calls to the class constructor will
    return the same instance.

    Example::
        >>> class MyService(metaclass=SingletonMeta):
        >>>     def get_value(self):
        >>>         return 233
        >>>
        >>> s = MyService()
        >>> s.get_value()    # 233
        >>> s1 = MyService()
        >>> s1 is s          # True

    .. note::

        In native singleton pattern, the constructor is not needed because \
        only one instance will be created in the whole lifetime. So when \
        :class:`SingletonMeta` is used as metaclass, please keep the constructor \
        be non-argument, or just ignore the ``__init__`` function.

    """
    _instances = {}

    def __call__(cls):
        """
        Override the call method to control instance creation.

        :return: The singleton instance of the class.
        :rtype: object
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__()
        return cls._instances[cls]


class ValueBasedSingletonMeta(type):
    """
    Meta class for value based singleton mode.

    This metaclass creates singleton instances based on a value parameter. 
    Multiple calls with the same value will return the same instance, while
    different values will create different instances.

    Example::
        >>> class MyData(metaclass=ValueBasedSingletonMeta):
        >>>     def __init__(self, value):
        >>>         self.__value = value
        >>>
        >>>     @property
        >>>     def value(self):
        >>>         return self.__value
        >>>
        >>> d1 = MyData(1)
        >>> d1.value       # 1
        >>> d2 = MyData(1)
        >>> d3 = MyData(2)
        >>> d2 is d1       # True
        >>> d2 is d3       # False

    .. note::

        This is an external case of singleton pattern. It can only contain one argument \
        (must be positional-supported), which differs from the native singleton case.

    """
    _instances = {}

    def __call__(cls, value):
        """
        Override the call method to control instance creation based on value.

        :param value: The value used as key for singleton instance lookup.
        :type value: Any hashable type
        :return: The singleton instance associated with the given value.
        :rtype: object
        """
        key = (cls, value)
        if key not in cls._instances:
            cls._instances[key] = super(ValueBasedSingletonMeta, cls).__call__(value)
        return cls._instances[key]


class SingletonMark(metaclass=ValueBasedSingletonMeta):
    """
    Singleton mark for some situation.
    
    Can be used when some default value is needed, especially when `None` has 
    meaning which is not default. This class creates unique marker objects that
    can be used as sentinel values.

    Example::
        >>> NO_VALUE = SingletonMark("no_value")
        >>> NO_VALUE is SingletonMark("no_value")  # True

    .. note::

        :class:`SingletonMark` is a value-based singleton class, can be used to create an unique \
        value, especially in the cases which ``None`` is not suitable for the default value.
    """

    def __init__(self, mark: str):
        """
        Constructor of :class:`SingletonMark`, can create a singleton mark object.

        :param mark: The string identifier for this mark.
        :type mark: str
        """
        self.__mark = mark

    @property
    def mark(self) -> str:
        """
        Get mark string of this mark object.

        :return: Mark string identifier.
        :rtype: str
        """
        return self.__mark

    def __hash__(self) -> int:
        """
        Compute hash value for the singleton mark.

        :class:`SingletonMark` objects are hash supported and can be directly used \
        in :class:`dict` and :class:`set`.

        :return: Hash value of the mark.
        :rtype: int
        """
        return hash(self.__mark)

    def __eq__(self, other) -> bool:
        """
        Compare equality between singleton marks.

        :class:`SingletonMark` objects can be directly compared with ``==``.

        :param other: The object to compare with.
        :type other: Any
        :return: True if marks are equal, False otherwise.
        :rtype: bool

        Examples::
            >>> mark1 = SingletonMark('mark1')
            >>> mark1x = SingletonMark('mark1')
            >>> mark2 = SingletonMark('mark2')
            >>> mark1 == mark1
            True
            >>> mark1 == mark1x
            True
            >>> mark1 == mark2
            False
        """
        if other is self:
            return True
        elif type(other) == type(self):
            return other.__mark == self.__mark
        else:
            return False

    def __repr__(self) -> str:
        """
        Return string representation of the singleton mark.

        When you try to print a :class:`SingletonMark` object, its mark content will be \
        displayed.

        :return: String representation of the mark.
        :rtype: str

        Examples::
            >>> mark1 = SingletonMark('mark1')
            >>> print(mark1)
            <SingletonMark 'mark1'>
        """
        return "<{cls} {mark}>".format(
            cls=self.__class__.__name__,
            mark=repr(self.__mark),
        )
