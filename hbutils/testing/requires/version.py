"""
Module for handling version information with dynamic comparison capabilities.

This module provides a flexible VersionInfo class that wraps version information
and supports various input formats (strings, tuples, callables, etc.) with
comparison operations.
"""

from operator import lt, le, gt, ge

from packaging.version import Version


class VersionInfo:
    """
    Class for wrapping version information with dynamic comparison support.

    This class provides a flexible wrapper around version information that supports
    multiple input formats and allows for dynamic version resolution through callables.

    .. warning::
        This class is not immutable for its designing for dynamic comparison and boolean check.
        Please pay attention when use it.

    :param v: The version information, can be a VersionInfo, Version, callable, string, tuple, int, or None.
    :type v: Union[VersionInfo, Version, Callable, str, tuple, int, None]
    :raises TypeError: If the version type is not supported.

    Example::
        >>> v1 = VersionInfo('1.2.3')
        >>> v2 = VersionInfo((1, 2, 4))
        >>> v1 < v2
        True
        >>> v3 = VersionInfo(lambda: '1.3.0')
        >>> v1 < v3
        True
    """

    def __init__(self, v):
        """
        Initialize the VersionInfo instance.

        :param v: The version information to wrap.
        :type v: Union[VersionInfo, Version, Callable, str, tuple, int, None]
        :raises TypeError: If the version type is unknown or unsupported.
        """
        if isinstance(v, VersionInfo):
            self._version, self._func = v._version, None
        elif isinstance(v, Version) or v is None:
            self._version, self._func = v, None
        elif callable(v):
            self._version, self._func = None, v
        elif isinstance(v, str):
            VersionInfo.__init__(self, Version(v))
        elif isinstance(v, tuple):
            VersionInfo.__init__(self, '.'.join(map(str, v)))
        elif isinstance(v, int):
            VersionInfo.__init__(self, str(v))
        else:
            raise TypeError(f'Unknown version type - {repr(v)}.')

    @property
    def _actual_version(self):
        """
        Get the actual version value, resolving callables if necessary.

        :return: The resolved version object.
        :rtype: Version

        .. note::
            If the version was provided as a callable, this property will invoke
            the callable to get the actual version.
        """
        if self._func is None:
            return self._version
        else:
            return VersionInfo(self._func())._version

    def _cmp(self, cmp, other):
        """
        Internal comparison method for version comparison operations.

        :param cmp: The comparison operator function (lt, le, gt, ge).
        :type cmp: Callable[[Version, Version], bool]
        :param other: The other version to compare against.
        :type other: Union[VersionInfo, Version, str, tuple, int, None]
        :return: The result of the comparison, or False if either version is None.
        :rtype: bool
        """
        other = VersionInfo(other)
        if self and other:
            return cmp(self._actual_version, VersionInfo(other)._actual_version)
        else:
            return False

    def __lt__(self, other):
        """
        Check if this version is less than another version.

        :param other: The other version to compare against.
        :type other: Union[VersionInfo, Version, str, tuple, int, None]
        :return: True if this version is less than the other, False otherwise.
        :rtype: bool
        """
        return self._cmp(lt, other)

    def __le__(self, other):
        """
        Check if this version is less than or equal to another version.

        :param other: The other version to compare against.
        :type other: Union[VersionInfo, Version, str, tuple, int, None]
        :return: True if this version is less than or equal to the other, False otherwise.
        :rtype: bool
        """
        return self._cmp(le, other)

    def __gt__(self, other):
        """
        Check if this version is greater than another version.

        :param other: The other version to compare against.
        :type other: Union[VersionInfo, Version, str, tuple, int, None]
        :return: True if this version is greater than the other, False otherwise.
        :rtype: bool
        """
        return self._cmp(gt, other)

    def __ge__(self, other):
        """
        Check if this version is greater than or equal to another version.

        :param other: The other version to compare against.
        :type other: Union[VersionInfo, Version, str, tuple, int, None]
        :return: True if this version is greater than or equal to the other, False otherwise.
        :rtype: bool
        """
        return self._cmp(ge, other)

    def __eq__(self, other):
        """
        Check if this version is equal to another version.

        :param other: The other version to compare against.
        :type other: Union[VersionInfo, Version, str, tuple, int, None]
        :return: True if this version equals the other, False otherwise.
        :rtype: bool
        """
        return self._actual_version == VersionInfo(other)._actual_version

    def __ne__(self, other):
        """
        Check if this version is not equal to another version.

        :param other: The other version to compare against.
        :type other: Union[VersionInfo, Version, str, tuple, int, None]
        :return: True if this version does not equal the other, False otherwise.
        :rtype: bool
        """
        return self._actual_version != VersionInfo(other)._actual_version

    def __bool__(self):
        """
        Check if the version is truthy (not None).

        :return: True if the version is not None, False otherwise.
        :rtype: bool
        """
        return bool(self._actual_version)

    def __repr__(self):
        """
        Get the string representation of the VersionInfo object.

        :return: A string representation showing the class name and actual version.
        :rtype: str

        Example::
            >>> v = VersionInfo('1.2.3')
            >>> repr(v)
            '<VersionInfo 1.2.3>'
        """
        return f'<{type(self).__name__} {self._actual_version}>'
