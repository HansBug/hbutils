import subprocess
import sys

import pytest

from hbutils.testing import isolated_stdin, isolated_directory


@pytest.mark.unittest
class TestTestingIsolatedInput:
    @pytest.mark.parametrize(['mem', ], [(True,), (False,)])
    def test_isolated_stdin_with_list(self, mem):
        with isolated_stdin(['123', '456'], mem=mem):
            a = int(input())
            b = int(input())
            assert a == 123
            assert b == 456

    @pytest.mark.parametrize(['mem', ], [(True,), (False,)])
    def test_isolated_stdin_with_str(self, mem):
        with isolated_stdin('123\n456', mem=mem):
            a = int(input())
            b = int(input())
            assert a == 123
            assert b == 456

    def test_isolated_stdin_to_subprocess(self):
        with isolated_directory():
            with open('main.py', 'w+') as f:
                print('a = int(input())', file=f)
                print('b = int(input())', file=f)
                print('print(a, b, a + b)', file=f)

            with isolated_stdin(['123', '456']):
                process = subprocess.run([sys.executable, 'main.py'], stdin=sys.stdin, capture_output=True)
                process.check_returncode()
                assert process.stdout.strip() == b'123 456 579'

    def test_isolated_stdin_invalid_type(self):
        with pytest.raises(TypeError):
            with isolated_stdin(None):
                pytest.fail('Should not reach here')
