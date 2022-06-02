"""
Overview:
    Utilities for building context variables on thread level.

    This is useful when implementing a with-block-based syntax.
    For example:

        >>> from contextlib import contextmanager
        >>> from hbutils.reflection import context
        >>>
        >>> # developer's view
        ... @contextmanager
        ... def use_mul():  # set 'mul' to `True` in its with-block
        ...     with context().vars(mul=True):
        ...         yield
        >>>
        >>> def calc(a, b):  # logic of `calc` will be changed when 'mul' is given
        ...     if context().get('mul', None):
        ...         return a * b
        ...     else:
        ...         return a + b
        >>>
        >>> # user's view (magic-liked, isn't it?)
        ... print(calc(3, 5))  # 3 + 5
        8
        >>> with use_mul():
        ...     print(calc(3, 5))  # changed to 3 * 5
        15
        >>> print(calc(3, 5))  # back to 3 + 5, again :)
        8
"""
import collections.abc

from contextlib import contextmanager
from functools import wraps
from multiprocessing import current_process
from threading import current_thread
from typing import Tuple, TypeVar, Iterator, Mapping, Optional

__all__ = [
    'context', 'cwrap',
]


def _get_pid() -> int:
    return current_process().pid


def _get_tid() -> int:
    return current_thread().ident


def _get_context_id() -> Tuple[int, int]:
    return _get_pid(), _get_tid()


_global_contexts = {}

_KeyType = TypeVar('_KeyType', bound=str)
_ValueType = TypeVar('_ValueType')


class ContextVars(collections.abc.Mapping):
    """
    Overview:
        Context variable management.

    .. note::
        This class is inherited from :class:`collections.abc.Mapping`.
        Main features of mapping object (such as ``__getitem__``, ``__len__``, ``__iter__``) are supported.
        See `Collections Abstract Base Classes \
        <https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes>`_.

    .. warning::
        This object should be singleton on thread level.
        It is not recommended constructing manually.
    """

    def __init__(self, **kwargs):
        """
        Constructor of :class:`ContextVars`.

        :param kwargs: Initial context values.
        """
        self._vars = dict(kwargs)

    @contextmanager
    def _with_vars(self, params: Mapping[_KeyType, _ValueType], clear: bool = False):
        # initialize new values
        _origin = dict(self._vars)
        self._vars.update(params)
        if clear:
            for key in list(self._vars.keys()):
                if key not in params:
                    del self._vars[key]

        try:
            yield
        finally:
            # de-initialize, recover changed values
            for k in set(_origin.keys()) | set(self._vars.keys()):
                if k not in _origin:
                    del self._vars[k]
                else:
                    self._vars[k] = _origin[k]

    @contextmanager
    def vars(self, **kwargs):
        """
        Adding variables into context of ``with`` block.

        :param kwargs: Additional context variables.

        Examples::
            >>> from hbutils.reflection import context
            >>>
            >>> def var_detect():
            ...     if context().get('var', None):
            ...         print(f'Var detected, its value is {context()["var"]}.')
            ...     else:
            ...         print('Var not detected.')
            >>>
            >>> var_detect()
            Var not detected.
            >>> with context().vars(var=1):
            ...     var_detect()
            Var detected, its value is 1.
            >>> var_detect()
            Var not detected.

        .. note::
            See :func:`context`.

        """
        with self._with_vars(kwargs, clear=False):
            yield

    @contextmanager
    def inherit(self, context_: 'ContextVars'):
        """
        Inherit variables from the given context.

        :param context_: :class:`ContextVars` object to inherit from.

        .. note::
            After :meth:`inherit` is used, **the original variables which not present in the given ``context_`` \
            will be removed**. This is different from :meth:`vars`, so attention.
        """
        with self._with_vars(context_._vars, clear=True):
            yield

    def __getitem__(self, key: _KeyType):
        return self._vars[key]

    def __len__(self) -> int:
        return len(self._vars)

    def __iter__(self) -> Iterator[_KeyType]:
        return self._vars.__iter__()


def context() -> ContextVars:
    """
    Overview:
        Get context object in this thread.

    :return: Context object in this thread.

    .. note::
        This result is unique on one thread.
    """
    _context_id = _get_context_id()
    if _context_id not in _global_contexts:
        _context = ContextVars()
        _global_contexts[_context_id] = _context

    return _global_contexts[_context_id]


def cwrap(func, *, context_: Optional[ContextVars] = None, **vars_):
    """
    Overview:
        Context wrap for functions.

    :param func: Original function to wrap.
    :param context_: Context for inheriting. Default is ``None`` which means :func:`context`'s result will be used.
    :param vars_: External variables after inherit context.

    .. note::
        :func:`cwrap` is important when you need to pass the current context into thread.
        And **it is compitable on all platforms**.

        For example:

            >>> from threading import Thread
            >>> from hbutils.reflection import context, cwrap
            >>>
            >>> def var_detect():
            ...     if context().get('var', None):
            ...         print(f'Var detected, its value is {context()["var"]}.')
            ...     else:
            ...         print('Var not detected.')
            >>>
            >>> with context().vars(var=1):  # no inherit, vars will be lost in thread
            ...     t = Thread(target=var_detect)
            ...     t.start()
            ...     t.join()
            Var not detected.
            >>> with context().vars(var=1):  # with inherit, vars will be kept in thread
            ...     t = Thread(target=cwrap(var_detect))
            ...     t.start()
            ...     t.join()
            Var detected, its value is 1.

    .. warning::
        :func:`cwrap` **is not compitable on Windows or Python3.8+ on macOS** when creating **new process**.
        Please pass in direct arguments by ``args`` argument of :class:`Process`.
        If you insist on using :func:`context` feature, you need to pass the context object into the sub process.
        For example:

            >>> from contextlib import contextmanager
            >>> from multiprocessing import Process
            >>> from hbutils.reflection import context
            >>>
            >>> # developer's view
            ... @contextmanager
            ... def use_mul():  # set 'mul' to `True` in its with-block
            ...     with context().vars(mul=True):
            ...         yield
            >>>
            >>> def calc(a, b):  # logic of `calc` will be changed when 'mul' is given
            ...     if context().get('mul', None):
            ...         print(a * b)
            ...     else:
            ...         print(a + b)
            >>>
            >>> def _calc(a, b, ctx=None):
            ...     with context().inherit(ctx or context()):
            ...         return calc(a, b)
            >>>
            >>> # user's view
            ... if __name__ == '__main__':
            ...     calc(3, 5)  # 3 + 5
            ...     with use_mul():
            ...         p = Process(target=_calc, args=(3, 5, context()))
            ...         p.start()
            ...         p.join()
            ...     calc(3, 5)  # back to 3 + 5, again :)
            8
            15
            8

    """
    context_ = context_ or context()

    @wraps(func)
    def _new_func(*args, **kwargs):
        with context().inherit(context_):
            with context().vars(**vars_):
                return func(*args, **kwargs)

    return _new_func
