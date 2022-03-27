import pytest
from ometa.runtime import ParseError

from hbutils.dependency import Dependency
from hbutils.dependency.marker import MarkerExpr, EnvVar, MarkerOr, MarkerAnd
from hbutils.dependency.version import VersionSpec


@pytest.mark.unittest
class TestDependencyModel:
    def test_base(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        assert Dependency.loads(p) is p
        assert isinstance(p, Dependency)
        assert p.name == 'name'
        assert p.extras == ('quux', 'strange')
        assert p.versions == (VersionSpec('1.2', '>='), VersionSpec('3', '<'))
        assert p.mark == MarkerExpr(EnvVar('python_version'), '2.7', "~=")
        assert repr(p) == "name[quux,strange]>=1.2,<3; python_version ~= '2.7'"

        with pytest.raises(TypeError) as ei:
            Dependency.loads(None)
        err = ei.value
        assert isinstance(err, TypeError)
        assert err.args == ("Unknown dependency type - <class 'NoneType'>.",)

    def test_with_name(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.with_name('new_name')
        assert p.name == 'name'
        assert px.name == 'new_name'
        assert repr(px) == "new_name[quux,strange]>=1.2,<3; python_version ~= '2.7'"

        with pytest.raises(ParseError):
            p.with_name('^&^233')
        with pytest.raises(TypeError):
            p.with_name(233)

    def test_no_extra(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.no_extra()
        assert p.extras == ('quux', 'strange')
        assert px.extras == ()
        assert repr(px) == "name>=1.2,<3; python_version ~= '2.7'"

    def test_add_extras(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.add_extras('extra1', 'extra2')
        assert p.extras == ('quux', 'strange')
        assert px.extras == ('quux', 'strange', 'extra1', 'extra2')
        assert repr(px) == "name[quux,strange,extra1,extra2]>=1.2,<3; python_version ~= '2.7'"

        px = p.add_extras()
        assert px.extras == ('quux', 'strange')
        assert repr(px) == "name[quux,strange]>=1.2,<3; python_version ~= '2.7'"

        with pytest.raises(ParseError):
            p.add_extras('^&^233')
        with pytest.raises(TypeError):
            p.add_extras(233)

    def test_with_extras(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.with_extras('extra1', 'extra2')
        assert p.extras == ('quux', 'strange')
        assert px.extras == ('extra1', 'extra2')
        assert repr(px) == "name[extra1,extra2]>=1.2,<3; python_version ~= '2.7'"

        px = p.with_extras()
        assert px.extras == ()
        assert repr(px) == "name>=1.2,<3; python_version ~= '2.7'"

        with pytest.raises(ParseError):
            p.with_extras('^&^233')
        with pytest.raises(TypeError):
            p.with_extras(233)

    def test_no_version(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.no_version()
        assert p.versions == (VersionSpec('1.2', '>='), VersionSpec('3', '<'))
        assert px.versions == ()
        assert repr(px) == "name[quux,strange]; python_version ~= '2.7'"

    def test_add_versions(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.add_versions('~=8.5.4', '!=8.5.5+')
        assert p.versions == (VersionSpec('1.2', '>='), VersionSpec('3', '<'))
        assert px.versions == (VersionSpec('1.2', '>='), VersionSpec('3', '<'),
                               VersionSpec('8.5.4', '~='), VersionSpec('8.5.5+', '!='))
        assert repr(px) == "name[quux,strange]>=1.2,<3,~=8.5.4,!=8.5.5+; python_version ~= '2.7'"

        px = p.add_versions()
        assert px.versions == (VersionSpec('1.2', '>='), VersionSpec('3', '<'))
        assert repr(px) == "name[quux,strange]>=1.2,<3; python_version ~= '2.7'"

        with pytest.raises(ParseError):
            p.add_versions('^&^233')
        with pytest.raises(TypeError):
            p.add_versions(233)

        p = Dependency.loads("name[quux, strange]@http://foo.com ; python_version  ~= '2.7'")
        with pytest.raises(ValueError):
            p.add_versions('!=8.5.5+')

    def test_with_versions(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.with_versions('~=8.5.4', '!=8.5.5+')
        assert p.versions == (VersionSpec('1.2', '>='), VersionSpec('3', '<'))
        assert px.versions == (VersionSpec('8.5.4', '~='), VersionSpec('8.5.5+', '!='))
        assert repr(px) == "name[quux,strange]~=8.5.4,!=8.5.5+; python_version ~= '2.7'"

        px = p.with_versions()
        assert px.versions == ()
        assert repr(px) == "name[quux,strange]; python_version ~= '2.7'"

        with pytest.raises(ParseError):
            p.with_versions('^&^233')
        with pytest.raises(TypeError):
            p.with_versions(233)

        p = Dependency.loads("name[quux, strange]@http://foo.com ; python_version  ~= '2.7'")
        px = p.with_versions('!=8.5.5+')
        assert p.versions == 'http://foo.com'
        assert px.versions == (VersionSpec('8.5.5+', '!='),)
        assert repr(px) == "name[quux,strange]!=8.5.5+; python_version ~= '2.7'"

    def test_with_url(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.with_url('http://foo.com')
        assert p.versions == (VersionSpec('1.2', '>='), VersionSpec('3', '<'))
        assert px.versions == 'http://foo.com'
        assert repr(px) == "name[quux,strange]@http://foo.com ; python_version ~= '2.7'"

        with pytest.raises(ParseError):
            p.with_url('abc@#$%^&d___efg')
        with pytest.raises(TypeError):
            p.with_url(123)

    def test_no_mark(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.no_mark()
        assert p.mark == MarkerExpr(EnvVar('python_version'), '2.7', '~=')
        assert px.mark is None
        assert repr(px) == "name[quux,strange]>=1.2,<3"

    def test_with_mark(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.with_mark('platform_version == "Linux" or python_version >= "3.8"')
        assert p.mark == MarkerExpr(EnvVar('python_version'), '2.7', '~=')
        assert px.mark == MarkerOr(
            MarkerExpr(EnvVar('platform_version'), 'Linux', '=='),
            MarkerExpr(EnvVar('python_version'), '3.8', '>='),
        )
        assert repr(px) == "name[quux,strange]>=1.2,<3; platform_version == 'Linux' or python_version >= '3.8'"

    def test_and_mark(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.and_mark('platform_version == "Linux" or python_version >= "3.8"')
        assert p.mark == MarkerExpr(EnvVar('python_version'), '2.7', '~=')
        assert px.mark == MarkerAnd(
            MarkerExpr(EnvVar('python_version'), '2.7', '~='),
            MarkerOr(
                MarkerExpr(EnvVar('platform_version'), 'Linux', '=='),
                MarkerExpr(EnvVar('python_version'), '3.8', '>='),
            ),
        )
        assert repr(px) == "name[quux,strange]>=1.2,<3; python_version ~= '2.7' and " \
                           "(platform_version == 'Linux' or python_version >= '3.8')"

        p = Dependency.loads("name[quux, strange]>=1.2,<3")
        px = p.and_mark('platform_version == "Linux" or python_version >= "3.8"')
        assert p.mark is None
        assert px.mark == MarkerOr(
            MarkerExpr(EnvVar('platform_version'), 'Linux', '=='),
            MarkerExpr(EnvVar('python_version'), '3.8', '>='),
        )
        assert repr(px) == "name[quux,strange]>=1.2,<3; platform_version == 'Linux' or python_version >= '3.8'"

    def test_or_mark(self):
        p = Dependency.loads("name[quux, strange]>=1.2,<3; python_version  ~= '2.7'")
        px = p.or_mark('platform_version == "Linux" and python_version >= "3.8"')
        assert p.mark == MarkerExpr(EnvVar('python_version'), '2.7', '~=')
        assert px.mark == MarkerOr(
            MarkerExpr(EnvVar('python_version'), '2.7', '~='),
            MarkerAnd(
                MarkerExpr(EnvVar('platform_version'), 'Linux', '=='),
                MarkerExpr(EnvVar('python_version'), '3.8', '>='),
            ),
        )
        assert repr(px) == "name[quux,strange]>=1.2,<3; python_version ~= '2.7' or " \
                           "platform_version == 'Linux' and python_version >= '3.8'"

        p = Dependency.loads("name[quux, strange]>=1.2,<3")
        px = p.or_mark('platform_version == "Linux" and python_version >= "3.8"')
        assert p.mark is None
        assert px.mark == MarkerAnd(
            MarkerExpr(EnvVar('platform_version'), 'Linux', '=='),
            MarkerExpr(EnvVar('python_version'), '3.8', '>='),
        )
        assert repr(px) == "name[quux,strange]>=1.2,<3; platform_version == 'Linux' and python_version >= '3.8'"
