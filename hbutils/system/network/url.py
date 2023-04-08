import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from urllib import parse as urlparse

__all__ = [
    'urlsplit', 'SplitURL',
]


def _split_params(params: str) -> List[Tuple[str, Optional[str]]]:
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
    return [urlparse.unquote(segment) for segment in path.split('/')]


@dataclass
class SplitURL:
    """
    Overview:
        Splitted url object.
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
        Query dict.
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
        Separated path segments.
        """
        return _split_path(self.path)

    @property
    def filename(self) -> Optional[str]:
        """
        Filename of current url, return ``None`` when path is empty.
        """
        return self.path_segments[-1]

    def __str__(self):
        """
        Original url.
        """
        return self.url

    def __repr__(self):
        """
        Repr format of :class:`SplitURL`.
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
    Overview:
        Split url into 5 parts (scheme, host, path, query and fragment).

    :param url: Original url string.
    :return: :class:`SplitURL` object.

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
