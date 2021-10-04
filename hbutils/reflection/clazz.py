"""
Overview:
    Useful functions for processing python classes and types.
"""
from functools import WRAPPER_ASSIGNMENTS as CLASS_WRAPPER_ASSIGNMENTS
from functools import update_wrapper, partial
from typing import Tuple

__all__ = ['class_wraps']

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
