from operator import lt, le, gt, ge

from pkg_resources import parse_version

_Version = type(parse_version('0.0.1'))


class VersionInfo:
    """
    Overview:
        Class for wrapping version information.

    .. warning::
        This class is not immutable for its designing for dynamic comparison and boolean check.
        Please pay attention when use it.
    """

    def __init__(self, v):
        if isinstance(v, VersionInfo):
            self._version, self._func = v._version, None
        elif isinstance(v, _Version) or v is None:
            self._version, self._func = v, None
        elif callable(v):
            self._version, self._func = None, v
        elif isinstance(v, str):
            VersionInfo.__init__(self, parse_version(v))
        elif isinstance(v, tuple):
            VersionInfo.__init__(self, '.'.join(map(str, v)))
        elif isinstance(v, int):
            VersionInfo.__init__(self, str(v))
        else:
            raise TypeError(f'Unknown version type - {repr(v)}.')

    @property
    def _actual_version(self):
        if self._func is None:
            return self._version
        else:
            return VersionInfo(self._func())._version

    def _cmp(self, cmp, other):
        other = VersionInfo(other)
        if self and other:
            return cmp(self._actual_version, VersionInfo(other)._actual_version)
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
        return self._actual_version == VersionInfo(other)._actual_version

    def __ne__(self, other):
        return self._actual_version != VersionInfo(other)._actual_version

    def __bool__(self):
        return bool(self._actual_version)

    def __repr__(self):
        return f'<{type(self).__name__} {self._actual_version}>'
