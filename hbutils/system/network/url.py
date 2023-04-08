import re
from dataclasses import dataclass
from typing import List, Tuple, Optional
from urllib import parse as urlparse

__all__ = [
    'urlsplit', 'SplitUrl',
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
class SplitUrl:
    url: str
    scheme: str
    host: str
    path: str
    query: str
    fragment: str

    @property
    def query_dict(self):
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
        return _split_path(self.path)

    @property
    def filename(self) -> Optional[str]:
        segments = self.path_segments
        if segments:
            return segments[-1]
        else:
            return None

    def __str__(self):
        return self.url

    def __repr__(self):
        content = ', '.join([f'{key}={value!r}' for key, value in [
            ('scheme', self.scheme),
            ('host', self.host),
            ('path', self.path),
            ('filename', self.filename),
            ('query', self.query_dict),
            ('fragment', self.fragment),
        ] if value])

        return f'{self.__class__.__name__}({content})'


def urlsplit(url) -> SplitUrl:
    splitted = urlparse.urlsplit(url)
    return SplitUrl(url, splitted.scheme, splitted.netloc, splitted.path, splitted.query, splitted.fragment)
