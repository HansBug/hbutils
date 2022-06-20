import pytest

from hbutils.dependency.version import VersionSpec


@pytest.mark.unittest
class TestDependencyVersion:
    def test_version_spec(self):
        vs = VersionSpec('0.0.1', '>=')
        assert vs.version == '0.0.1'
        assert vs.cmp == '>='
        assert repr(vs) == '>=0.0.1'
        assert vs == VersionSpec('0.0.1', '>=')
        assert vs != VersionSpec('0.0.1', '<=')

    def test_version_spec_loads(self):
        vs = VersionSpec('0.0.1', '>=')
        assert VersionSpec.loads(vs) is vs
        assert VersionSpec.loads('>=0.0.1') == vs
        assert VersionSpec.loads(('>=', '0.0.1')) == vs
        with pytest.raises(TypeError) as ei:
            VersionSpec.loads(123)
        err = ei.value
        assert isinstance(err, TypeError)
        assert err.args == ("Unknown version type - <class 'int'>.",)
