"""
Overview:
    Useful functions for processing python classes and types.
"""
from functools import WRAPPER_ASSIGNMENTS as CLASS_WRAPPER_ASSIGNMENTS
from functools import update_wrapper, partial
from typing import Tuple

__all__ = [
    'class_wraps',
    'common_base',
]

CLASS_WRAPPER_UPDATES = ()


def class_wraps(wrapped: type,
                assigned: Tuple[str] = CLASS_WRAPPER_ASSIGNMENTS,
                updated: Tuple[str] = CLASS_WRAPPER_UPDATES):
    r"""
    Overview:
        Wrapper decorator for class.

    Arguments:
        - wrapped (:obj:`type`): Wrapped class.
        - assigned (:obj:`Tuple[str]`): Wrapper assignments, equal to :func:`functools.wraps`'s \
            ``WRAPPER_ASSIGNMENTS``.
        - updated (:obj:`Tuple[str]`): Wrapper updates, default is ``()``, no update will be done.

    Examples:
        >>> def cls_dec(clazz):
        >>>     @class_wraps(clazz)
        >>>     class _NewClazz(clazz):
        >>>         pass
        >>>
        >>>     return _NewClazz
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)


def common_base(cls: type, *clss: type) -> type:
    """
    Overview:
        Get common base class of the given classes.
        Only ``__base__`` is considered.

    Arguments:
        - cls (:obj:`type`): First class.
        - clss (:obj:`type`): Other classes.

    Returns:
        - base (:obj:`type`): Common base class.

    Examples::
        >>> from hbutils.reflection import common_base
        >>> common_base(object)
        <class 'object'>
        >>> common_base(object, int, str)
        <class 'object'>
        >>> common_base(RuntimeError, ValueError, KeyError)
        <class 'Exception'>
    """
    current_cls = cls
    for new_cls in clss:
        while not issubclass(new_cls, current_cls):
            current_cls = current_cls.__base__

        if current_cls is object:
            break

    return current_cls
