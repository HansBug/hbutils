"""
This module provides utilities for parsing and splitting URLs into their constituent components.

It offers a convenient way to decompose URLs into scheme, host, path, query parameters, and fragments,
with additional functionality to parse query parameters into dictionaries and extract path segments.
The module wraps Python's standard urllib.parse functionality with enhanced features for easier URL manipulation.

Main components:
- :class:`SplitURL`: A dataclass representing a parsed URL with convenient properties
- :func:`urlsplit`: Function to split a URL string into a SplitURL object
"""

import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from urllib import parse as urlparse

__all__ = [
    'urlsplit', 'SplitURL',
]


def _split_params(params: str) -> List[Tuple[str, Optional[str]]]:
    """
    Split URL query parameters string into a list of name-value pairs.

    :param params: The query parameters string to split.
    :type params: str

    :return: A list of tuples containing parameter names and their values (or None if no value).
    :rtype: List[Tuple[str, Optional[str]]]

    Example::
        >>> _split_params('q=1&v=kdjf&q=2')
        [('q', '1'), ('v', 'kdjf'), ('q', '2')]
        >>> _split_params('param1&param2=value')
        [('param1', None), ('param2', 'value')]
    """
    name_value_pairs = re.split(r'[&;]', params)
    result = []
    for name_value_pair in name_value_pairs:
        # Split the pair string into a naive, encoded (name, value) pair.
        name_value = name_value_pair.split('=', 1)

        if len(name_value) == 1:
            # 'param' => ('param', None)
            name, value = name_value[0], None
        else:
            # 'param=value' => ('param', 'value')
            # 'param=' => ('param', '')
            name, value = name_value

        name = urlparse.unquote_plus(name)
        if value is not None:
            value = urlparse.unquote_plus(value)

        result.append((name, value))

    return result


def _split_path(path: str) -> List[str]:
    """
    Split URL path into segments and decode each segment.

    :param path: The URL path string to split.
    :type path: str

    :return: A list of decoded path segments.
    :rtype: List[str]

    Example::
        >>> _split_path('/dslkjf/sdfhk/asdasd.png')
        ['', 'dslkjf', 'sdfhk', 'asdasd.png']
        >>> _split_path('/path%20with%20spaces/file.txt')
        ['', 'path with spaces', 'file.txt']
    """
    return [urlparse.unquote(segment) for segment in path.split('/')]


@dataclass
class SplitURL:
    """
    A dataclass representing a parsed URL with its constituent components.

    This class provides convenient access to URL components and additional
    properties for working with query parameters and path segments.

    :ivar url: The original URL string.
    :vartype url: str
    :ivar scheme: The URL scheme (e.g., 'http', 'https', 'ftp').
    :vartype scheme: str
    :ivar host: The host/netloc part of the URL.
    :vartype host: str
    :ivar path: The path component of the URL.
    :vartype path: str
    :ivar query: The query string (without the leading '?').
    :vartype query: str
    :ivar fragment: The fragment identifier (without the leading '#').
    :vartype fragment: str
    """
    url: str
    scheme: str
    host: str
    path: str
    query: str
    fragment: str

    @property
    def query_dict(self):
        """
        Parse the query string into a dictionary.

        When a query parameter appears multiple times, its values are stored as a list.
        Single-occurrence parameters are stored as single values.

        :return: A dictionary mapping parameter names to their values (or lists of values).
        :rtype: dict

        Example::
            >>> sp = urlsplit('https://example.com?q=1&v=kdjf&q=2')
            >>> sp.query_dict
            {'q': ['1', '2'], 'v': 'kdjf'}
        """
        retval = {}
        for key, value in _split_params(self.query or ''):
            if key in retval:
                if isinstance(retval[key], list):
                    retval[key].append(value)
                else:
                    retval[key] = [retval[key], value]
            else:
                retval[key] = value

        return retval

    @property
    def path_segments(self) -> List[str]:
        """
        Get the path split into individual segments.

        The path is split by '/' and each segment is URL-decoded.

        :return: A list of decoded path segments.
        :rtype: List[str]

        Example::
            >>> sp = urlsplit('https://example.com/path/to/file.txt')
            >>> sp.path_segments
            ['', 'path', 'to', 'file.txt']
        """
        return _split_path(self.path)

    @property
    def filename(self) -> Optional[str]:
        """
        Get the filename from the URL path.

        Returns the last segment of the path, or None if the path is empty.

        :return: The filename, or None if no path exists.
        :rtype: Optional[str]

        Example::
            >>> sp = urlsplit('https://example.com/path/to/file.txt')
            >>> sp.filename
            'file.txt'
            >>> sp = urlsplit('https://example.com')
            >>> sp.filename
            ''
        """
        return self.path_segments[-1]

    def __str__(self):
        """
        Get the original URL string.

        :return: The original URL.
        :rtype: str
        """
        return self.url

    def __repr__(self):
        """
        Get a detailed string representation of the SplitURL object.

        :return: A string representation showing all non-empty components.
        :rtype: str

        Example::
            >>> sp = urlsplit('https://example.com/path?q=1#frag')
            >>> repr(sp)
            "SplitURL(scheme='https', host='example.com', path='/path', query={'q': '1'}, fragment='frag')"
        """
        content = ', '.join([f'{key}={value!r}' for key, value in [
            ('scheme', self.scheme),
            ('host', self.host),
            ('path', self.path),
            ('query', self.query_dict),
            ('fragment', self.fragment),
        ] if value])

        return f'{self.__class__.__name__}({content})'


def urlsplit(url: str) -> SplitURL:
    """
    Split a URL into its constituent components.

    This function parses a URL string and returns a SplitURL object containing
    the scheme, host, path, query parameters, and fragment. It provides enhanced
    functionality over urllib.parse.urlsplit by offering convenient properties
    for accessing parsed query parameters and path segments.

    :param url: The URL string to split.
    :type url: str

    :return: A SplitURL object containing the parsed URL components.
    :rtype: SplitURL

    Examples::
        >>> from hbutils.system import urlsplit
        >>>
        >>> sp = urlsplit('https://www.baidu.com/dslkjf/sdfhk/asdasd.png?q=1&v=kdjf&q=2#fff')
        >>> sp
        SplitURL(scheme='https', host='www.baidu.com', path='/dslkjf/sdfhk/asdasd.png', query={'q': ['1', '2'], 'v': 'kdjf'}, fragment='fff')
        >>> repr(sp)
        "SplitURL(scheme='https', host='www.baidu.com', path='/dslkjf/sdfhk/asdasd.png', query={'q': ['1', '2'], 'v': 'kdjf'}, fragment='fff')"
        >>>
        >>> sp.scheme
        'https'
        >>> sp.host
        'www.baidu.com'
        >>> sp.path
        '/dslkjf/sdfhk/asdasd.png'
        >>> sp.query
        'q=1&v=kdjf&q=2'
        >>> sp.fragment
        'fff'
        >>>
        >>> sp.query_dict
        {'q': ['1', '2'], 'v': 'kdjf'}
        >>> sp.path_segments
        ['', 'dslkjf', 'sdfhk', 'asdasd.png']
        >>> sp.filename
        'asdasd.png'

    """
    splitted = urlparse.urlsplit(url)
    return SplitURL(url, splitted.scheme, splitted.netloc, splitted.path, splitted.query, splitted.fragment)
