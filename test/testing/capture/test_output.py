import subprocess
import sys
from textwrap import dedent

import pytest
from tqdm.auto import tqdm

from hbutils.testing import capture_output, disable_output, isolated_directory


@pytest.mark.unittest
class TestTestingCaptureOutput:
    @pytest.mark.parametrize(['mem'], [(True,), (False,)])
    def test_capture_output(self, mem):
        with capture_output(mem=mem) as r:
            print('This is stdout.')
            print('This is stderr.', file=sys.stderr)
            print('This is stdout line 2.')
            print('This is stderr 2rd line.', file=sys.stderr)

        assert dedent(r.stdout).strip() == dedent("""
            This is stdout.
            This is stdout line 2.
        """).strip()
        assert dedent(r.stderr).strip() == dedent("""
            This is stderr.
            This is stderr 2rd line.
        """).strip()

    def test_capture_output_with_subprocess_run(self):
        with isolated_directory():
            with open('main.py', 'w') as f:
                print('print("This is output")', file=f)
                print('print("This is output 2")', file=f)
                print('import sys', file=f)
                print('print("This is output x", file=sys.stderr)', file=f)

            with capture_output() as r:
                process = subprocess.run([sys.executable, 'main.py'], stdout=sys.stdout, stderr=sys.stderr)
                process.check_returncode()

            assert list(map(str.strip, r.stdout.strip().splitlines())) == [
                'This is output',
                'This is output 2'
            ]
            assert list(map(str.strip, r.stderr.strip().splitlines())) == [
                'This is output x'
            ]

    def test_disable_output(self):
        with capture_output() as r:
            print('This is stdout.')
            with disable_output():
                print('This is stderr.', file=sys.stderr)
                print('This is stdout line 2.')

            print('This is stderr 2rd line.', file=sys.stderr)
            with disable_output():
                print('This is stdout line 3.')

            print('This is stderr 3rd line.', file=sys.stderr)

        assert dedent(r.stdout).strip() == dedent("""
            This is stdout.
        """).strip()
        assert dedent(r.stderr).strip() == dedent("""
            This is stderr 2rd line.
            This is stderr 3rd line.
        """).strip()

    def test_disable_output_with_tqdm(self):
        with capture_output() as r:
            with disable_output():
                f = tqdm(total=10)
                f.set_description('你好，这个是中文')
                f.update(5)

        assert not r.stdout.strip()
        assert not r.stderr.strip()
