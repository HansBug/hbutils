from operator import lt, le, gt, ge

from pkg_resources import parse_version

_Version = type(parse_version('0.0.1'))


class VersionInfo:
    def __init__(self, v):
        if isinstance(v, VersionInfo):
            self._version = v._version
        elif isinstance(v, _Version) or v is None:
            self._version = v
        elif isinstance(v, str):
            VersionInfo.__init__(self, parse_version(v))
        elif isinstance(v, tuple):
            VersionInfo.__init__(self, '.'.join(map(str, v)))
        elif isinstance(v, int):
            VersionInfo.__init__(self, str(v))
        else:
            raise TypeError(f'Unknown version type - {repr(v)}.')

    def _cmp(self, cmp, other):
        other = VersionInfo(other)
        if self and other:
            return cmp(self._version, VersionInfo(other)._version)
        else:
            return False

    def __lt__(self, other):
        return self._cmp(lt, other)

    def __le__(self, other):
        return self._cmp(le, other)

    def __gt__(self, other):
        return self._cmp(gt, other)

    def __ge__(self, other):
        return self._cmp(ge, other)

    def __eq__(self, other):
        return self._version == VersionInfo(other)._version

    def __ne__(self, other):
        return self._version != VersionInfo(other)._version

    def __bool__(self):
        return bool(self._version)

    def __repr__(self):
        return f'<{type(self).__name__} {self._version}>'
