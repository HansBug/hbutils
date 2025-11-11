"""
Overview:
    Base interface to quickly implement a comparable object.
    
    This module provides the IComparable interface class that allows easy implementation
    of comparison operations (__eq__, __ne__, __lt__, __le__, __gt__, __ge__) for custom
    objects by only requiring the implementation of a single _cmpkey() method.
"""
import operator as ops

__all__ = [
    'IComparable',
]


class IComparable:
    """
    Overview:
        Interface for a comparable object.
        
        This class provides a base interface for creating comparable objects. Subclasses
        only need to implement the _cmpkey() method to enable all comparison operations.
        The comparison is based on the key values returned by _cmpkey().

    Examples::
        >>> from hbutils.model import IComparable
        >>> class MyValue(IComparable):
        ...     def __init__(self, v) -> None:
        ...         self._v = v
        ...
        ...     def _cmpkey(self):
        ...         return self._v
        ...

        >>> MyValue(1) == MyValue(1)
        True
        >>> MyValue(1) == MyValue(2)
        False
        >>> MyValue(1) != MyValue(2)
        True
        >>> MyValue(1) > MyValue(2)
        False
        >>> MyValue(1) >= MyValue(2)
        False
        >>> MyValue(1) < MyValue(2)
        True
        >>> MyValue(1) <= MyValue(2)
        True
    """

    def _cmpkey(self):
        """
        Function for getting a key value which is used for comparison.

        :return: A value used to compare.
        :raises NotImplementedError: This method must be implemented by subclasses.
        
        .. note::
            Subclasses must override this method to return a comparable value that
            represents the object for comparison purposes.
        """
        raise NotImplementedError  # pragma: no cover

    def _cmpcheck(self, op, other, default=False):
        """
        Internal method to perform comparison check between two objects.
        
        :param op: The comparison operator function to apply.
        :type op: callable
        :param other: The other object to compare with.
        :type other: object
        :param default: The default value to return if types don't match.
        :type default: bool
        
        :return: Result of the comparison operation.
        :rtype: bool
        
        .. note::
            This method checks if both objects are of the same type before performing
            the comparison. If types differ, it returns the default value.
        """
        if type(self) == type(other):
            return op(self._cmpkey(), other._cmpkey())
        else:
            return default

    def __eq__(self, other):
        """
        Check equality between two objects.
        
        :param other: The other object to compare with.
        :type other: object
        
        :return: True if objects are equal, False otherwise.
        :rtype: bool
        
        .. note::
            Returns True immediately if comparing with self (identity check).
            Otherwise, compares using _cmpkey() values if types match.
        """
        if self is other:
            return True
        else:
            return self._cmpcheck(ops.__eq__, other, default=False)

    def __ne__(self, other):
        """
        Check inequality between two objects.
        
        :param other: The other object to compare with.
        :type other: object
        
        :return: True if objects are not equal, False otherwise.
        :rtype: bool
        
        .. note::
            Returns False immediately if comparing with self (identity check).
            Otherwise, compares using _cmpkey() values if types match.
        """
        if self is other:
            return False
        else:
            return self._cmpcheck(ops.__ne__, other, default=True)

    def __lt__(self, other):
        """
        Check if this object is less than another object.
        
        :param other: The other object to compare with.
        :type other: object
        
        :return: True if this object is less than other, False otherwise.
        :rtype: bool
        """
        return self._cmpcheck(ops.__lt__, other)

    def __le__(self, other):
        """
        Check if this object is less than or equal to another object.
        
        :param other: The other object to compare with.
        :type other: object
        
        :return: True if this object is less than or equal to other, False otherwise.
        :rtype: bool
        """
        return self._cmpcheck(ops.__le__, other)

    def __gt__(self, other):
        """
        Check if this object is greater than another object.
        
        :param other: The other object to compare with.
        :type other: object
        
        :return: True if this object is greater than other, False otherwise.
        :rtype: bool
        """
        return self._cmpcheck(ops.__gt__, other)

    def __ge__(self, other):
        """
        Check if this object is greater than or equal to another object.
        
        :param other: The other object to compare with.
        :type other: object
        
        :return: True if this object is greater than or equal to other, False otherwise.
        :rtype: bool
        """
        return self._cmpcheck(ops.__ge__, other)
