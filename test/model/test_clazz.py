import pytest

from hbutils.model import visual, constructor, asitems, hasheq, accessor, get_field


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestModelClazz:
    def test_asitems(self):
        @asitems(['x', 'y'])
        class T:
            pass

        assert T.__items__ == ['x', 'y']

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

        @visual()
        @asitems(['x'])
        class T6:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        assert repr(T6(1, 2)) == '<T6 x: 1>'

    def test_constructor(self):
        @constructor(['x', ('y', 2)], doc="This is constructor of T.")
        class T:
            @property
            def x(self):
                return self.__x

            @property
            def y(self):
                return self.__y

        t = T(100, 20)
        assert t.x == 100
        assert t.y == 20

        t = T(100)
        assert t.x == 100
        assert t.y == 2

        assert T.__init__.__doc__ == "This is constructor of T."

        with pytest.raises(TypeError):
            T(y=2)

        with pytest.raises(SyntaxError):
            @constructor([('x', 1), 'y'])
            class T1:
                @property
                def x(self):
                    return self.__x

                @property
                def y(self):
                    return self.__y

        @constructor(doc="This is constructor of T.")
        @asitems(['x', 'y'])
        class T2:
            @property
            def x(self):
                return self.__x

            @property
            def y(self):
                return self.__y

        t = T2(100, 20)
        assert t.x == 100
        assert t.y == 20

        assert T2.__init__.__doc__ == "This is constructor of T."

    # noinspection PyComparisonWithNone
    def test_hasheq(self):
        @hasheq(['x', 'y'])
        class T:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        t = T(1, 2)
        assert t == t
        assert t == T(1, 2)
        assert t != T(10, 20)
        assert hash(t) == hash(T(1, 2))
        assert hash(t) != hash(T(10, 20))
        assert t != None

        @hasheq()
        @constructor()
        @asitems(['x', 'y'])
        class T1:
            pass

        t = T1(1, 2)
        assert t == t
        assert t == T1(1, 2)
        assert t != T1(10, 20)
        assert hash(t) == hash(T1(1, 2))
        assert hash(t) != hash(T1(10, 20))
        assert t != None

    def test_accessor(self):
        @accessor()
        @asitems(['x', 'y'])
        class T1:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        t = T1(2, 100)
        assert t.x == 2
        assert t.y == 100
        t.x, t.y = 3, 7
        assert t.x == 3
        assert t.y == 7

        @accessor(readonly=True)
        @asitems(['x', 'y'])
        class T2:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        t = T2(2, 100)
        assert t.x == 2
        assert t.y == 100
        with pytest.raises(AttributeError):
            t.x = 3
        with pytest.raises(AttributeError):
            t.y = 7

        @accessor([('x', 'ro'), ('y', 'rw')])
        class T3:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        t = T3(2, 100)
        assert t.x == 2
        assert t.y == 100
        with pytest.raises(AttributeError):
            t.x = 3
        t.y = 7
        assert t.x == 2
        assert t.y == 7

        @accessor('y')
        @accessor('x', readonly=True)
        class T4:
            def __init__(self, x, y):
                self.__x = x
                self.__y = y

        t = T4(2, 100)
        assert t.x == 2
        assert t.y == 100
        with pytest.raises(AttributeError):
            t.x = 3
        t.y = 7
        assert t.x == 2
        assert t.y == 7

        with pytest.raises(ValueError):
            @accessor([('x', 'rrr'), ('y', 'rw')])
            class T5:
                def __init__(self, x, y):
                    self.__x = x
                    self.__y = y

    def test_get_field(self):
        class T:
            def __init__(self):
                self.a = 1
                self._b = 2
                self.__c = 3
                self.___d = 4

        assert get_field(T(), 'a') == 1
        assert get_field(T(), '_b') == 2
        assert get_field(T(), 'b', 233) == 233
        assert get_field(T(), '__c') == 3
        assert get_field(T(), '___d') == 4

        # noinspection PyPep8Naming
        class _T_:
            def __init__(self):
                self.a = 1
                self._b = 2
                self.__c = 3
                self.___d = 4

        assert get_field(_T_(), 'a') == 1
        assert get_field(_T_(), '_b') == 2
        assert get_field(_T_(), 'b', 233) == 233
        assert get_field(_T_(), '__c') == 3
        assert get_field(_T_(), '___d') == 4
