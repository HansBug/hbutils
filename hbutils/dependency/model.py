import io
from functools import partial
from typing import Union, Tuple

from .grammar import _build_syntax
from .marker import load_marker, MarkerExpr, MarkerAnd, MarkerOr, _load_marker_from_data
from .version import VersionSpec
from ..model import asitems, hasheq


def load_name(name: str):
    if isinstance(name, str):
        return _build_syntax(name).name()
    else:
        raise TypeError(f'Invalid name - str expected but {repr(name)} found.')


def load_extra(extra: str):
    if isinstance(extra, str):
        return _build_syntax(extra).extra()
    else:
        raise TypeError(f'Invalid extra - str expected but {repr(extra)} found.')


def load_url(url: str):
    if isinstance(url, str):
        return _build_syntax(url).URI_reference()
    else:
        raise TypeError(f'Invalid url - str expected but {repr(url)} found.')


@hasheq()
@asitems(['name', 'extras', 'versions', 'mark'])
class Dependency:
    def __init__(self, name, extras, versions, mark):
        self.__name = name
        self.__extras = tuple(extras)
        self.__versions = tuple(versions) if isinstance(versions, (list, tuple)) else str(versions)
        self.__mark = mark

    @property
    def name(self) -> str:
        return self.__name

    @property
    def extras(self) -> Tuple[str, ...]:
        return self.__extras

    @property
    def versions(self) -> Union[Tuple[VersionSpec, ...], str]:
        return self.__versions

    @property
    def mark(self) -> Union[MarkerOr, MarkerAnd, MarkerExpr, None]:
        return self.__mark

    def __repr__(self):
        with io.StringIO() as sio:
            lprint = partial(print, file=sio, end='')
            lprint(self.__name)
            if self.__extras:
                lprint('[' + ','.join(map(str, self.__extras)) + ']')
            if self.__versions:
                if isinstance(self.__versions, str):
                    lprint('@' + self.__versions + ' ')
                else:
                    lprint(','.join(map(repr, self.__versions)))
            if self.__mark is not None:
                lprint(';', self.__mark)

            return sio.getvalue().strip()

    def with_name(self, name: str) -> 'Dependency':
        return self.__class__(load_name(name), self.__extras, self.__versions, self.__mark)

    def no_extra(self) -> 'Dependency':
        return self.with_extras()

    def add_extras(self, *exts: str) -> 'Dependency':
        return self.__class__(self.__name, [*self.__extras, *map(load_extra, exts)],
                              self.__versions, self.__mark)

    def with_extras(self, *exts: str) -> 'Dependency':
        return self.__class__(self.__name, [*map(load_extra, exts)], self.__versions, self.__mark)

    def no_version(self) -> 'Dependency':
        return self.with_versions()

    def add_versions(self, *vers) -> 'Dependency':
        if isinstance(self.__versions, str):
            raise ValueError(f'URL version {repr(self.__versions)} is used, adding of versions is not available.')
        else:
            return self.__class__(self.__name, self.__extras,
                                  [*self.__versions, *map(VersionSpec.loads, vers)], self.__mark)

    def with_versions(self, *vers) -> 'Dependency':
        return self.__class__(self.__name, self.__extras,
                              [*map(VersionSpec.loads, vers)], self.__mark)

    def with_url(self, url: str) -> 'Dependency':
        return self.__class__(self.__name, self.__extras, load_url(url), self.__mark)

    def no_mark(self) -> 'Dependency':
        return self.__class__(self.__name, self.__extras, self.__versions, None)

    def with_mark(self, mark) -> 'Dependency':
        return self.__class__(self.__name, self.__extras, self.__versions, load_marker(mark))

    def and_mark(self, mark) -> 'Dependency':
        if self.__mark is not None:
            return self.__class__(self.__name, self.__extras,
                                  self.__versions, self.__mark & load_marker(mark))
        else:
            return self.with_mark(mark)

    def or_mark(self, mark) -> 'Dependency':
        if self.__mark is not None:
            return self.__class__(self.__name, self.__extras,
                                  self.__versions, self.__mark | load_marker(mark))
        else:
            return self.with_mark(mark)

    @classmethod
    def loads(cls, data) -> 'Dependency':
        if isinstance(data, Dependency):
            return data
        elif isinstance(data, str):
            name, extras, vers, marks = _build_syntax(data).specification()
            if marks is not None:
                marks = _load_marker_from_data(marks)
            if isinstance(vers, (list, tuple)):
                vers = tuple(map(VersionSpec.loads, vers))

            return Dependency(name, extras, vers, marks)
        else:
            raise TypeError(f'Unknown dependency type - {repr(type(data))}.')
