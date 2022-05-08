import os.path

import pytest

from hbutils.system import touch
from hbutils.testing import isolated_directory


@pytest.mark.unittest
class TestSystemFilesystemFile:
    def test_touch(self):
        with isolated_directory():
            touch('1/2/3/4/5.txt')
            assert os.path.exists('1/2/3/4/5.txt')

            touch('1/2/3/4/5.txt')
            with pytest.raises(OSError):
                touch('1/2/3/4/5.txt', exist_ok=False)

            with pytest.raises(OSError):
                touch('1/2/3/6/7.txt', makedirs=False)
