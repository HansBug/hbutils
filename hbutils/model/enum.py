"""
Enum utilities for enhanced IntEnum usage.

This module provides helpers that extend standard :class:`enum.IntEnum` classes
with automatic value assignment and flexible parsing utilities. It includes:

* :class:`AutoIntEnum` - An :class:`enum.IntEnum` subclass that auto-assigns
  sequential integer values.
* :func:`int_enum_loads` - A decorator that adds a robust ``loads`` class method
  to :class:`enum.IntEnum` subclasses.

These tools are useful when you want clean, declarative enum definitions while
still supporting convenient parsing of values from integers, strings, or custom
types.

Example::

    >>> from enum import IntEnum, unique
    >>> from hbutils.model.enum import AutoIntEnum, int_enum_loads
    >>>
    >>> class Color(AutoIntEnum):
    ...     def __init__(self, code: str) -> None:
    ...         self.code = code
    ...     RED = "#ff0000"
    ...     BLUE = "#0000ff"
    >>>
    >>> Color.RED.value
    1
    >>> Color.RED.code
    '#ff0000'
    >>>
    >>> @int_enum_loads()
    >>> @unique
    ... class Status(IntEnum):
    ...     OK = 1
    ...     FAILED = 2
    >>>
    >>> Status.loads(1) is Status.OK
    True
    >>> Status.loads("FAILED") is Status.FAILED
    True

.. note::
   The ``loads`` method performs cached lookups, which is efficient for repeated
   parsing. Preprocessors can be used to normalize input values.

"""
from enum import IntEnum, unique
from functools import lru_cache
from types import MethodType
from typing import Type, Optional, Callable, TypeVar, Any, Dict

__all__ = [
    'AutoIntEnum', 'int_enum_loads'
]


class AutoIntEnum(IntEnum):
    """
    An :class:`enum.IntEnum` subclass with automatically assigned values.

    This class assigns sequential integer values starting from ``1`` to each
    enum member. You can still define custom initialization values via
    ``__init__`` while the underlying enum value is managed automatically.

    This implementation follows the official Python documentation example:
    https://docs.python.org/3/library/enum.html#using-a-custom-new

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

    def __new__(cls, *args: Any, **kwargs: Any) -> "AutoIntEnum":
        """
        Create a new enum member with an automatically assigned integer value.

        The value is assigned based on the number of existing members in the
        enum class. The actual initialization arguments are delegated to the
        enum member's ``__init__`` implementation.

        :param args: Positional arguments for ``__init__``.
        :type args: tuple
        :param kwargs: Keyword arguments for ``__init__``.
        :type kwargs: dict
        :return: The newly created enum instance.
        :rtype: AutoIntEnum
        """
        value = len(cls.__members__) + 1
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj


_EnumType = TypeVar('_EnumType', bound=IntEnum)


def _default_value_preprocess(value: int) -> int:
    """
    Default preprocessor for integer values.

    This function returns the given value unchanged.

    :param value: The integer value to preprocess.
    :type value: int
    :return: The preprocessed integer value.
    :rtype: int
    """
    return value


def _default_name_preprocess(name: str) -> str:
    """
    Default preprocessor for enum member names.

    This function returns the given name unchanged.

    :param name: The enum name to preprocess.
    :type name: str
    :return: The preprocessed name.
    :rtype: str
    """
    return name


def _get_default_external_preprocess(enum_class: Type[_EnumType]) -> Callable[[Any], Optional[_EnumType]]:
    """
    Get a default external processor that rejects unsupported types.

    The returned function raises a :class:`TypeError` when it is called.

    :param enum_class: The enum class to be referenced in the error message.
    :type enum_class: Type[_EnumType]
    :return: A function that raises :class:`TypeError` for any input.
    :rtype: Callable[[Any], Optional[_EnumType]]
    """

    def _default_external_preprocess(data: Any) -> Optional[_EnumType]:
        """
        Raise a :class:`TypeError` for unsupported data.

        :param data: The data that failed to be processed.
        :type data: Any
        :raises TypeError: Always raised with a message describing the type.
        """
        raise TypeError('Unknown type {type} for loads to {cls}.'.format(
            type=repr(type(data).__name__), cls=repr(enum_class.__name__),
        ))

    return _default_external_preprocess


def int_enum_loads(enable_int: bool = True,
                   value_preprocess: Optional[Callable[[int], int]] = None,
                   enable_str: bool = True,
                   name_preprocess: Optional[Callable[[str], str]] = None,
                   external_process: Optional[Callable[[Any], Optional[_EnumType]]] = None
                   ) -> Callable[[Type[_EnumType]], Type[_EnumType]]:
    """
    Decorate an :class:`enum.IntEnum` class with a ``loads`` class method.

    The resulting ``loads`` method supports:

    * Direct enum member passthrough
    * Integer value lookups (optionally preprocessed)
    * String name lookups (optionally preprocessed)
    * Custom external processing for other types

    :param enable_int: Whether to allow integer parsing, defaults to ``True``.
    :type enable_int: bool
    :param value_preprocess: Preprocessor for integer values prior to lookup.
        If ``None``, the identity function is used.
    :type value_preprocess: Optional[Callable[[int], int]]
    :param enable_str: Whether to allow string name parsing, defaults to ``True``.
    :type enable_str: bool
    :param name_preprocess: Preprocessor for string names prior to lookup.
        If ``None``, the identity function is used.
    :type name_preprocess: Optional[Callable[[str], str]]
    :param external_process: Handler for unrecognized data types.
        If ``None``, a :class:`TypeError` is raised.
    :type external_process: Optional[Callable[[Any], Optional[_EnumType]]]
    :return: A decorator that enhances an :class:`enum.IntEnum` class.
    :rtype: Callable[[Type[_EnumType]], Type[_EnumType]]
    :raises TypeError: If the decorated class is not a subclass of
        :class:`enum.IntEnum`.

    Examples:

        - Simple usage::

            >>> from enum import IntEnum, unique
            >>>
            >>> @int_enum_loads()
            >>> @unique
            ... class MyEnum(IntEnum):
            ...     A = 1
            ...     B = 2
            >>>
            >>> MyEnum.loads(1)    # MyEnum.A
            >>> MyEnum.loads('A')  # MyEnum.A
            >>> MyEnum.loads(2)    # MyEnum.B
            >>> MyEnum.loads('B')  # MyEnum.B
            >>> MyEnum.loads(-1)   # KeyError
            >>> MyEnum.loads('a')  # KeyError
            >>> MyEnum.loads('C')  # KeyError

        - Preprocessors::

            >>> from enum import IntEnum, unique
            >>>
            >>> @int_enum_loads(name_preprocess=str.upper, value_preprocess=abs)
            >>> @unique
            ... class MyEnum(IntEnum):
            ...     A = 1
            ...     B = 2
            >>>
            >>> MyEnum.loads(1)    # MyEnum.A
            >>> MyEnum.loads('A')  # MyEnum.A
            >>> MyEnum.loads(2)    # MyEnum.B
            >>> MyEnum.loads('B')  # MyEnum.B
            >>> MyEnum.loads(-1)   # MyEnum.A
            >>> MyEnum.loads('a')  # MyEnum.A
            >>> MyEnum.loads('C')  # KeyError

        - External processor::

            >>> from enum import IntEnum, unique
            >>>
            >>> @int_enum_loads(external_process=lambda data: None)
            >>> @unique
            ... class MyEnum(IntEnum):
            ...     A = 1
            ...     B = 2
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
        Add a ``loads`` method to the given enum class.

        :param enum_class: The enum class to be decorated.
        :type enum_class: Type[_EnumType]
        :return: The same class with an added ``loads`` method.
        :rtype: Type[_EnumType]
        :raises TypeError: If ``enum_class`` is not a subclass of
            :class:`enum.IntEnum`.
        """
        if not issubclass(enum_class, IntEnum):
            raise TypeError('Int enum expected but {type} found.'.format(type=repr(enum_class.__name__)))
        enum_class = unique(enum_class)

        @lru_cache()
        def _dict_item() -> Dict[str, _EnumType]:
            """
            Get a cached mapping of member names to enum members.

            :return: Mapping of enum names to members.
            :rtype: dict
            """
            return {key: value for key, value in enum_class.__members__.items()}

        @lru_cache()
        def _int_value_to_item() -> Dict[int, _EnumType]:
            """
            Get a cached mapping of integer values to enum members.

            :return: Mapping of integer values to members.
            :rtype: dict
            """
            return {value.value: value for _, value in _dict_item().items()}

        @lru_cache()
        def _str_name_to_item() -> Dict[str, _EnumType]:
            """
            Get a cached mapping of preprocessed names to enum members.

            :return: Mapping of preprocessed names to members.
            :rtype: dict
            """
            return {name_preprocess(key): value for key, value in _dict_item().items()}

        def _load_func(data: Any) -> Optional[_EnumType]:
            """
            Internal loader function used by ``loads``.

            :param data: Input data to parse.
            :type data: Any
            :return: The matching enum member or the result of ``external_process``.
            :rtype: Optional[_EnumType]
            :raises KeyError: If lookup fails and no external handler returns a value.
            :raises TypeError: If an unsupported type is provided and no external handler is set.
            """
            if isinstance(data, enum_class):
                return data
            elif enable_int and isinstance(data, int):
                return _int_value_to_item()[value_preprocess(data)]
            elif enable_str and isinstance(data, str):
                return _str_name_to_item()[name_preprocess(data)]
            else:
                return (external_process or _get_default_external_preprocess(enum_class))(data)

        def loads(cls: Type[_EnumType], data: Any) -> Optional[_EnumType]:
            """
            Load an enum member from raw data.

            :param data: Input data to be parsed.
            :type data: Any
            :return: The parsed enum member or the external handler's result.
            :rtype: Optional[_EnumType]
            :raises KeyError: If lookup fails and no external handler returns a value.
            :raises TypeError: If an unsupported type is provided and no external handler is set.
            """
            return _load_func(data)

        loads.__qualname__ = f'{enum_class.__qualname__}.{loads.__name__}'
        enum_class.loads = MethodType(loads, enum_class)
        return enum_class

    return _decorator
