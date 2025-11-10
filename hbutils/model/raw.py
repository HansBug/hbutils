"""
This module provides support for wrapping and unwrapping raw values based on conditions.

The module offers a factory function to create raw/unraw functions and a proxy class
that can conditionally wrap values. This is useful for marking certain values as "raw"
to prevent further processing or transformation.
"""

from .clazz import asitems, visual, hasheq, accessor
from ..reflection import dynamic_call, frename

__all__ = [
    'raw_support'
]


def raw_support(condition, raw_name: str = 'raw', unraw_name: str = 'unraw', proxy_name='RawProxy'):
    """
    Get raw support wrapper function and class.

    This function creates a set of utilities for conditionally wrapping values in a proxy class.
    Values that satisfy the given condition can be wrapped to mark them as "raw", preventing
    further processing. The wrapped values can later be unwrapped to retrieve the original value.

    :param condition: Condition function or callable that determines when a value should be wrapped.
                     The value will be wrapped only when ``condition`` returns True.
    :type condition: callable
    :param raw_name: Name for the raw wrapping function, defaults to 'raw'.
    :type raw_name: str
    :param unraw_name: Name for the unwrapping function, defaults to 'unraw'.
    :type unraw_name: str
    :param proxy_name: Name for the proxy class, defaults to 'RawProxy'.
    :type proxy_name: str

    :return: A tuple containing (raw_func, unraw_func, proxy_class) where:
            - raw_func: Function to wrap values that satisfy the condition
            - unraw_func: Function to unwrap proxy objects back to original values
            - proxy_class: The proxy class used for wrapping
    :rtype: tuple

    Examples::
        >>> from hbutils.model import raw_support
        >>> raw, unraw, RawProxy = raw_support(lambda x: isinstance(x, dict))
        >>> raw(1)
        1
        >>> raw({'a': 1, 'b': 2})
        <RawProxy value: {'a': 1, 'b': 2}>

        >>> unraw(1)
        1
        >>> unraw({'a': 1, 'b': 2})
        {'a': 1, 'b': 2}
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

        This class wraps values that need to be marked as "raw" to prevent further processing.
        It provides read-only access to the wrapped value and supports visualization, hashing,
        and equality comparison.
        """

        def __init__(self, value):
            """
            Initialize the raw proxy with a value.

            :param value: The value to be wrapped as raw.
            :type value: Any
            """
            self.__value = value

    _RawProxy.__name__ = proxy_name

    @frename(raw_name)
    def _raw(v):
        """
        Wrap a value in a raw proxy if it satisfies the condition.

        If the value is not already wrapped and satisfies the condition function,
        it will be wrapped in a RawProxy object. Otherwise, the value is returned as-is.

        :param v: The value to potentially wrap.
        :type v: Any

        :return: Either the original value or a RawProxy wrapping the value.
        :rtype: Any or _RawProxy
        """
        if not isinstance(v, _RawProxy) and _dc(v):
            return _RawProxy(v)
        else:
            return v

    @frename(unraw_name)
    def _unraw(v):
        """
        Unwrap a raw proxy to retrieve the original value.

        If the value is a RawProxy instance, extract and return the wrapped value.
        Otherwise, return the value unchanged.

        :param v: The value to potentially unwrap.
        :type v: Any

        :return: The unwrapped value if v is a RawProxy, otherwise v itself.
        :rtype: Any
        """
        if isinstance(v, _RawProxy):
            return v.value
        else:
            return v

    return _raw, _unraw, _RawProxy
