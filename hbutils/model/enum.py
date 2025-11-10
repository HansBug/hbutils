"""
Overview:
    Useful utilities for python enum class.
    
    This module provides utilities for working with Python enum classes, including:
    - AutoIntEnum: An IntEnum that automatically assigns sequential integer values
    - int_enum_loads: A decorator that adds a 'loads' method to IntEnum classes for flexible data parsing
"""
from enum import IntEnum, unique
from functools import lru_cache
from types import MethodType
from typing import Type, Optional, Callable, TypeVar, Any

__all__ = [
    'AutoIntEnum', 'int_enum_loads'
]


class AutoIntEnum(IntEnum):
    """
    Overview:
        An example from `official documentation <https://docs.python.org/3/library/enum.html#using-a-custom-new>`_.
        
        An IntEnum subclass that automatically assigns sequential integer values starting from 1.
        This allows you to define enum members with custom initialization values while the actual
        enum value is automatically assigned.

    Examples::
        >>> from hbutils.model import AutoIntEnum
        >>> class MyEnum(AutoIntEnum):
        ...     def __init__(self, v):
        ...         self.v = v
        ...     A = 'a_v'
        ...     B = 'b_vv'
        ...     C = 'c_vvv'
        ...
        >>> MyEnum.A
        <MyEnum.A: 1>
        >>> MyEnum.A.value
        1
        >>> MyEnum.A.v
        'a_v'
        >>> MyEnum.C
        <MyEnum.C: 3>
        >>> MyEnum.C.value
        3
        >>> MyEnum.C.v
        'c_vvv'
    """

    def __new__(cls, *args, **kwargs):
        """
        Create a new enum member with an automatically assigned sequential integer value.
        
        :param args: Arguments to pass to the enum member's __init__ method.
        :type args: tuple
        :param kwargs: Keyword arguments to pass to the enum member's __init__ method.
        :type kwargs: dict
        
        :return: A new enum member instance.
        :rtype: AutoIntEnum
        """
        value = len(cls.__members__) + 1
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj


_EnumType = TypeVar('_EnumType', bound=IntEnum)


def _default_value_preprocess(value: int) -> int:
    """
    Default preprocessor for integer values that returns the value unchanged.
    
    :param value: The integer value to preprocess.
    :type value: int
    
    :return: The unchanged integer value.
    :rtype: int
    """
    return value


def _default_name_preprocess(name: str) -> str:
    """
    Default preprocessor for string names that returns the name unchanged.
    
    :param name: The string name to preprocess.
    :type name: str
    
    :return: The unchanged string name.
    :rtype: str
    """
    return name


def _get_default_external_preprocess(enum_class: Type[_EnumType]) -> Callable:
    """
    Get the default external preprocessor that raises a TypeError for unknown types.
    
    :param enum_class: The enum class for which to create the preprocessor.
    :type enum_class: Type[_EnumType]
    
    :return: A function that raises TypeError for any input.
    :rtype: Callable
    """

    def _default_external_preprocess(data):
        """
        Raise a TypeError for data that cannot be processed.
        
        :param data: The data that failed to be processed.
        :type data: Any
        
        :raises TypeError: Always raised with information about the unknown type.
        """
        raise TypeError('Unknown type {type} for loads to {cls}.'.format(
            type=repr(type(data).__name__), cls=repr(enum_class.__name__),
        ))

    return _default_external_preprocess


def int_enum_loads(enable_int: bool = True, value_preprocess: Optional[Callable[[int, ], int]] = None,
                   enable_str: bool = True, name_preprocess: Optional[Callable[[str, ], str]] = None,
                   external_process: Optional[Callable[[Any, ], Optional[_EnumType]]] = None):
    """
    Overview:
        Decorate an IntEnum class with a new `loads` class method that provides flexible parsing
        of various data types into enum members. The decorator supports integer value parsing,
        string name parsing, and custom external processing for other data types.

    :param enable_int: Enable parsing from integer values, defaults to True.
    :type enable_int: bool
    :param value_preprocess: Preprocessor function for integer values before lookup, 
        defaults to None which means no preprocessing.
    :type value_preprocess: Optional[Callable[[int, ], int]]
    :param enable_str: Enable parsing from string names, defaults to True.
    :type enable_str: bool
    :param name_preprocess: Preprocessor function for string names before lookup,
        defaults to None which means no preprocessing.
    :type name_preprocess: Optional[Callable[[str, ], str]]
    :param external_process: External processor function for handling unprocessable data types,
        defaults to None which means raise a TypeError.
    :type external_process: Optional[Callable[[Any, ], Optional[_EnumType]]]
    
    :return: A decorator function that adds the loads method to an IntEnum class.
    :rtype: Callable[[Type[_EnumType]], Type[_EnumType]]
    
    :raises TypeError: If the decorated class is not a subclass of IntEnum.

    Examples:
        - Simple usage

        >>> from enum import IntEnum, unique
        >>>
        >>> @int_enum_loads()
        >>> @unique
        >>> class MyEnum(IntEnum):
        >>>     A = 1
        >>>     B = 2
        >>>
        >>> MyEnum.loads(1)    # MyEnum.A
        >>> MyEnum.loads('A')  # MyEnum.A
        >>> MyEnum.loads(2)    # MyEnum.B
        >>> MyEnum.loads('B')  # MyEnum.B
        >>> MyEnum.loads(-1)   # KeyError
        >>> MyEnum.loads('a')  # KeyError
        >>> MyEnum.loads('C')  # KeyError

        - Preprocessors

        >>> from enum import IntEnum, unique
        >>>
        >>> @int_enum_loads(name_preprocess=str.upper, value_preprocess=abs)
        >>> @unique
        >>> class MyEnum(IntEnum):
        >>>     A = 1
        >>>     B = 2
        >>>
        >>> MyEnum.loads(1)    # MyEnum.A
        >>> MyEnum.loads('A')  # MyEnum.A
        >>> MyEnum.loads(2)    # MyEnum.B
        >>> MyEnum.loads('B')  # MyEnum.B
        >>> MyEnum.loads(-1)   # MyEnum.A
        >>> MyEnum.loads('a')  # MyEnum.A
        >>> MyEnum.loads('C')  # KeyError

        - External processor

        >>> from enum import IntEnum, unique
        >>>
        >>> @int_enum_loads(external_process=lambda data: None)
        >>> @unique
        >>> class MyEnum(IntEnum):
        >>>     A = 1
        >>>     B = 2
        >>>
        >>> MyEnum.loads(1)    # MyEnum.A
        >>> MyEnum.loads('A')  # MyEnum.A
        >>> MyEnum.loads(2)    # MyEnum.B
        >>> MyEnum.loads('B')  # MyEnum.B
        >>> MyEnum.loads(-1)   # None
        >>> MyEnum.loads('a')  # None
        >>> MyEnum.loads('C')  # None
    """
    value_preprocess = value_preprocess or _default_value_preprocess
    name_preprocess = name_preprocess or _default_name_preprocess

    def _decorator(enum_class: Type[_EnumType]) -> Type[_EnumType]:
        """
        The actual decorator that adds the loads method to the enum class.
        
        :param enum_class: The IntEnum class to decorate.
        :type enum_class: Type[_EnumType]
        
        :return: The decorated enum class with the loads method added.
        :rtype: Type[_EnumType]
        
        :raises TypeError: If enum_class is not a subclass of IntEnum.
        """
        if not issubclass(enum_class, IntEnum):
            raise TypeError('Int enum expected but {type} found.'.format(type=repr(enum_class.__name__)))
        enum_class = unique(enum_class)

        @lru_cache()
        def _dict_item():
            """
            Get a cached dictionary of all enum members.
            
            :return: Dictionary mapping member names to member values.
            :rtype: dict
            """
            return {key: value for key, value in enum_class.__members__.items()}

        @lru_cache()
        def _int_value_to_item():
            """
            Get a cached dictionary mapping integer values to enum members.
            
            :return: Dictionary mapping integer values to enum members.
            :rtype: dict
            """
            return {value.value: value for _, value in _dict_item().items()}

        @lru_cache()
        def _str_name_to_item():
            """
            Get a cached dictionary mapping preprocessed string names to enum members.
            
            :return: Dictionary mapping preprocessed names to enum members.
            :rtype: dict
            """
            return {name_preprocess(key): value for key, value in _dict_item().items()}

        def _load_func(data) -> Optional[enum_class]:
            """
            Internal function to load enum data from raw data.
            
            :param data: Data to be parsed into an enum member.
            :type data: Any
            
            :return: The corresponding enum member, or result from external_process.
            :rtype: Optional[enum_class]
            
            :raises KeyError: If the data cannot be parsed and no external_process is provided.
            :raises TypeError: If the data type is not supported and no external_process is provided.
            """
            if isinstance(data, enum_class):
                return data
            elif enable_int and isinstance(data, int):
                return _int_value_to_item()[value_preprocess(data)]
            elif enable_str and isinstance(data, str):
                return _str_name_to_item()[name_preprocess(data)]
            else:
                return (external_process or _get_default_external_preprocess(enum_class))(data)

        def loads(cls, data) -> Optional[enum_class]:
            """
            Overview:
                Load enum data from raw data.

            :param data: Data which is going to be parsed.
            :type data: Any

            :return: Parsed enum data.
            :rtype: Optional[enum_class]
            
            :raises KeyError: If the data cannot be parsed and no external_process is provided.
            :raises TypeError: If the data type is not supported and no external_process is provided.
            """
            return _load_func(data)

        loads.__qualname__ = f'{enum_class.__qualname__}.{loads.__name__}'
        enum_class.loads = MethodType(loads, enum_class)
        return enum_class

    return _decorator
