"""
Overview:
    Function operations for nested structure.
    
    This module provides utilities for applying functions to nested data structures
    (lists, tuples, and dictionaries) in a recursive manner. It allows mapping operations
    over complex nested structures while preserving their original types and hierarchy.
"""
from ..reflection import dynamic_call

__all__ = [
    'nested_map'
]


def nested_map(f, s):
    """
    Map the nested structure with a function.
    
    This function recursively traverses a nested structure (containing lists, tuples, 
    and dictionaries) and applies the given function to each leaf value. The function 
    can optionally accept the path to the current element as a parameter.

    :param f: The function to apply to each leaf value. Can accept 0, 1, or 2 parameters:
              - 0 params: Returns a constant value
              - 1 param: Receives the leaf value
              - 2 params: Receives the leaf value and its path (tuple of keys/indices)
    :type f: callable
    :param s: The nested structure to map over. Can be a dict, list, tuple, or any 
              combination thereof, with leaf values of any type.
    :type s: dict or list or tuple or any
    
    :return: A new nested structure with the same type and hierarchy as the input,
             but with the function applied to all leaf values.
    :rtype: Same type as input structure
    
    Examples::
        >>> from hbutils.collection import nested_map
        >>> nested_map(lambda x: x + 1, [
        ...     2, 3, (4, {'x': 2, 'y': 4}),
        ...     {'a': 3, 'b': (4, 5)},
        ... ])
        [3, 4, (5, {'x': 3, 'y': 5}), {'a': 4, 'b': (5, 6)}]
        >>> nested_map(lambda x, p: (x + 1) *  len(p), [
        ...     2, 3, (4, {'x': 2, 'y': 4}),
        ...     {'a': 3, 'b': (4, 5)},
        ... ])
        [3, 4, (10, {'x': 9, 'y': 15}), {'a': 8, 'b': (15, 18)}]
        >>> nested_map(lambda: 233, [
        ...     2, 3, (4, {'x': 2, 'y': 4}),
        ...     {'a': 3, 'b': (4, 5)},
        ... ])
        [233, 233, (233, {'x': 233, 'y': 233}), {'a': 233, 'b': (233, 233)}]
    """
    _df = dynamic_call(f)

    def _recursion(sval, p):
        """
        Recursively traverse and map the nested structure.
        
        :param sval: The current value being processed
        :type sval: any
        :param p: The path to the current value (tuple of keys/indices)
        :type p: tuple
        
        :return: The mapped value or structure
        :rtype: any
        """
        if isinstance(sval, dict):
            return type(sval)({k: _recursion(v, (*p, k)) for k, v in sval.items()})
        elif isinstance(sval, (list, tuple)):
            return type(sval)(_recursion(v, (*p, i)) for i, v in enumerate(sval))
        else:
            return _df(sval, p)

    return _recursion(s, ())
