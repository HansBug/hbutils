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
