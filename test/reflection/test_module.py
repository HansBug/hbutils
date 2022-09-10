import pytest

from hbutils.reflection import mount_pythonpath
from test.testings import get_testfile_path


@pytest.mark.unittest
class TestReflectionModule:
    def test_mount_pythonpath(self):
        with mount_pythonpath(get_testfile_path('igm')):
            from gf1 import FIXED
            assert FIXED == 1234567

        with mount_pythonpath(get_testfile_path('dir1')):
            from gf1 import FIXED
            assert FIXED == 233

        with mount_pythonpath(get_testfile_path('dir2')):
            from gf1 import FIXED
            assert FIXED == 455

    def test_mount_pythonpath_env(self):
        with mount_pythonpath(get_testfile_path('dir1')) as env1:
            from gf1 import FIXED
            assert FIXED == 233

        with mount_pythonpath(get_testfile_path('dir2')) as env2:
            from gf1 import FIXED
            assert FIXED == 455

        with env1.mount():
            from gf1 import FIXED, m1, m2
            assert FIXED == 233
            assert m1() == 10000
            assert m2() == 1061208

        with env2.mount(keep=False):
            from gf1 import FIXED, m1, m2
            assert FIXED == 455
            assert m1() == pytest.approx(1038365.9804592021)
            assert m2() == pytest.approx(135673.20093683453)
