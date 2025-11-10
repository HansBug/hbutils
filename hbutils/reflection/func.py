"""
Overview:
    Useful functions for processing python functions.
    
    This module provides a collection of utility functions and decorators for manipulating,
    inspecting, and transforming Python functions. It includes tools for:
    
    - Function attribute manipulation (fassign, frename, fcopy)
    - Argument processing and iteration (args_iter, sigsupply)
    - Dynamic and static function calling (dynamic_call, static_call)
    - Function pre/post processing (pre_process, post_process)
    - Exception and warning handling (raising, warning_)
    - Function reduction (freduce)
    - Type hint extraction (get_callable_hint)
"""
import warnings
from functools import wraps
from inspect import signature, Parameter
from itertools import chain
from typing import Callable, TypeVar, Union, Type, get_type_hints, Any

from ..design import SingletonMark, decolize

__all__ = [
    'fassign', 'frename', 'fcopy',
    'args_iter', 'sigsupply',
    'dynamic_call', 'static_call',
    'pre_process', 'post_process',
    'raising', 'warning_',
    'freduce',
    'get_callable_hint',
]


def fassign(**assigns):
    """
    Do assignments to function attributes.
    
    This decorator allows you to assign arbitrary attributes to a function object.
    It's useful for adding metadata or custom properties to functions.

    :param assigns: Keyword arguments representing attribute names and their values to assign.
    :type assigns: Any
    
    :return: A decorator function that assigns the specified attributes to the target function.
    :rtype: Callable
    
    Examples::
    
        >>> @fassign(__name__='fff')
        >>> def func(a, b):
        >>>     return a + b
        >>> func.__name__
        'fff'
    """

    def _decorator(func):
        for k, v in assigns.items():
            setattr(func, k, v)

        return func

    return _decorator


def frename(new_name: str):
    """
    Rename the given function.
    
    This decorator changes the ``__name__`` attribute of a function to the specified new name.

    :param new_name: New name of function.
    :type new_name: str
    
    :return: Decorator to rename the function.
    :rtype: Callable
    
    Examples::
    
        >>> @frename('fff')
        >>> def func(a, b):
        >>>     return a + b
        >>> func.__name__
        'fff'
    """
    return fassign(__name__=new_name)


def fcopy(func):
    """
    Make a copy of given function.
    
    Creates a new function that wraps the original function, effectively creating a copy
    with the same behavior but a different identity. The wrapper preserves the original
    function's metadata using ``functools.wraps``.

    :param func: Function to be copied.
    :type func: Callable
    
    :return: Copied function.
    :rtype: Callable
    
    Examples::
    
        >>> def func(a, b):
        ...     return a + b
        >>> nfunc = fcopy(func)
        >>> nfunc(1, 2)
        3
        >>> nfunc is func
        False
    """

    @wraps(func)
    def _new_func(*args, **kwargs):
        return func(*args, **kwargs)

    return _new_func


def args_iter(*args, **kwargs):
    """
    Iterate all the arguments with index and value.
    
    This generator function yields (index, value) pairs for all arguments.
    For positional arguments, indices are integers starting from 0.
    For keyword arguments, indices are strings representing the argument names.
    Numeric indices appear before string indices, and the order of string indices
    follows dictionary ordering (insertion order in Python 3.7+).

    :param args: Positional arguments to iterate over.
    :type args: Tuple[Any]
    :param kwargs: Keyword arguments to iterate over.
    :type kwargs: Dict[str, Any]
    
    :yield: Tuples of (index, value) where index is int for positional args and str for keyword args.
    :rtype: Generator[Tuple[Union[int, str], Any], None, None]
    
    Examples::
    
        >>> for index, value in args_iter(1, 2, 3, a=1, b=2, c=3):
        ...     print(index, value)
        0 1
        1 2
        2 3
        a 1
        b 2
        c 3
    """
    for _index, _item in chain(enumerate(args), sorted(kwargs.items())):
        yield _index, _item


_SIG_WRAPPED = '__sig_wrapped__'
_DYNAMIC_WRAPPED = '__dynamic_wrapped__'


def sigsupply(func, sfunc):
    """
    Supply a signature for builtin functions or methods.
    
    This function provides a workaround for builtin functions that don't have inspectable
    signatures. It attaches a supplemental function's signature to the builtin function,
    allowing it to be processed by :func:`dynamic_call` and other signature-dependent operations.

    :param func: Original function, can be a native function or builtin function.
    :type func: Callable
    :param sfunc: Supplemental function with a valid signature. Its implementation doesn't matter,
                  only its signature is used.
    :type sfunc: Callable
    
    :return: The original function if it already has a signature, or a wrapped version with
             the supplemental signature attached.
    :rtype: Callable
    
    Examples::
    
        >>> dynamic_call(max)([1, 2, 3])  # no sigsupply
        ValueError: no signature found for builtin <built-in function max>
        >>> dynamic_call(sigsupply(max, lambda x: None))([1, 2, 3])  # use it as func(x) when builtin
        3
    """
    if getattr(func, _SIG_WRAPPED, None):
        return func

    try:
        signature(func, follow_wrapped=False)
    except ValueError:
        @wraps(func)
        def _new_func(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(_new_func, _SIG_WRAPPED, sfunc)
        return _new_func
    else:
        return func


def _getsignature(func):
    """
    Get the signature of a function, considering supplemental signatures.
    
    This internal helper retrieves the signature from either the function itself
    or from a supplemental function attached via :func:`sigsupply`.

    :param func: Function to get signature from.
    :type func: Callable
    
    :return: The function's signature.
    :rtype: inspect.Signature
    """
    sfunc = getattr(func, _SIG_WRAPPED, func)
    return signature(sfunc, follow_wrapped=False)


@decolize
def dynamic_call(func: Callable):
    """
    Decorate function to support dynamic calling with flexible arguments.
    
    This decorator makes a function accept any number of arguments, automatically
    filtering them based on the function's signature. Extra positional arguments
    are ignored unless the function has *args, and extra keyword arguments are
    ignored unless the function has **kwargs.

    :param func: Original function to be decorated.
    :type func: Callable
    
    :return: Decorated function that supports dynamic calling.
    :rtype: Callable
    
    Examples::
    
        >>> dynamic_call(lambda x, y: x ** y)(2, 3)  # 8
        8
        >>> dynamic_call(lambda x, y: x ** y)(2, 3, 4)  # 8, 3rd is ignored
        8
        >>> dynamic_call(lambda x, y, t, *args: (args, (t, x, y)))(1, 2, 3, 4, 5)  # ((4, 5), (3, 1, 2))
        ((4, 5), (3, 1, 2))
        >>> dynamic_call(lambda x, y: (x, y))(y=2, x=1)  # (1, 2), keyword supported
        (1, 2)
        >>> dynamic_call(lambda x, y, **kwargs: (kwargs, x, y))(1, k=2, y=3)  # ({'k': 2}, 1, 3)
        ({'k': 2}, 1, 3)

    .. note::
    
        Simple :func:`dynamic_call` **cannot support builtin functions because they do not have
        python signatures**. If you need to deal with builtin functions, you can use :func:`sigsupply`
        to add a signature onto the function when necessary.
    """
    if _is_dynamic_call(func):
        return func

    enable_args, args_count = False, 0
    enable_kwargs, kwargs_set = False, set()

    for name, param in _getsignature(func).parameters.items():
        if param.kind in {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}:
            args_count += 1
        if param.kind in (Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
            kwargs_set |= {name}
        if param.kind == Parameter.VAR_POSITIONAL:
            enable_args = True
        if param.kind == Parameter.VAR_KEYWORD:
            enable_kwargs = True

    def _get_args(*args):
        return args if enable_args else args[:args_count]

    def _get_kwargs(**kwargs):
        return kwargs if enable_kwargs else {key: value for key, value in kwargs.items() if key in kwargs_set}

    @wraps(func)
    def _new_func(*args, **kwargs):
        return func(*_get_args(*args), **_get_kwargs(**kwargs))

    setattr(_new_func, _DYNAMIC_WRAPPED, func)
    return _new_func


def _is_dynamic_call(func: Callable):
    """
    Check if a function has been wrapped by dynamic_call.
    
    :param func: Function to check.
    :type func: Callable
    
    :return: True if the function is wrapped by dynamic_call, False otherwise.
    :rtype: bool
    """
    return not not getattr(func, _DYNAMIC_WRAPPED, None)


@decolize
def static_call(func: Callable, static_ok: bool = True):
    """
    Convert a dynamic-call function back to its original static form.
    
    This function unwraps a function that has been decorated with :func:`dynamic_call`,
    returning the original function. It's the inverse operation of :func:`dynamic_call`.

    :param func: Given dynamic function to convert.
    :type func: Callable
    :param static_ok: Allow given function to be already static, default is ``True``.
    :type static_ok: bool
    
    :return: Original static function.
    :rtype: Callable
    
    :raises TypeError: If ``static_ok`` is False and the function is already static.
    """
    if not static_ok and not _is_dynamic_call(func):
        raise TypeError("Given callable is already static.")

    return getattr(func, _DYNAMIC_WRAPPED, func)


def pre_process(processor: Callable):
    """
    Create a decorator that pre-processes function arguments.
    
    This decorator applies a processor function to the arguments before passing them
    to the original function. The processor can transform both positional and keyword
    arguments.

    :param processor: Pre-processor function that transforms arguments.
    :type processor: Callable
    
    :return: Function decorator that applies pre-processing.
    :rtype: Callable
    
    Examples::
    
        >>> @pre_process(lambda x, y: (-x, (x + 2) * y))
        >>> def plus(a, b):
        >>>     return a + b
        >>>
        >>> plus(1, 2)  # 5, 5 = -1 + (1 + 2) * 2
        5
    
    .. note::
        The processor can return:
        - A tuple of (args_list, kwargs_dict) for both positional and keyword arguments
        - A tuple/list for positional arguments only
        - A dict for keyword arguments only
        - A single value which will be passed as the first positional argument
    """
    _processor = dynamic_call(processor)

    def _decorator(func):
        @wraps(func)
        def _new_func(*args, **kwargs):
            pargs = _processor(*args, **kwargs)

            if isinstance(pargs, tuple) and len(pargs) == 2 \
                    and isinstance(pargs[0], (list, tuple)) \
                    and isinstance(pargs[1], (dict,)):
                args_, kwargs_ = tuple(pargs[0]), dict(pargs[1])
            elif isinstance(pargs, (tuple, list)):
                args_, kwargs_ = tuple(pargs), {}
            elif isinstance(pargs, (dict,)):
                args_, kwargs_ = (), dict(pargs)
            else:
                args_, kwargs_ = (pargs,), {}

            return func(*args_, **kwargs_)

        return _new_func

    return _decorator


def post_process(processor: Callable):
    """
    Create a decorator that post-processes function return values.
    
    This decorator applies a processor function to the return value of the original
    function before returning it to the caller.

    :param processor: Post-processor function that transforms the return value.
    :type processor: Callable
    
    :return: Function decorator that applies post-processing.
    :rtype: Callable
    
    Examples::
    
        >>> @post_process(lambda x: -x)
        >>> def plus(a, b):
        >>>     return a + b
        >>>
        >>> plus(1, 2)  # -3
        -3
    """
    processor = dynamic_call(processor)

    def _decorator(func):
        @wraps(func)
        def _new_func(*args, **kwargs):
            _result = func(*args, **kwargs)
            return processor(_result)

        return _new_func

    return _decorator


def _is_throwable(err):
    """
    Check if an object is a throwable exception.
    
    :param err: Object to check.
    :type err: Any
    
    :return: True if the object is an exception instance or exception class.
    :rtype: bool
    """
    return isinstance(err, BaseException) or (isinstance(err, type) and issubclass(err, BaseException))


def _post_for_raising(ret):
    """
    Post-processor helper that raises exceptions if the return value is throwable.
    
    :param ret: Return value to check and potentially raise.
    :type ret: Any
    
    :return: The original return value if it's not an exception.
    :rtype: Any
    
    :raises BaseException: If ret is a throwable exception.
    """
    if _is_throwable(ret):
        raise ret
    else:
        return ret


def raising(func: Union[Callable, BaseException, Type[BaseException]]):
    """
    Decorate function to raise exceptions instead of returning them.
    
    This decorator transforms functions that return exception objects into functions
    that raise those exceptions. It can also be used directly with exception classes
    or instances to create raising callables.

    :param func: Function that returns exceptions, or an exception class/instance.
    :type func: Union[Callable, BaseException, Type[BaseException]]
    
    :return: Decorated function that raises exceptions.
    :rtype: Callable
    
    Examples::
    
        >>> raising(RuntimeError)()  # Raises RuntimeError
        RuntimeError
        >>> raising(lambda x: ValueError('value error - %s' % (repr(x), )))(1)  # Raises ValueError
        ValueError: value error - 1
    """
    if _is_throwable(func):
        return raising(dynamic_call(lambda: func))
    else:
        return post_process(_post_for_raising)(func)


def _is_warning(w):
    """
    Check if an object is a warning.
    
    :param w: Object to check.
    :type w: Any
    
    :return: True if the object is a warning instance, warning class, or warning string.
    :rtype: bool
    """
    return isinstance(w, (Warning, str)) or (isinstance(w, type) and issubclass(w, Warning))


def _warn(w):
    """
    Convert a warning class to a warning instance.
    
    :param w: Warning class, instance, or string.
    :type w: Union[Warning, Type[Warning], str]
    
    :return: Warning instance or string.
    :rtype: Union[Warning, str]
    """
    return w() if _is_warning(w) and isinstance(w, type) and issubclass(w, Warning) else w


def _post_for_warning(ret):
    """
    Post-processor helper that issues warnings if the return value is a warning.
    
    :param ret: Return value to check and potentially warn about.
    :type ret: Any
    
    :return: None if a warning was issued, otherwise the original return value.
    :rtype: Any
    """
    _matched = False
    if _is_warning(ret):
        _matched, _w, args_, kwargs_ = True, ret, (), {}
    elif isinstance(ret, tuple) and len(ret) >= 1 and _is_warning(ret[0]):
        _w, ret = ret[0], ret[1:]
        if len(ret) == 1:
            if isinstance(ret[0], tuple):
                _matched, args_, kwargs_ = True, ret[0], {}
            elif isinstance(ret[0], dict):
                _matched, args_, kwargs_ = True, (), ret[0]
        elif len(ret) == 2:
            if isinstance(ret[0], tuple) and isinstance(ret[1], dict):
                _matched, args_, kwargs_ = True, ret[0], ret[1]

    if not _matched:
        return ret
    else:
        # noinspection PyUnboundLocalVariable
        warnings.warn(_warn(_w), *args_, **kwargs_)


def warning_(func: Union[Callable, Warning, Type[Warning], str]):
    """
    Decorate function to issue warnings instead of returning them.
    
    This decorator transforms functions that return warning objects into functions
    that issue those warnings using the warnings module. It can also be used directly
    with warning classes, instances, or strings to create warning callables.

    :param func: Function that returns warnings, or a warning class/instance/string.
    :type func: Union[Callable, Warning, Type[Warning], str]
    
    :return: Decorated function that issues warnings.
    :rtype: Callable
    
    Examples::
    
        >>> warning_(RuntimeWarning)()  # Issues RuntimeWarning
        >>> warning_(lambda x: Warning('value warning - %s' % (repr(x), )))(1)  # Issues Warning
    """
    if _is_warning(func):
        return warning_(dynamic_call(lambda: func))
    else:
        return post_process(_post_for_warning)(func)


NO_INITIAL = SingletonMark("no_initial")

_ElementType = TypeVar("_ElementType")


def freduce(init=NO_INITIAL, pass_kwargs: bool = True):
    """
    Make a binary function reducible over multiple arguments.
    
    This decorator transforms a binary function into a variadic function that applies
    the binary operation repeatedly (reduction). Similar to functools.reduce but as
    a decorator with more flexibility.

    :param init: Initial value or generator function. If ``NO_INITIAL``, the first argument
                 is used as the initial value. Can be a value or a callable that returns a value.
    :type init: Any
    :param pass_kwargs: Whether to pass keyword arguments to the initial function and wrapped function.
    :type pass_kwargs: bool
    
    :return: Decorator for the original binary function.
    :rtype: Callable
    
    :raises SyntaxError: If no initial value is provided and no arguments are passed to the function.
    
    Examples::
    
        >>> @freduce(init=0)
        >>> def plus(a, b):
        >>>     return a + b
        >>>
        >>> plus()            # 0
        0
        >>> plus(1)           # 1
        1
        >>> plus(1, 2)        # 3
        3
        >>> plus(1, 2, 3, 4)  # 10
        10
    """
    if init is NO_INITIAL:
        init_func = None
    else:
        init_func = dynamic_call(init if hasattr(init, '__call__') else (lambda: init))

    def _decorator(func):
        func = dynamic_call(func)

        @wraps(func)
        def _new_func(*args, **kwargs) -> _ElementType:
            if not pass_kwargs and kwargs:
                warnings.warn(SyntaxWarning(
                    "Key-word arguments detected but will not be passed due to the pass_kwargs setting - {kwargs}.".format(
                        kwargs=repr(kwargs))))
            kwargs = kwargs if pass_kwargs else {}

            if init_func is None:
                if not args:
                    raise SyntaxError(
                        "No less than 1 argument expected in function {func} but 0 found.".format(func=repr(func)))
                current = args[0]
                args = args[1:]
            else:
                current = init_func(**kwargs)

            for arg in args:
                current = func(current, arg, **kwargs)

            return current

        return _new_func

    return _decorator


def get_callable_hint(f: Callable):
    """
    Get the type hint of a callable as a Callable type annotation.
    
    This function extracts type hints from a callable and returns a Callable type
    annotation that represents the function's signature. If the function has only
    positional parameters, it returns a specific Callable type; otherwise, it returns
    Callable[..., Any].

    :param f: Callable object to extract type hints from.
    :type f: Callable
    
    :return: Type hint representing the callable's signature.
    :rtype: type
    
    Examples::
    
        >>> def f1(x: float, y: str) -> int:
        ...     pass
        >>> get_callable_hint(f1)  # Callable[[float, str], int]
        typing.Callable[[float, str], int]
        >>>
        >>> def f2(x: float, y: str, *, z: int):
        ...     pass
        >>> get_callable_hint(f2)  # Callable[..., Any]
        typing.Callable[..., typing.Any]
    """
    count, ponly = 0, True
    for key, value in signature(f).parameters.items():
        if value.kind in {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}:
            count += 1
        else:
            ponly = False

    _type_hints = get_type_hints(f)
    _return_type = _type_hints.get('return', Any)
    if ponly:
        _items = [_type_hints.get(key, Any) for key in signature(f).parameters.keys()]
        return Callable[[*_items], _return_type]
    else:
        return Callable[..., _return_type]
