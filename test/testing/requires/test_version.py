from functools import partial

import pytest
from pkg_resources import parse_version

from hbutils.testing.requires.version import VersionInfo


@pytest.mark.unittest
class TestTestingRequiresVersion:
    def test_init(self):
        assert VersionInfo(None)._version is None
        assert VersionInfo('3.6.3') == parse_version('3.6.3')
        assert VersionInfo((3, 6, 3)) == parse_version('3.6.3')
        assert VersionInfo(VersionInfo('3.6.3')) == parse_version('3.6.3')
        assert VersionInfo(7) == parse_version('7')
        with pytest.raises(TypeError):
            _ = VersionInfo(233.238459)

        def _get_version(v):
            try:
                return next(v)
            except StopIteration:
                return None

        vi = VersionInfo(partial(_get_version, iter(['3.6.3', '3.6.2', '3.8.1'])))
        assert vi == '3.6.3'
        assert vi == '3.6.2'
        assert vi == '3.8.1'
        assert not vi

    def test_bool(self):
        assert not VersionInfo(None)
        assert VersionInfo('3.6.3')
        assert VersionInfo((3, 6, 3))
        assert VersionInfo(VersionInfo('3.6.3'))
        assert not VersionInfo(VersionInfo(None))

    def test_eq(self):
        assert VersionInfo(None) == VersionInfo(None)
        assert not (VersionInfo(None) == VersionInfo('3.6.3'))
        assert VersionInfo('3.6.3') == VersionInfo((3, 6, 3))
        assert not (VersionInfo('3.6.3') == VersionInfo('3.6.2'))

    def test_ne(self):
        assert not (VersionInfo(None) != VersionInfo(None))
        assert VersionInfo(None) != VersionInfo('3.6.3')
        assert not (VersionInfo('3.6.3') != VersionInfo((3, 6, 3)))
        assert VersionInfo('3.6.3') != VersionInfo('3.6.2')

    def test_lt(self):
        assert VersionInfo('3.6.3') < VersionInfo('3.6.4')
        assert VersionInfo('3.6.3') < '3.6.4'
        assert not (VersionInfo('3.6.3') < '3.6.3')
        assert not (VersionInfo('3.6.3') < '3.6.2')
        assert not (VersionInfo('3.6.3') < None)
        assert not (VersionInfo(None) < '3.6.3')

    def test_le(self):
        assert VersionInfo('3.6.3') <= VersionInfo('3.6.4')
        assert VersionInfo('3.6.3') <= '3.6.4'
        assert VersionInfo('3.6.3') <= '3.6.3'
        assert not (VersionInfo('3.6.3') <= '3.6.2')
        assert not (VersionInfo('3.6.3') <= None)
        assert not (VersionInfo(None) <= '3.6.3')

    def test_gt(self):
        assert VersionInfo('3.6.3') > VersionInfo('3.6.2')
        assert not (VersionInfo('3.6.3') > '3.6.4')
        assert not (VersionInfo('3.6.3') > '3.6.3')
        assert VersionInfo('3.6.3') > '3.6.2'
        assert not (VersionInfo('3.6.3') > None)
        assert not (VersionInfo(None) > '3.6.3')

    def test_ge(self):
        assert VersionInfo('3.6.3') >= VersionInfo('3.6.2')
        assert not (VersionInfo('3.6.3') >= '3.6.4')
        assert VersionInfo('3.6.3') >= '3.6.3'
        assert VersionInfo('3.6.3') >= '3.6.2'
        assert not (VersionInfo('3.6.3') >= None)
        assert not (VersionInfo(None) >= '3.6.3')

    def test_repr(self):
        assert repr(VersionInfo(None)) == '<VersionInfo None>'
        assert repr(VersionInfo('3.6.3')) == '<VersionInfo 3.6.3>'
        assert repr(VersionInfo((3, 6, 3))) == '<VersionInfo 3.6.3>'
