"""
Overview:
    Implementation of observer pattern.
    See `Observer Pattern - Wikipedia <https://en.wikipedia.org/wiki/Observer_pattern>`_.

    This module provides the Observable class which implements the observer design pattern,
    allowing objects to subscribe to and receive notifications about events.
"""
from enum import Enum
from typing import Union, Type, TypeVar, Dict, Callable, Tuple, Any, List

__all__ = [
    'Observable'
]

_EventSetType = Union[Type[Enum], list, tuple]


def _auto_members(events: _EventSetType):
    """
    Extract members from event set.

    :param events: Event set, can be an Enum class, list, or tuple.
    :type events: _EventSetType

    :return: List of event members.
    :rtype: list

    :raises TypeError: If the event set type is invalid.
    """
    if isinstance(events, type) and issubclass(events, Enum):
        return list(events.__members__.values())
    elif isinstance(events, (list, tuple)):
        return list(events)
    else:
        raise TypeError(f'Invalid event set - {repr(events)}.')


def _get_object_id(obj) -> Tuple[str, int]:
    """
    Get a unique identifier for an object.

    :param obj: The object to identify.
    :type obj: Any

    :return: A tuple containing the identifier type ('hash' or 'id') and the identifier value.
    :rtype: Tuple[str, int]
    """
    try:
        return 'hash', hash(obj)
    except TypeError:
        return 'id', id(obj)


_EventType = TypeVar('_EventType')
_SubscriberType = TypeVar('_SubscriberType')
_CallbackType = TypeVar('_CallbackType', bound=Callable[..., Any])


class _CallbackWrapper:
    """
    Wrapper class for callback functions to handle dynamic argument passing.
    """

    def __init__(self, callback):
        """
        Initialize the callback wrapper.

        :param callback: The callback function to wrap.
        :type callback: Callable
        """
        from ..reflection import dynamic_call, sigsupply
        self.raw = callback
        self._callback = dynamic_call(sigsupply(callback, lambda x: None))

    def __call__(self, *args, **kwargs):
        """
        Call the wrapped callback function.

        :param args: Positional arguments to pass to the callback.
        :param kwargs: Keyword arguments to pass to the callback.

        :return: The return value of the callback function.
        :rtype: Any
        """
        return self._callback(*args, **kwargs)


class Observable:
    """
    Overview:
        Observable object implementing the observer pattern.

        * :meth:`subscribe` can be used for subscribing on specific event.
        * :meth:`unsubscribe` can be used for unsubscribing from specific event.
        * :meth:`dispatch` can be used for broadcasting a specific event, and all the subscribed callback will be \
            triggered.

    Examples::
        >>> from enum import IntEnum, unique
        >>> from hbutils.design import Observable
        >>>
        >>> @unique
        ... class MyIntEnum(IntEnum):
        ...     A = 1
        ...     B = 2
        >>>
        >>> o = Observable(MyIntEnum)
        >>> list_a, list_b = [], []
        >>> o.subscribe(MyIntEnum.A, list_a, 'append')  # use list_a.append
        >>> o.subscribe(MyIntEnum.B, list_a, lambda v: list_a.append(v))  # custom function.
        >>> o.subscribe(MyIntEnum.A, list_b, 'append')  # use list_b.append
        >>>
        >>> list_a, list_b
        ([], [])
        >>> o.dispatch(MyIntEnum.A)
        >>> list_a, list_b
        ([<MyIntEnum.A: 1>], [<MyIntEnum.A: 1>])
        >>> o.dispatch(MyIntEnum.B)
        >>> list_a, list_b
        ([<MyIntEnum.A: 1>, <MyIntEnum.B: 2>], [<MyIntEnum.A: 1>])
        >>>
        >>> o.unsubscribe(MyIntEnum.A, list_a)
        >>> o.dispatch(MyIntEnum.A)
        >>> list_a, list_b
        ([<MyIntEnum.A: 1>, <MyIntEnum.B: 2>], [<MyIntEnum.A: 1>, <MyIntEnum.A: 1>])
        >>> o.dispatch(MyIntEnum.B)
        >>> list_a, list_b
        ([<MyIntEnum.A: 1>, <MyIntEnum.B: 2>, <MyIntEnum.B: 2>], [<MyIntEnum.A: 1>, <MyIntEnum.A: 1>])
    """

    def __init__(self, events: _EventSetType):
        """
        Constructor of :class:`Observable`.

        :param events: Set of events, can be a list, tuple or an enum class.
        :type events: _EventSetType

        .. note::
            When enum is used, its values will be used as events. For example:

            >>> from enum import IntEnum
            >>> from hbutils.design import Observable
            >>>
            >>> class MyIntEnum(IntEnum):
            ...     A = 1
            ...     B = 2
            >>>
            >>> # equals to `Observable([MyIntEnum.A, MyIntEnum.B])`
            ... o = Observable(MyIntEnum)
            >>> o._events  # just for explanation, do not do this on actual use
            {<MyIntEnum.A: 1>: {}, <MyIntEnum.B: 2>: {}}
        """
        events = _auto_members(events)
        self._observers: Dict[Tuple[str, int], _SubscriberType] = {}
        self._events: Dict[_EventType, Dict[Tuple[str, int], _CallbackWrapper]] = {e: {} for e in events}

    def subscribers(self, event: _EventType) -> List[_SubscriberType]:
        """
        Get subscribers of the given ``event``.

        :param event: Event for querying.
        :type event: _EventType

        :return: A list of subscribers.
        :rtype: List[_SubscriberType]
        """
        return [self._observers[id_] for id_ in self._get_subscriptions(event).keys()]

    def subscriptions(self, event: _EventType) -> List[Tuple[_SubscriberType, _CallbackType]]:
        """
        Get subscriptions of the given ``event``.

        :param event: Event for querying.
        :type event: _EventType

        :return: A list of tuples with subscribers and their callbacks.
        :rtype: List[Tuple[_SubscriberType, _CallbackType]]
        """
        return [
            (self._observers[id_], callback.raw)
            for id_, callback in self._get_subscriptions(event).items()
        ]

    def _get_subscriptions(self, event: _EventType) -> Dict[Tuple[str, int], _CallbackWrapper]:
        """
        Get the subscription dictionary for a specific event.

        :param event: The event to query.
        :type event: _EventType

        :return: Dictionary mapping subscriber IDs to callback wrappers.
        :rtype: Dict[Tuple[str, int], _CallbackWrapper]
        """
        return self._events[event]

    def _put_subscription(self, event: _EventType, subscriber: _SubscriberType, callback: _CallbackType):
        """
        Add a subscription for a specific event.

        :param event: The event to subscribe to.
        :type event: _EventType
        :param subscriber: The subscriber object.
        :type subscriber: _SubscriberType
        :param callback: The callback function.
        :type callback: _CallbackType
        """
        subscriber_id = _get_object_id(subscriber)
        self._get_subscriptions(event)[subscriber_id] = _CallbackWrapper(callback)
        self._observers[subscriber_id] = subscriber

    def _del_subscription(self, event: _EventType, subscriber: _SubscriberType):
        """
        Remove a subscription for a specific event.

        :param event: The event to unsubscribe from.
        :type event: _EventType
        :param subscriber: The subscriber object.
        :type subscriber: _SubscriberType

        :raises KeyError: If the subscriber is not found.
        """
        try:
            del self._get_subscriptions(event)[_get_object_id(subscriber)]
        except KeyError:
            raise KeyError(subscriber)

    def subscribe(self, event: _EventType, subscriber: _SubscriberType,
                  callback: Union[_CallbackType, str, None] = None):
        """
        Subscribe to the given ``event``.

        :param event: Event to be subscribed.
        :type event: _EventType
        :param subscriber: Subscriber of this subscription.
        :type subscriber: _SubscriberType
        :param callback: Callback function. If ``str`` is given, method with this name on ``subscriber`` will be used. \
            Default is ``None`` which means the ``update`` method on ``subscriber`` will be used.
        :type callback: Union[_CallbackType, str, None]

        :raises TypeError: If the callback is not callable.

        .. note::
            Callback function should have no more than 2 positional arguments. For example:

            >>> o.subscribe(MyIntEnum.A, 'user1', lambda: 2)  # ok
            >>> o.subscribe(MyIntEnum.A, 'user2', lambda event: 2)  # ok
            >>> o.subscribe(MyIntEnum.A, 'user3', lambda event, obs: 2)  # ok
            >>> o.subscribe(MyIntEnum.A, 'user4', lambda x, y, z: 2)  # X
        """
        if callback is None:
            callback = getattr(subscriber, 'update')
        elif isinstance(callback, str):
            callback = getattr(subscriber, callback)
        if not callable(callback):
            raise TypeError(f'Callback should be callable, but {repr(callback)} found.')

        self._put_subscription(event, subscriber, callback)

    def unsubscribe(self, event: _EventType, subscriber: _SubscriberType):
        """
        Unsubscribe from the given ``event``.

        :param event: Event to be unsubscribed.
        :type event: _EventType
        :param subscriber: Subscriber of this unsubscription.
        :type subscriber: _SubscriberType

        :raises KeyError: If the subscriber is not found for the given event.
        """
        self._del_subscription(event, subscriber)

    def dispatch(self, event: _EventType):
        """
        Dispatch event to all subscribers.

        :param event: Event to be dispatched.
        :type event: _EventType

        This method triggers all callbacks subscribed to the given event,
        passing the event and the observable instance as arguments.
        """
        for _, callback in self._get_subscriptions(event).items():
            callback(event, self)
