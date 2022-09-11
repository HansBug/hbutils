import sys

import pytest

from hbutils.testing import capture_exit


@pytest.mark.unittest
class TestTestingCaptureExit:
    def test_capture_exit_no_exit(self):
        with capture_exit() as e1:
            pass

        assert e1.exitcode == 0

        with capture_exit(None) as e2:
            pass

        assert e2.exitcode is None

    def test_capture_exit_quit(self):
        with capture_exit() as e1:
            quit(233)

        assert e1.exitcode == 233

        with capture_exit() as e2:
            quit()

        assert e2.exitcode == 0

        with capture_exit(None) as e3:
            quit()

        assert e3.exitcode == 0

    # noinspection PyUnreachableCode,PyUnusedLocal
    def test_capture_exit_sys_exit(self):
        with capture_exit() as e1:
            sys.exit(233)

        assert e1.exitcode == 233

        with capture_exit() as e2:
            sys.exit()

        assert e2.exitcode == 0

        with capture_exit(None) as e3:
            sys.exit()

        assert e3.exitcode == 0
