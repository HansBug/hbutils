from operator import lt, le, gt, ge, eq, ne

from pkg_resources import parse_version

_Version = type(parse_version('0.0.1'))


class _VersionModel:
    def __init__(self, v):
        if isinstance(v, _VersionModel):
            self._version = v._version
        elif isinstance(v, _Version) or v is None:
            self._version = v
        elif isinstance(v, str):
            _VersionModel.__init__(self, parse_version(v))
        elif isinstance(v, tuple):
            _VersionModel.__init__(self, '.'.join(map(str, v)))
        else:
            raise TypeError(f'Unknown version type - {repr(v)}.')

    def _cmp(self, cmp, other):
        return cmp(self, _VersionModel(other))

    def __lt__(self, other):
        return self._cmp(lt, other)

    def __le__(self, other):
        return self._cmp(le, other)

    def __gt__(self, other):
        return self._cmp(gt, other)

    def __ge__(self, other):
        return self._cmp(ge, other)

    def __eq__(self, other):
        return self._cmp(eq, other)

    def __ne__(self, other):
        return self._cmp(ne, other)
