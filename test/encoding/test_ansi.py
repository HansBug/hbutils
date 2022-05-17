from textwrap import dedent

import pytest

from hbutils.encoding import ansi_unescape


@pytest.mark.unittest
class TestEncodingAnsi:
    def test_ansi_unescape(self):
        assert ansi_unescape(dedent("""
            \x1b[1;31mHello
            \x1b[2;37;41mWorld
        """).strip()) == dedent("""
            Hello
            World
        """).strip()
