from hbutils.system import is_cpython, is_pypy, is_jython, is_ironpython
from ...testings import cpython_mark, pypy_mark


class TestSystemPythonImplementation:
    @cpython_mark
    def test_is_cpython(self):
        assert is_cpython()
        assert not is_pypy()
        assert not is_jython()
        assert not is_ironpython()

    @pypy_mark
    def test_is_pypy(self):
        assert not is_cpython()
        assert is_pypy()
        assert not is_jython()
        assert not is_ironpython()
