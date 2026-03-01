"""
Conditional raw value wrapping utilities.

This module provides a factory function that builds a raw-value wrapper,
an unwrapping helper, and a proxy class for marking values as "raw".
Wrapped values are intended to bypass additional processing stages and
can be unwrapped later to restore the original value.

The module contains the following public component:

* :func:`raw_support` - Factory for creating raw/unraw functions and a proxy class

Example::

    >>> from hbutils.model.raw import raw_support
    >>> raw, unraw, RawProxy = raw_support(lambda x: isinstance(x, dict))
    >>> raw(1)
    1
    >>> raw({'a': 1, 'b': 2})
    <RawProxy value: {'a': 1, 'b': 2}>
    >>> unraw(raw({'a': 1, 'b': 2}))
    {'a': 1, 'b': 2}

.. note::
   The proxy class returned by :func:`raw_support` is dynamically created
   and named according to the ``proxy_name`` argument.
"""

from typing import Any, Callable, Tuple, Type

from .clazz import asitems, visual, hasheq, accessor
from ..reflection import dynamic_call, frename

__all__ = [
    'raw_support'
]


def raw_support(condition: Callable[..., bool],
                raw_name: str = 'raw',
                unraw_name: str = 'unraw',
                proxy_name: str = 'RawProxy') -> Tuple[Callable[[Any], Any], Callable[[Any], Any], Type[Any]]:
    """
    Create raw/unraw helpers and a proxy class based on a condition.

    This factory function builds a set of utilities for conditionally wrapping
    values in a proxy class. When a value satisfies the provided ``condition``,
    it will be wrapped in the dynamically created proxy class. Wrapped values
    can later be restored with the unwrapping function.

    The condition is passed through :func:`hbutils.reflection.dynamic_call` to
    allow flexible signatures and to ignore extra arguments when necessary.

    :param condition: Predicate callable that determines whether a value should
                      be wrapped. The value is wrapped only when the predicate
                      returns ``True``.
    :type condition: Callable[..., bool]
    :param raw_name: Name for the raw wrapping function, defaults to ``'raw'``.
    :type raw_name: str, optional
    :param unraw_name: Name for the unwrapping function, defaults to ``'unraw'``.
    :type unraw_name: str, optional
    :param proxy_name: Name for the proxy class, defaults to ``'RawProxy'``.
    :type proxy_name: str, optional
    :return: A tuple of ``(raw_func, unraw_func, proxy_class)`` where:

             * ``raw_func`` wraps values that satisfy the condition.
             * ``unraw_func`` unwraps proxy objects back to original values.
             * ``proxy_class`` is the dynamically generated proxy class.
    :rtype: tuple[Callable[[Any], Any], Callable[[Any], Any], type]

    Example::

        >>> raw, unraw, RawProxy = raw_support(lambda x: isinstance(x, dict))
        >>> raw(1)
        1
        >>> raw({'a': 1, 'b': 2})
        <RawProxy value: {'a': 1, 'b': 2}>
        >>> unraw(raw({'a': 1, 'b': 2}))
        {'a': 1, 'b': 2}

    """
    _dc = dynamic_call(condition)

    @visual()
    @hasheq()
    @accessor(readonly=True)
    @asitems(['value'])
    class _RawProxy:
        """
        Proxy class for wrapping raw values.

        Instances of this class store a value that is marked as "raw".
        The class provides read-only access to the wrapped value and
        supports visualization, hashing, and equality comparison.

        :param value: The value to be wrapped as raw.
        :type value: Any
        """

        def __init__(self, value: Any):
            """
            Initialize the raw proxy with a value.

            :param value: The value to be wrapped as raw.
            :type value: Any
            """
            self.__value = value

    _RawProxy.__name__ = proxy_name

    @frename(raw_name)
    def _raw(v: Any) -> Any:
        """
        Wrap a value in a raw proxy if it satisfies the condition.

        If the value is not already wrapped and satisfies the condition,
        it is wrapped in the proxy class. Otherwise, the value is returned
        unchanged.

        :param v: The value to potentially wrap.
        :type v: Any
        :return: The original value or a proxy wrapping the value.
        :rtype: Any
        """
        if not isinstance(v, _RawProxy) and _dc(v):
            return _RawProxy(v)
        else:
            return v

    @frename(unraw_name)
    def _unraw(v: Any) -> Any:
        """
        Unwrap a raw proxy to retrieve the original value.

        If the value is an instance of the proxy class, the wrapped value
        is returned. Otherwise, the value is returned unchanged.

        :param v: The value to potentially unwrap.
        :type v: Any
        :return: The unwrapped value if ``v`` is a proxy, otherwise ``v``.
        :rtype: Any
        """
        if isinstance(v, _RawProxy):
            return v.value
        else:
            return v

    return _raw, _unraw, _RawProxy
