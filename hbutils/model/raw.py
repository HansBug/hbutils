from .clazz import asitems, visual, hasheq, accessor
from ..reflection import dynamic_call, frename

__all__ = [
    'raw_support'
]


def raw_support(condition, raw_name: str = 'raw', unraw_name: str = 'unraw', proxy_name='RawProxy'):
    """
    Overview:
        Get raw support wrapper function and class.

    Arguments:
        - condition: Condition of wrapper, the value will be wrapped only when ``condition`` is satisfied.
        - raw_name (:obj:`str`): Raw function's name.
        - unraw_name (:obj:`str`): Unraw function's name.
        - proxy_name (:obj:`str`): Proxy class's name.

    Returns:
        - (raw_func, unraw_func, proxy_class).

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

        def __init__(self, value):
            self.__value = value

    _RawProxy.__name__ = proxy_name

    @frename(raw_name)
    def _raw(v):
        if not isinstance(v, _RawProxy) and _dc(v):
            return _RawProxy(v)
        else:
            return v

    @frename(unraw_name)
    def _unraw(v):
        if isinstance(v, _RawProxy):
            return v.value
        else:
            return v

    return _raw, _unraw, _RawProxy
