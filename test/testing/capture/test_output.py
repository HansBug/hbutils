import sys
from textwrap import dedent

import pytest

from hbutils.testing import capture_output, disable_output


@pytest.mark.unittest
class TestTestingCaptureOutput:
    def test_capture_output(self):
        with capture_output() as r:
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
