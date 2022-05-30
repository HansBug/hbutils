from enum import IntEnum, unique

import pytest

from hbutils.design import Observable


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestDesignObserver:
    def test_base(self):
        o = Observable(['a', 'b'])

        a_visited = 0

        def _hansbug_watch_a():
            nonlocal a_visited
            a_visited += 1

        def _stranger_watch_a():
            nonlocal a_visited
            a_visited += 10

        b_visited = 0

        def _hansbug_watch_b():
            nonlocal b_visited
            b_visited += 1

        o.subscribe('a', 'hansbug', _hansbug_watch_a)
        o.subscribe('b', 'hansbug', _hansbug_watch_b)
        o.subscribe('a', 'stranger', _stranger_watch_a)

        assert (a_visited, b_visited) == (0, 0)
        o.dispatch('a')
        assert (a_visited, b_visited) == (11, 0)
        o.dispatch('b')
        assert (a_visited, b_visited) == (11, 1)

        o.unsubscribe('a', 'hansbug')
        o.dispatch('a')
        assert (a_visited, b_visited) == (21, 1)
        o.dispatch('b')
        assert (a_visited, b_visited) == (21, 2)

        o.unsubscribe('a', 'stranger')
        o.dispatch('a')
        assert (a_visited, b_visited) == (21, 2)
        o.dispatch('b')
        assert (a_visited, b_visited) == (21, 3)

        o.unsubscribe('b', 'hansbug')
        o.dispatch('a')
        assert (a_visited, b_visited) == (21, 3)
        o.dispatch('b')
        assert (a_visited, b_visited) == (21, 3)

    def test_with_enum(self):
        @unique
        class MyIntEnum(IntEnum):
            A = 1
            B = 2

        o = Observable(MyIntEnum)

        a_visited = 0

        def _hansbug_watch_a():
            nonlocal a_visited
            a_visited += 1

        def _stranger_watch_a():
            nonlocal a_visited
            a_visited += 10

        b_visited = 0

        def _hansbug_watch_b():
            nonlocal b_visited
            b_visited += 1

        o.subscribe(MyIntEnum.A, 'hansbug', _hansbug_watch_a)
        o.subscribe(MyIntEnum.B, 'hansbug', _hansbug_watch_b)
        o.subscribe(MyIntEnum.A, 'stranger', _stranger_watch_a)

        assert (a_visited, b_visited) == (0, 0)
        o.dispatch(MyIntEnum.A)
        assert (a_visited, b_visited) == (11, 0)
        o.dispatch(MyIntEnum.B)
        assert (a_visited, b_visited) == (11, 1)

        o.unsubscribe(MyIntEnum.A, 'hansbug')
        o.dispatch(MyIntEnum.A)
        assert (a_visited, b_visited) == (21, 1)
        o.dispatch(MyIntEnum.B)
        assert (a_visited, b_visited) == (21, 2)

        o.unsubscribe(MyIntEnum.A, 'stranger')
        o.dispatch(MyIntEnum.A)
        assert (a_visited, b_visited) == (21, 2)
        o.dispatch(MyIntEnum.B)
        assert (a_visited, b_visited) == (21, 3)

        o.unsubscribe(MyIntEnum.B, 'hansbug')
        o.dispatch(MyIntEnum.A)
        assert (a_visited, b_visited) == (21, 3)
        o.dispatch(MyIntEnum.B)
        assert (a_visited, b_visited) == (21, 3)

    # noinspection PyTypeChecker
    def test_invalid_type(self):
        class MyClazz:
            A = 1
            B = 2

        with pytest.raises(TypeError):
            Observable(MyClazz)
        with pytest.raises(TypeError):
            Observable(1)
        with pytest.raises(TypeError):
            Observable('skldfj')

    def test_unhashable(self):
        # noinspection DuplicatedCode
        @unique
        class MyIntEnum(IntEnum):
            A = 1
            B = 2

        o = Observable(MyIntEnum)

        la, lb = [], []

        o.subscribe(MyIntEnum.A, la, 'append')
        o.subscribe(MyIntEnum.B, la, 'append')
        o.subscribe(MyIntEnum.A, lb, 'append')

        assert (la, lb) == ([], [])
        o.dispatch(MyIntEnum.A)
        assert (la, lb) == ([MyIntEnum.A], [MyIntEnum.A])
        o.dispatch(MyIntEnum.B)
        assert (la, lb) == ([MyIntEnum.A, MyIntEnum.B], [MyIntEnum.A])

        o.unsubscribe(MyIntEnum.A, la)
        o.dispatch(MyIntEnum.A)
        assert (la, lb) == ([MyIntEnum.A, MyIntEnum.B], [MyIntEnum.A, MyIntEnum.A])
        o.dispatch(MyIntEnum.B)
        assert (la, lb) == ([MyIntEnum.A, MyIntEnum.B, MyIntEnum.B], [MyIntEnum.A, MyIntEnum.A])

    def test_use_update(self):
        # noinspection DuplicatedCode
        @unique
        class MyIntEnum(IntEnum):
            A = 1
            B = 2

        o = Observable(MyIntEnum)

        class MyClass:
            def __init__(self):
                self.lst = []

            def update(self, x):
                self.lst.append(x)

        la, lb = MyClass(), MyClass()

        o.subscribe(MyIntEnum.A, la)
        o.subscribe(MyIntEnum.B, la)
        o.subscribe(MyIntEnum.A, lb)

        assert (la.lst, lb.lst) == ([], [])
        o.dispatch(MyIntEnum.A)
        assert (la.lst, lb.lst) == ([MyIntEnum.A], [MyIntEnum.A])
        o.dispatch(MyIntEnum.B)
        assert (la.lst, lb.lst) == ([MyIntEnum.A, MyIntEnum.B], [MyIntEnum.A])

        o.unsubscribe(MyIntEnum.A, la)
        o.dispatch(MyIntEnum.A)
        assert (la.lst, lb.lst) == ([MyIntEnum.A, MyIntEnum.B], [MyIntEnum.A, MyIntEnum.A])
        o.dispatch(MyIntEnum.B)
        assert (la.lst, lb.lst) == ([MyIntEnum.A, MyIntEnum.B, MyIntEnum.B], [MyIntEnum.A, MyIntEnum.A])

    # noinspection PyTypeChecker
    def test_invalid_subscribe(self):
        @unique
        class MyIntEnum(IntEnum):
            A = 1
            B = 2

        o = Observable(MyIntEnum)

        la, lb = [], []

        with pytest.raises(TypeError):
            o.subscribe(MyIntEnum.A, la, 1)
        with pytest.raises(TypeError):
            o.subscribe(MyIntEnum.B, la, '__doc__')

    def test_invalid_unsubscribe(self):
        # noinspection DuplicatedCode
        @unique
        class MyIntEnum(IntEnum):
            A = 1
            B = 2

        o = Observable(MyIntEnum)

        la, lb = [], []
        o.subscribe(MyIntEnum.A, la, 'append')
        o.subscribe(MyIntEnum.B, la, 'append')
        o.subscribe(MyIntEnum.A, lb, 'append')

        o.unsubscribe(MyIntEnum.A, la)
        with pytest.raises(KeyError) as ei:
            o.unsubscribe(MyIntEnum.A, la)
        err = ei.value
        assert err.args == (la,)
