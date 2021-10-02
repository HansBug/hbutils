"""
Overview:
    Implement of singleton design pattern.
"""
__all__ = [
    'SingletonMeta',
    'ValueBasedSingletonMeta',
    'SingletonMark',
]


class SingletonMeta(type):
    """
    Overview:
        Meta class for singleton mode.

    Example:
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
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__()
        return cls._instances[cls]


class ValueBasedSingletonMeta(type):
    """
    Overview:
        Meta class for value based singleton mode.

    Example:
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
        key = (cls, value)
        if key not in cls._instances:
            cls._instances[key] = super(ValueBasedSingletonMeta, cls).__call__(value)
        return cls._instances[key]


class SingletonMark(metaclass=ValueBasedSingletonMeta):
    """
    Overview:
        Singleton mark for some situation.
        Can be used when some default value is needed, especially when `None` has meaning which is not default.

    Example:
        >>> NO_VALUE = SingletonMark("no_value")
        >>> NO_VALUE is SingletonMark("no_value")  # True

    .. note::

        :class:`SingletonMark` is a value-based singleton class, can be used to create an unique \
        value, especially in the cases which ``None`` is not suitable for the default value.
    """

    def __init__(self, mark):
        """
        Overview:
            Constructor of :class:`SingletonMark`, can create a singleton mark object.
        """
        self.__mark = mark

    @property
    def mark(self):
        """
        Overview:
            Get mark string of this mark object.

        Returns:
            - mark (:obj:`str`): Mark string
        """
        return self.__mark

    def __hash__(self):
        """
        Overview:
            :class:`SingletonMark` objects are hash supported. can be directly used \
            in :class:`dict` and :class:`set`.
        """
        return hash(self.__mark)

    def __eq__(self, other):
        """
        Overview:
            :class:`SingletonMark` objects can be directly compared with ``==``.

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

    def __repr__(self):
        """
        Overview:
            When you try to print a :class:`SingletonMark` object, its mark content will be \
            displayed.

        Examples::
            >>> mark1 = SingletonMark('mark1')
            >>> print(mark1)
            <SingletonMark mark1>
        """
        return "<{cls} {mark}>".format(
            cls=self.__class__.__name__,
            mark=repr(self.__mark),
        )
