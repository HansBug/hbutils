import pytest

from hbutils.dependency import parse_dependency, Dependency
from hbutils.dependency.marker import MarkerExpr, EnvVar, MarkerAnd, MarkerOr
from hbutils.dependency.version import VersionSpec


@pytest.mark.unittest
class TestDependencyParse:
    def test_parse_dependency_simple(self):
        p = parse_dependency('my-pypi')
        assert isinstance(p, Dependency)
        assert p.name == 'my-pypi'
        assert p.extras == ()
        assert p.versions == ()
        assert p.mark is None
        assert repr(p) == 'my-pypi'

        p = parse_dependency("A.B-C_D")
        assert isinstance(p, Dependency)
        assert p.name == "A.B-C_D"
        assert p.extras == ()
        assert p.versions == ()
        assert p.mark is None
        assert repr(p) == 'A.B-C_D'

    def test_parse_dependency_with_extra(self):
        p = parse_dependency('my-pypi[test]')
        assert isinstance(p, Dependency)
        assert p.name == 'my-pypi'
        assert p.extras == ('test',)
        assert p.versions == ()
        assert p.mark is None
        assert repr(p) == 'my-pypi[test]'

        p = parse_dependency('my-pypi[test ,   extra]')
        assert isinstance(p, Dependency)
        assert p.name == 'my-pypi'
        assert p.extras == ('test', 'extra')
        assert p.versions == ()
        assert p.mark is None
        assert repr(p) == 'my-pypi[test,extra]'

    def test_parse_dependency_with_versions(self):
        p = parse_dependency('name>=1.0,<8.3')
        assert isinstance(p, Dependency)
        assert p.name == 'name'
        assert p.extras == ()
        assert p.versions == (VersionSpec('1.0', '>='), VersionSpec('8.3', '<'))
        assert p.mark is None
        assert repr(p) == 'name>=1.0,<8.3'

        p = parse_dependency('name >= 1.0   ')
        assert isinstance(p, Dependency)
        assert p.name == 'name'
        assert p.extras == ()
        assert p.versions == (VersionSpec('1.0', '>='),)
        assert p.mark is None
        assert repr(p) == 'name>=1.0'

    def test_parse_dependency_with_url(self):
        p = parse_dependency("name@http://foo.com")
        assert isinstance(p, Dependency)
        assert p.name == 'name'
        assert p.extras == ()
        assert p.versions == 'http://foo.com'
        assert p.mark is None
        assert repr(p) == 'name@http://foo.com'

        p = parse_dependency("name [fred,bar] @ http://foo.com")
        assert isinstance(p, Dependency)
        assert p.name == 'name'
        assert p.extras == ('fred', 'bar')
        assert p.versions == 'http://foo.com'
        assert p.mark is None
        assert repr(p) == 'name[fred,bar]@http://foo.com'

    def test_parse_dependency_with_marks(self):
        p = parse_dependency("name[quux, strange]; python_version  ~= '2.7'")
        assert isinstance(p, Dependency)
        assert p.name == 'name'
        assert p.extras == ('quux', 'strange')
        assert p.versions == ()
        assert p.mark == MarkerExpr(EnvVar('python_version'), '2.7', "~=")
        assert repr(p) == "name[quux,strange]; python_version ~= '2.7'"

        p = parse_dependency("name[quux, strange];python_version<'2.7' and platform_version=='2'")
        assert isinstance(p, Dependency)
        assert p.name == 'name'
        assert p.extras == ('quux', 'strange')
        assert p.versions == ()
        assert p.mark == MarkerAnd(
            MarkerExpr(EnvVar('python_version'), '2.7', "<"),
            MarkerExpr(EnvVar('platform_version'), '2', "=="),
        )
        assert repr(p) == "name[quux,strange]; python_version < '2.7' and platform_version == '2'"

        p = parse_dependency(
            "name[quux, strange];python_version>='3.3' or python_version<'2.7' and platform_version=='2'")
        assert isinstance(p, Dependency)
        assert p.name == 'name'
        assert p.extras == ('quux', 'strange')
        assert p.versions == ()
        assert p.mark == MarkerOr(
            MarkerExpr(EnvVar('python_version'), '3.3', ">="),
            MarkerAnd(
                MarkerExpr(EnvVar('python_version'), '2.7', "<"),
                MarkerExpr(EnvVar('platform_version'), '2', "=="),
            ),
        )
        assert repr(p) == "name[quux,strange]; python_version >= '3.3' or " \
                          "python_version < '2.7' and platform_version == '2'"
