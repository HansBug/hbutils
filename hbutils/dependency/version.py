from .grammar import _build_syntax
from ..model import asitems, hasheq


@hasheq()
@asitems(['version', 'cmp'])
class VersionSpec:
    def __init__(self, version, cmp):
        self.__version = version
        self.__cmp = cmp

    @property
    def version(self) -> str:
        return self.__version

    @property
    def cmp(self) -> str:
        return self.__cmp

    def __repr__(self):
        return f'{self.__cmp}{self.__version}'

    @classmethod
    def loads(cls, data) -> 'VersionSpec':
        if isinstance(data, VersionSpec):
            return data
        elif isinstance(data, tuple):
            return VersionSpec(data[1], data[0])
        elif isinstance(data, str):
            return cls.loads(_build_syntax(data).version_one())
        else:
            raise TypeError(f'Unknown version type - {repr(type(data))}.')
