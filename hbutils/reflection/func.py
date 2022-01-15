"""
Overview:
    Useful functions for processing python functions.
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
    Overview:
        Do assignments to function.

    Arguments:
        - assigns: Assignment values.

    Returns:
        - decorator: A decorator for assigning.

    Examples::
        >>> @fassign(__name__='fff')
        >>> def func(a, b):
        >>>     return a + b
    """

    def _decorator(func):
        for k, v in assigns.items():
            setattr(func, k, v)

        return func

    return _decorator


def frename(new_name: str):
    """
    Overview:
        Rename the given function.

    Arguments:
        - new_name (:obj:`str`): New name of function.

    Returns:
        - decorator: Decorator to rename the function.

    Examples::
        >>> @frename('fff')
        >>> def func(a, b):
        >>>     return a + b
    """
    return fassign(__name__=new_name)


def fcopy(func):
    """
    Overview:
        Make a copy of given function.

    Arguments:
        - func: Function to be copied.

    Returns:
        - new_func: Copied function.

    Examples::
        >>> def func(a, b):
        ...     return a + b
        >>> nfunc = fcopy(func)
        >>> nfunc(1, 2)
        3
    """

    @wraps(func)
    def _new_func(*args, **kwargs):
        return func(*args, **kwargs)

    return _new_func


def args_iter(*args, **kwargs):
    """
    Overview:
        Iterate all the arguments with index and value.
        If argument is in `args`, the index should be integer increasing from 0.
        If argument is in `kwargs`, the index should be string which meaning the argument's name.
        The numeric indices will appear before the string indices,
        and **the order of the string indices are not approved**.

    Arguments:
        - args (:obj:`Tuple[Any]`): Argument list
        - kwargs (:obj:`Dict[str, Any]`): Argument mapping

    Example:
        >>> for index, value in args_iter(1, 2, 3, a=1, b=2, c=3)):
        >>>     print(index, value)

        The output should be

        >>> 0 1
        >>> 1 2
        >>> 2 3
        >>> a 1
        >>> b 2
        >>> c 3
    """
    for _index, _item in chain(enumerate(args), sorted(kwargs.items())):
        yield _index, _item


_SIG_WRAPPED = '__sig_wrapped__'
_DYNAMIC_WRAPPED = '__dynamic_wrapped__'


def sigsupply(func, sfunc):
    """
    Overview:
        A solution for :func:`dynamic_call`. When ``func`` is a builtin function or method \
        (which means its signature can not be captured by ``inspect.signature``), the signature of \
        ``sfunc`` will take the place, and the builtin function will be able to processed properly by \
        function :func:`dynamic_call`.

    Arguments:
        - func: Original function, can be a native function or builtin function.
        - sfunc: Supplemental function, must be a native python function which has signature. \
            Its inner logic has no importance, just provide a lambda with arguments format and \
            ``None`` return.

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
    sfunc = getattr(func, _SIG_WRAPPED, func)
    return signature(sfunc, follow_wrapped=False)


@decolize
def dynamic_call(func: Callable):
    """
    Overview:
        Decorate function to dynamic-call-supported function.

    Arguments:
        - func (:obj:`Callable`): Original function to be decorated.

    Returns:
        - new_func (:obj:`Callable`): Decorated function.

    Example:
        >>> dynamic_call(lambda x, y: x ** y)(2, 3)  # 8
        >>> dynamic_call(lambda x, y: x ** y)(2, 3, 4)  # 8, 3rd is ignored
        >>> dynamic_call(lambda x, y, t, *args: (args, (t, x, y)))(1, 2, 3, 4, 5)  # ((4, 5), (3, 1, 2))
        >>> dynamic_call(lambda x, y: (x, y))(y=2, x=1)  # (1, 2), key word supported
        >>> dynamic_call(lambda x, y, **kwargs: (kwargs, x, y))(1, k=2, y=3)  # ({'k': 2}, 1, 3)

    .. note::

        Simple :func:`dynamic_call` **can not support builtin functions because they do not have \
        python signature**. If you need to deal with builtin functions, you can use :func:`sigsupply` \
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
    return not not getattr(func, _DYNAMIC_WRAPPED, None)


@decolize
def static_call(func: Callable, static_ok: bool = True):
    """
    Overview:
        Static call, anti-calculation of dynamic call.

    Arguments:
        - func (:obj:`Callable`): Given dynamic function.
        - static_ok (:obj:`bool`): Allow given function to be static, default is ``True``.

    Returns:
        - static (:obj:`Callable`): Static function.
    """
    if not static_ok and not _is_dynamic_call(func):
        raise TypeError("Given callable is already static.")

    return getattr(func, _DYNAMIC_WRAPPED, func)


def pre_process(processor: Callable):
    """
    Overview:
        Pre processor for function.

    Arguments:
        - processor (:obj:`Callable`): Pre processor.

    Returns:
        - decorator (:obj:`Callable`): Function decorator

    Example:
        >>> @pre_process(lambda x, y: (-x, (x + 2) * y))
        >>> def plus(a, b):
        >>>     return a + b
        >>>
        >>> plus(1, 2)  # 5, 5 = -1 + (1 + 2) * 2
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
    Overview:
        Post processor for function.

    Arguments:
        - processor (:obj:`Callable`): Post processor.

    Returns:
        - decorator (:obj:`Callable`): Function decorator

    Example:
        >>> @post_process(lambda x: -x)
        >>> def plus(a, b):
        >>>     return a + b
        >>>
        >>> plus(1, 2)  # -3
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
    return isinstance(err, BaseException) or (isinstance(err, type) and issubclass(err, BaseException))


def _post_for_raising(ret):
    if _is_throwable(ret):
        raise ret
    else:
        return ret


def raising(func: Union[Callable, BaseException, Type[BaseException]]):
    """
    Overview:
        Decorate function with exception object return value to a raisisng function.

    Arguments:
        - func (:obj:`Union[Callable, BaseException, Type[BaseException]]`): Not decorated function or class

    Returns:
        - decorated (:obj:`Callable`): Decorated new function

    Examples:
        >>> raising(RuntimeError)()  # RuntimeError
        >>> raising(lambda x: ValueError('value error - %s' % (repr(x), )))(1)  # ValueError, value error - 1
    """
    if _is_throwable(func):
        return raising(dynamic_call(lambda: func))
    else:
        return post_process(_post_for_raising)(func)


def _is_warning(w):
    return isinstance(w, (Warning, str)) or (isinstance(w, type) and issubclass(w, Warning))


def _warn(w):
    return w() if _is_warning(w) and isinstance(w, type) and issubclass(w, Warning) else w


def _post_for_warning(ret):
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
    Overview:
        Decorate function with exception object return value to a ``warning_`` function.

    Arguments:
        - func (:obj:`Union[Callable, Warning, Type[Warning], str]`): Not decorated function or class

    Returns:
        - decorated (:obj:`Callable`): Decorated new function

    Examples:
        >>> warning_(RuntimeWarning)()  # RuntimeWarning
        >>> raising(lambda x: Warning('value warning - %s' % (repr(x), )))(1)  # Warning, value warning - 1
    """
    if _is_warning(func):
        return warning_(dynamic_call(lambda: func))
    else:
        return post_process(_post_for_warning)(func)


NO_INITIAL = SingletonMark("no_initial")

_ElementType = TypeVar("_ElementType")


def freduce(init=NO_INITIAL, pass_kwargs: bool = True):
    """
    Overview:
        Make binary function be reducible.

    Arguments:
        - init (:obj:`Any`): Initial data generator or \
            initial data, default is `NO_INITIAL` which means no initial data. \
            Missing of positional arguments is forbidden.
        - pass_kwargs (:obj:`bool`): Pass kwargs into initial function and wrapped function or not, \
            default is `True` which means pass the arguments in.

    Returns:
        - decorator (:obj:`Callable`): Decorator for the original function.

    Example:
        >>> @freduce(init=0)
        >>> def plus(a, b):
        >>>     return a + b
        >>>
        >>> plus()            # 0
        >>> plus(1)           # 1
        >>> plus(1, 2)        # 3
        >>> plus(1, 2, 3, 4)  # 10
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
    Overview:
        Get type hint of callable.

    Arguments:
        - f (:obj:`Callable`): Callable object.

    Returns:
        - hint: Hint of the callable.

    Example:
        >>> def f1(x: float, y: str) -> int:
        >>>     pass
        >>> get_callable_hint(f1)  # Callable[[float, str], int]
        >>>
        >>> def f2(x: float, y: str, *, z: int):
        >>>     pass
        >>> get_callable_hint(f2)  # Callable[..., Any]
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
