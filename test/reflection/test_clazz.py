import pytest

from hbutils.reflection import class_wraps


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestReflectionClazz:
    def test_class_wraps(self):
        def add_sum(cls: type):
            @class_wraps(cls)
            class _NewClass(cls):
                def sum(self):
                    return self.a + self.b

            return _NewClass

        @add_sum
        class _MyContainer:
            """
            This is a mark for __doc__
            """

            def __init__(self, a, b):
                self.a, self.b = a, b

            def __repr__(self):
                return f'<{self.__class__.__name__} a: {self.a}, b: {self.b}>'

        assert _MyContainer(1, 2).sum() == 3
        assert _MyContainer.__name__ == '_MyContainer'
        assert 'a mark for __doc__' in _MyContainer.__doc__
