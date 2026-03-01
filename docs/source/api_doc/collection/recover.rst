hbutils.collection.recover
========================================================

.. currentmodule:: hbutils.collection.recover

.. automodule:: hbutils.collection.recover


\_\_all\_\_
-----------------------------------------------------

.. autodata:: __all__


BaseRecovery
-----------------------------------------------------

.. autoclass:: BaseRecovery
    :members: __init__,recover,from_origin,__rtype__


DictRecovery
-----------------------------------------------------

.. autoclass:: DictRecovery
    :members: __init__,from_origin,__rtype__


TupleRecovery
-----------------------------------------------------

.. autoclass:: TupleRecovery
    :members: __init__,from_origin,__rtype__


ListRecovery
-----------------------------------------------------

.. autoclass:: ListRecovery
    :members: __init__,from_origin,__rtype__


NullRecovery
-----------------------------------------------------

.. autoclass:: NullRecovery
    :members: from_origin,__rtype__


GenericObjectRecovery
-----------------------------------------------------

.. autoclass:: GenericObjectRecovery
    :members: __init__,from_origin,__rtype__


register\_recovery
-----------------------------------------------------

.. autofunction:: register_recovery


get\_recovery\_func
-----------------------------------------------------

.. autofunction:: get_recovery_func


