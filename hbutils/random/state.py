"""
Overview:
    Random state and seed management.

    Native default random instance (``random._inst``), torch, numpy and faker (default random instance) are supported. \
    Other random sources can be registered with :func:`register_random_source` and :func:`register_random_instance`.
"""
import random
import warnings
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Tuple, TypeVar, Dict, Mapping

T = TypeVar('T')

_SEED_FUNC = Callable[[int], None]
_GETSTATE_FUNC = Callable[[], T]
_SETSTATE_FUNC = Callable[[T], None]
_RANDOM_SOURCES: Dict[str, Tuple[_SEED_FUNC, _GETSTATE_FUNC, _SETSTATE_FUNC]] = {}

__all__ = [
    'register_random_source',
    'register_random_instance',
    'get_global_state',
    'set_global_state',
    'keep_global_state',
    'global_seed',
    'seedable_func',
]


def register_random_source(name: str, seed: _SEED_FUNC, getstate: _GETSTATE_FUNC, setstate: _SETSTATE_FUNC):
    """
    Overview:
        Register random source, providing name, random seed function, state getting function \
        and state setting function.

    :param name: Name of random source.
    :param seed: Seed function, format: ``seed(x)``.
    :param getstate: State getting function, format: ``getstate()``.
    :param setstate: State setting function, format: ``setstate(state)``.

    Examples::
        >>> import random
        >>> from hbutils.random import global_seed, register_random_source
        >>>
        >>> rnd = random.Random()  # custom random object
        >>> global_seed(0)  # try to use same seed
        >>> rnd.random()
        0.4563765178328746
        >>> global_seed(0)
        >>> rnd.random()  # not same
        0.06875325446897462
        >>>
        >>> register_random_source('custom_random', rnd.seed, rnd.getstate, rnd.setstate)
        >>> global_seed(0)  # try again
        >>> rnd.random()
        0.8444218515250481
        >>> global_seed(0)
        >>> rnd.random()  # the same
        0.8444218515250481

    """
    if name in _RANDOM_SOURCES:
        raise NameError(f'Name {name!r} already exist.')
    _RANDOM_SOURCES[name] = (seed, getstate, setstate)


def register_random_instance(name: str, rnd: random.Random):
    """
    Overview:
        Register custom random instance.

    :param name: Name of random source.
    :param rnd: Custom random instance, should be an instance of :class:`random.Random`.

    Examples::
        >>> import random
        >>> from hbutils.random import global_seed, register_random_instance
        >>>
        >>> rnd = random.Random()  # custom random object
        >>> global_seed(0)  # try to use same seed
        >>> rnd.random()
        0.48936053503964005
        >>> global_seed(0)
        >>> rnd.random()  # not same
        0.4113361070387721
        >>>
        >>> register_random_instance('custom_random', rnd)
        >>> global_seed(0)  # try again
        >>> rnd.random()
        0.8444218515250481
        >>> global_seed(0)
        >>> rnd.random()  # the same
        0.8444218515250481
    """
    register_random_source(name, rnd.seed, rnd.getstate, rnd.setstate)


def get_global_state() -> Dict[str, T]:
    """
    Overview:
        Get states of registered random sources.

    :returns: Global states.

    Examples::
        >>> import random
        >>> import numpy as np
        >>> import torch
        >>> from faker import Faker
        >>>
        >>> from hbutils.random import get_global_state, set_global_state
        >>>
        >>> _ = random.randint(0, 100)  # just do something
        >>> _ = random.random()
        >>> _ = torch.randn(2, 3)
        >>> _ = np.random.randn(2, 3)
        >>>
        >>> states = get_global_state()
        >>> random.randint(0, 100)  # first time's result
        99
        >>> random.random()
        0.4656250864192085
        >>> torch.randn(2, 3)
        tensor([[ 0.8886, -0.3602,  1.3071],
                [-0.0187, -0.5980, -0.5469]])
        >>> np.random.randn(2, 3)
        array([[ 1.24249156,  0.71018699, -0.53496231],
               [ 0.78748336, -0.01407442, -0.6607438 ]])
        >>> Faker().sentence(5)
        'New pass crime most.'
        >>>
        >>> set_global_state(states)
        >>> random.randint(0, 100)  # same as the first time
        99
        >>> random.random()
        0.4656250864192085
        >>> torch.randn(2, 3)
        tensor([[ 0.8886, -0.3602,  1.3071],
                [-0.0187, -0.5980, -0.5469]])
        >>> np.random.randn(2, 3)
        array([[ 1.24249156,  0.71018699, -0.53496231],
               [ 0.78748336, -0.01407442, -0.6607438 ]])
        >>> Faker().sentence(5)
        'New pass crime most.'
    """
    return {name: getstate() for name, (_, getstate, _) in _RANDOM_SOURCES.items()}


def set_global_state(states: Mapping[str, T]):
    """
    Overview:
        Set states of registered random sources.

    :param states: States to be set.

    Examples::
        See :func:`get_global_state`.
    """
    _skipped_names = set()
    _existing_names = set(_RANDOM_SOURCES.keys())
    for name, state in states.items():
        if name not in _existing_names:
            _skipped_names.add(name)
        else:
            _, _, setstate = _RANDOM_SOURCES[name]
            setstate(state)
            _existing_names.remove(name)

    if _skipped_names:
        _skipped_names = tuple(sorted(_skipped_names))
        warnings.warn(f'Random source {_skipped_names} skipped due to their non-existence in this environment.')

    if _existing_names:
        _existing_names = tuple(sorted(_existing_names))
        warnings.warn(f'Random source {_existing_names} not recovered because they are not provided.')


@contextmanager
def keep_global_state():
    """
    Overview:
        Keep all the states during this period.

    Examples::
        >>> import torch
        >>> from hbutils.random import global_seed, keep_global_state
        >>>
        >>> global_seed(0)
        >>> torch.randn(2, 3)  # before value 1
        tensor([[ 1.5410, -0.2934, -2.1788],
                [ 0.5684, -1.0845, -1.3986]])
        >>> torch.randn(2, 3)  # after value 1
        tensor([[ 0.4033,  0.8380, -0.7193],
                [-0.4033, -0.5966,  0.1820]])
        >>>
        >>> global_seed(0)
        >>> torch.randn(2, 3)  # before value 2, same as 1
        tensor([[ 1.5410, -0.2934, -2.1788],
                [ 0.5684, -1.0845, -1.3986]])
        >>> with keep_global_state():  # do anything you want here
        ...     _ = torch.randn(100, 200, 2)
        ...     _ = torch.randint(20, 30, (30, 40))
        >>> torch.randn(2, 3)  # after value 2, same as 1
        tensor([[ 0.4033,  0.8380, -0.7193],
                [-0.4033, -0.5966,  0.1820]])
    """
    states = get_global_state()
    try:
        yield
    finally:
        set_global_state(states)


def global_seed(seed: int):
    """
    Overview:
        Set seed for all registered random source.

    :param seed: Random seed.

    Examples::
        See :func:`keep_global_state` and :func:`register_random_instance`.

    """
    for _, (fseed, _, _) in _RANDOM_SOURCES.items():
        fseed(seed)


def seedable_func(func):
    """
    Overview:
        Wrap function to support seed.

    :param func: Function to be decorated, a new ``seed`` argument will be added.

    Examples::
        >>> import torch
        >>> from hbutils.random import seedable_func
        >>>
        >>> @seedable_func
        ... def get_random_value(mean, std):
        ...     return torch.randn((2, 3)) * std + mean
        >>>
        >>> get_random_value(2, 3)
        tensor([[-0.0844,  5.2530,  3.4248],
                [ 4.4923,  0.0492,  3.6731]])
        >>> get_random_value(2, 3)  # not the same
        tensor([[2.7600, 2.5135, 0.6484],
                [1.2459, 0.1020, 2.5905]])
        >>>
        >>> get_random_value(2, 3, seed=0)
        tensor([[ 6.6230,  1.1197, -4.5364],
                [ 3.7053, -1.2536, -2.1958]])
        >>> get_random_value(2, 3, seed=1)
        tensor([[3.9841, 2.8008, 2.1850],
                [3.8640, 0.6443, 1.5016]])
        >>> get_random_value(2, 3, seed=0)  # repeatable
        tensor([[ 6.6230,  1.1197, -4.5364],
                [ 3.7053, -1.2536, -2.1958]])
    """

    @wraps(func)
    def _new_func(*args, seed: int = None, **kwargs):
        if seed is not None:
            global_seed(seed)

        return func(*args, **kwargs)

    return _new_func


register_random_source('native_random', random.seed, random.getstate, random.setstate)

try:
    import numpy as np
except ImportError:
    pass
else:
    register_random_source('numpy', np.random.seed, np.random.get_state, np.random.set_state)

try:
    import torch
except ImportError:
    pass
else:
    register_random_source('torch', torch.manual_seed, torch.get_rng_state, torch.set_rng_state)

try:
    from faker import Faker
except ImportError:
    pass
else:
    _FAKER = Faker()
    register_random_instance('faker_default', _FAKER.random)
