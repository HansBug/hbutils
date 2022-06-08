import os.path

import pytest

from hbutils.system import touch, glob
from hbutils.testing import isolated_directory


@pytest.mark.unittest
class TestSystemFilesystemFile:
    def test_touch(self):
        with isolated_directory():
            touch('1/2/3/4/5.txt')
            touch('17.txt')
            assert os.path.exists('1/2/3/4/5.txt')
            assert os.path.exists('17.txt')

            touch('1/2/3/4/5.txt')
            with pytest.raises(OSError):
                touch('1/2/3/4/5.txt', exist_ok=False)

            with pytest.raises(OSError):
                touch('1/2/3/6/7.txt', makedirs=False)

    def test_glob(self):
        with isolated_directory():
            touch('1/2/3/4/5.txt')
            touch('1/2/3/5.txt')
            touch('1/2/3/4/6.txt')
            touch('1/4/7.txt')
            touch('7/147.txt')
            touch('17.txt')

            assert set(glob('1/2/3/4/*.txt')) == {
                '1/2/3/4/5.txt',
                '1/2/3/4/6.txt',
            }
            assert set(glob('1/**/5.txt')) == {
                '1/2/3/4/5.txt',
                '1/2/3/5.txt'
            }
            assert set(glob('**/*.txt')) == {
                '1/2/3/4/5.txt',
                '1/2/3/5.txt',
                '1/2/3/4/6.txt',
                '1/4/7.txt',
                '7/147.txt',
                '17.txt',
            }
            assert set(glob('**/')) == {'1/4/', '1/2/3/', '1/2/', '1/', '7/', '1/2/3/4/'}
