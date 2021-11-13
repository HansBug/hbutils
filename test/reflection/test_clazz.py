import pytest

from hbutils.reflection import class_wraps, visual


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

    def test_visual(self):
        @visual()
        class T:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        t = T(1, 2)
        assert repr(t) in {
            '<T x: 1, y: 2>',
            '<T y: 2, x: 1>',
        }

        @visual(['y', 'x'])
        class T1:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        assert repr(T1(1, 2)) == '<T1 y: 2, x: 1>'

        @visual([])
        class T2:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        assert repr(T2(1, 2)) == '<T2>'

        @visual(['x', 'y'], show_id=True)
        class T3:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        t = T3(1, 2)
        assert repr(t) == f'<T3 {hex(id(t))} x: 1, y: 2>'

        def _display_ox(v):
            return 'x' if v else 'o'

        @visual([('x', _display_ox), ('y', _display_ox)])
        class T4:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        assert repr(T4(True, False)) == '<T4 x: x, y: o>'

        def _display_ox_2(v):
            if v:
                return 'yes'
            else:
                raise ValueError

        @visual([('x', _display_ox_2), ('y', _display_ox_2)])
        class T5:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        assert repr(T5(True, False)) == '<T5 x: yes>'
