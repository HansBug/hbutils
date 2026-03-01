"""
Observer pattern implementation for event-driven subscriptions.

This module implements a lightweight observer pattern utility centered on the
:class:`Observable` class, enabling objects (subscribers) to register callbacks
for specific events and receive notifications when those events are dispatched.

The module contains the following public components:

* :class:`Observable` - Event dispatcher supporting subscriptions and notifications.

.. note::
   Events can be defined as an :class:`enum.Enum` subclass or as an iterable
   of event identifiers (e.g., strings, integers, or enum members).

Example::

    >>> from enum import Enum, unique
    >>> from hbutils.design.observer import Observable
    >>>
    >>> @unique
    ... class Event(Enum):
    ...     READY = 'ready'
    ...     DONE = 'done'
    >>>
    >>> observable = Observable(Event)
    >>> received = []
    >>> observable.subscribe(Event.READY, received, 'append')
    >>> observable.dispatch(Event.READY)
    >>> received
    [<Event.READY: 'ready'>]

"""
from enum import Enum
from typing import Union, Type, TypeVar, Dict, Callable, Tuple, Any, List

__all__ = [
    'Observable'
]

_EventSetType = Union[Type[Enum], list, tuple]


def _auto_members(events: _EventSetType) -> List[Any]:
    """
    Extract members from an event set.

    The event set can be an :class:`enum.Enum` class or a plain list/tuple of
    event identifiers. Enum classes are expanded into their members.

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


def _get_object_id(obj: Any) -> Tuple[str, int]:
    """
    Get a unique identifier for an object.

    Objects with a valid ``__hash__`` implementation are identified using their
    hash; otherwise their memory id is used.

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
    Wrapper for callback functions to support dynamic argument passing.

    The wrapper uses reflection utilities to safely call the underlying callback
    while supplying only the parameters it can accept.
    """

    def __init__(self, callback: Callable[..., Any]) -> None:
        """
        Initialize the callback wrapper.

        :param callback: The callback function to wrap.
        :type callback: Callable[..., Any]
        """
        from ..reflection import dynamic_call, sigsupply
        self.raw = callback
        self._callback = dynamic_call(sigsupply(callback, lambda x: None))

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Call the wrapped callback function.

        :param args: Positional arguments to pass to the callback.
        :type args: Any
        :param kwargs: Keyword arguments to pass to the callback.
        :type kwargs: Any
        :return: The return value of the callback function.
        :rtype: Any
        """
        return self._callback(*args, **kwargs)


class Observable:
    """
    Observable object implementing the observer pattern.

    The observable holds a set of events, and subscribers may register callbacks
    for each event. When an event is dispatched, all associated callbacks are
    invoked with the event and the observable instance as arguments.

    * :meth:`subscribe` can be used for subscribing to a specific event.
    * :meth:`unsubscribe` can be used for unsubscribing from a specific event.
    * :meth:`dispatch` can be used for broadcasting a specific event, and all
      the subscribed callbacks will be triggered.

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

    def __init__(self, events: _EventSetType) -> None:
        """
        Construct an :class:`Observable`.

        :param events: Set of events, can be a list, tuple, or an enum class.
        :type events: _EventSetType

        .. note::
            When an enum class is used, its members will be used as events. For example:

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

    def _put_subscription(self, event: _EventType, subscriber: _SubscriberType,
                          callback: _CallbackType) -> None:
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

    def _del_subscription(self, event: _EventType, subscriber: _SubscriberType) -> None:
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
                  callback: Union[_CallbackType, str, None] = None) -> None:
        """
        Subscribe to the given ``event``.

        :param event: Event to be subscribed.
        :type event: _EventType
        :param subscriber: Subscriber of this subscription.
        :type subscriber: _SubscriberType
        :param callback: Callback function. If ``str`` is given, the method with this
            name on ``subscriber`` will be used. Default is ``None`` which means the
            ``update`` method on ``subscriber`` will be used.
        :type callback: Union[_CallbackType, str, None]
        :raises TypeError: If the callback is not callable.

        .. note::
            Callback functions should accept no more than 2 positional arguments. For example:

            >>> o.subscribe(MyIntEnum.A, 'user1', lambda: 2)  # ok
            >>> o.subscribe(MyIntEnum.A, 'user2', lambda event: 2)  # ok
            >>> o.subscribe(MyIntEnum.A, 'user3', lambda event, obs: 2)  # ok
            >>> o.subscribe(MyIntEnum.A, 'user4', lambda x, y, z: 2)  # invalid
        """
        if callback is None:
            callback = getattr(subscriber, 'update')
        elif isinstance(callback, str):
            callback = getattr(subscriber, callback)
        if not callable(callback):
            raise TypeError(f'Callback should be callable, but {repr(callback)} found.')

        self._put_subscription(event, subscriber, callback)

    def unsubscribe(self, event: _EventType, subscriber: _SubscriberType) -> None:
        """
        Unsubscribe from the given ``event``.

        :param event: Event to be unsubscribed.
        :type event: _EventType
        :param subscriber: Subscriber of this unsubscription.
        :type subscriber: _SubscriberType
        :raises KeyError: If the subscriber is not found for the given event.
        """
        self._del_subscription(event, subscriber)

    def dispatch(self, event: _EventType) -> None:
        """
        Dispatch an event to all subscribers.

        This method triggers all callbacks subscribed to the given event, passing
        the event and the observable instance as arguments.

        :param event: Event to be dispatched.
        :type event: _EventType
        """
        for _, callback in self._get_subscriptions(event).items():
            callback(event, self)
