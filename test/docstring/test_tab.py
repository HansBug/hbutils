import pytest

from hbutils.docstring import untab


@pytest.mark.unittest
class TestDocstringTab:
    def test_untab(self):
        def func(a, b):
            """
            Overview:
                This is function ``func``.

            Args:
                - a: First argument
                - b: Second argument
            """
            pass

        assert func.__doc__ == """
            Overview:
                This is function ``func``.

            Args:
                - a: First argument
                - b: Second argument
            """
        assert untab(func.__doc__) == """
Overview:
    This is function ``func``.

Args:
    - a: First argument
    - b: Second argument
"""
