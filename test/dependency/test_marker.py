import pytest

from hbutils.dependency.marker import EnvVar, load_marker, MarkerExpr, MarkerAnd, MarkerOr


@pytest.mark.unittest
class TestDependencyMarker:
    def test_env_var(self):
        ev = EnvVar('python_version')
        assert ev.name == 'python_version'
        assert repr(ev) == 'python_version'
        assert ev == EnvVar('python_version')
        assert ev != EnvVar('python_version ')

    def test_load_marker_expr(self):
        mark = load_marker("python_version<\"3\"")
        assert isinstance(mark, MarkerExpr)
        assert mark.first == EnvVar('python_version')
        assert mark.second == '3'
        assert mark.op == '<'
        assert repr(mark) == 'python_version < \'3\''
        assert mark == MarkerExpr(EnvVar("python_version"), "3", "<")

    # noinspection PyComparisonWithNone,PyDictCreation
    def test_load_marker_and(self):
        mark = load_marker('python_version<"3" and platform_version>="2.3"')
        assert isinstance(mark, MarkerAnd)
        assert len(mark) == 2
        first, second = mark
        assert first is mark[0]
        assert second is mark[1]
        assert first == MarkerExpr(EnvVar('python_version'), '3', '<')
        assert second == MarkerExpr(EnvVar('platform_version'), '2.3', '>=')

        assert mark == mark
        assert mark != None
        assert mark == load_marker('python_version<"3" and platform_version>="2.3"')

        d = {}
        d[mark] = 1
        assert d[load_marker('python_version<"3" and platform_version>="2.3"')] == 1

        c1 = load_marker('python_version<"3"')
        c2 = load_marker('platform_version>="2.3"')
        assert c1 & c2 == mark
        assert mark & c1 == load_marker('python_version<"3" and platform_version>="2.3" and python_version<"3"')
        assert c1 & mark == load_marker('python_version<"3" and (python_version<"3" and platform_version>="2.3")')
        assert mark & mark == load_marker('python_version<"3" and platform_version>="2.3" and '
                                          '(python_version<"3" and platform_version>="2.3")')
        assert repr(c1 & mark) == "python_version < '3' and (python_version < '3' and platform_version >= '2.3')"
        assert repr(mark & mark) == "python_version < '3' and platform_version >= '2.3' and " \
                                    "(python_version < '3' and platform_version >= '2.3')"
        assert repr((c1 | c2) & mark) == "(python_version < '3' or platform_version >= '2.3') and " \
                                         "(python_version < '3' and platform_version >= '2.3')"

    def test_load_marker_or(self):
        mark = load_marker('python_version<"3" or platform_version>="2.3"')
        assert isinstance(mark, MarkerOr)
        assert len(mark) == 2
        first, second = mark
        assert first is mark[0]
        assert second is mark[1]
        assert first == MarkerExpr(EnvVar('python_version'), '3', '<')
        assert second == MarkerExpr(EnvVar('platform_version'), '2.3', '>=')

        assert mark == mark
        assert mark != None
        assert mark != load_marker('python_version<"3" and platform_version>="2.3"')
        assert mark == load_marker('python_version<"3" or platform_version>="2.3"')

        d = {}
        d[mark] = 1
        assert d[load_marker('python_version<"3" or platform_version>="2.3"')] == 1

        c1 = load_marker('python_version<"3"')
        c2 = load_marker('platform_version>="2.3"')
        assert c1 | c2 == mark
        assert mark | c1 == load_marker('python_version<"3" or platform_version>="2.3" or python_version<"3"')
        assert c1 | mark == load_marker('python_version<"3" or (python_version<"3" or platform_version>="2.3")')
        assert mark | mark == load_marker('python_version<"3" or platform_version>="2.3" or '
                                          '(python_version<"3" or platform_version>="2.3")')
        assert repr(c1 | mark) == "python_version < '3' or (python_version < '3' or platform_version >= '2.3')"
        assert repr(mark | mark) == "python_version < '3' or platform_version >= '2.3' or " \
                                    "(python_version < '3' or platform_version >= '2.3')"
        assert repr(c1 & c2 | mark) == "python_version < '3' and platform_version >= '2.3' or " \
                                       "(python_version < '3' or platform_version >= '2.3')"

    def test_load_marker_func(self):
        mark = load_marker('python_version<"3" or platform_version>="2.3"')
        assert load_marker(mark) is mark
        with pytest.raises(TypeError) as ei:
            load_marker(None)
        err = ei.value
        assert isinstance(err, TypeError)
        assert err.args == ("Unknown marker type - <class 'NoneType'>.",)
