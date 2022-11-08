import pytest

from hbutils.collection import get_recovery_func


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestCollectionRecover:
    def test_dict_simple(self):
        d = {'a': 1, 'b': 2, 'c': 'abcde'}
        func = get_recovery_func(d)
        assert callable(func)
        assert d is d
        assert d == {'a': 1, 'b': 2, 'c': 'abcde'}

        d['a'] = '923'
        del d['b']
        d['d'] = 10000
        assert d == {'a': '923', 'c': 'abcde', 'd': 10000}

        dx = func()
        assert dx is d
        assert d == {'a': 1, 'b': 2, 'c': 'abcde'}

    def test_dict_recursive(self):
        d = {'a': 1, 'b': {'x': 1, 'y': 2}, 'c': 'abcde', 'd': [3, 5, (8, 6)]}
        func = get_recovery_func(d)
        assert callable(func)
        assert d is d
        assert d == {'a': 1, 'b': {'x': 1, 'y': 2}, 'c': 'abcde', 'd': [3, 5, (8, 6)]}

        d['a'] = '923'
        del d['c']
        d['b']['z'] = 3
        d['b']['x'] = 2
        del d['b']['y']
        d['d'][0] = -1
        d['d'].append('777')
        d['e'] = 10000
        assert d == {'a': '923', 'b': {'x': 2, 'z': 3}, 'd': [-1, 5, (8, 6), '777'], 'e': 10000}

        dx = func()
        assert dx is d
        assert dx['b'] is d['b']
        assert dx['d'] is d['d']
        assert d == {'a': 1, 'b': {'x': 1, 'y': 2}, 'c': 'abcde', 'd': [3, 5, (8, 6)]}

    def test_dict_swallow(self):
        d = {'a': 1, 'b': {'x': 1, 'y': 2}, 'c': 'abcde', 'd': [3, 5, (8, 6)]}
        func = get_recovery_func(d, recursive=False)
        assert callable(func)
        assert d is d
        assert d == {'a': 1, 'b': {'x': 1, 'y': 2}, 'c': 'abcde', 'd': [3, 5, (8, 6)]}

        d['a'] = '923'
        del d['c']
        d['b']['z'] = 3
        d['b']['x'] = 2
        del d['b']['y']
        d['d'][0] = -1
        d['d'].append('777')
        d['e'] = 10000
        assert d == {'a': '923', 'b': {'x': 2, 'z': 3}, 'd': [-1, 5, (8, 6), '777'], 'e': 10000}

        dx = func()
        assert dx is d
        assert dx['b'] is d['b']
        assert dx['d'] is d['d']
        assert d == {'a': 1, 'b': {'x': 2, 'z': 3}, 'c': 'abcde', 'd': [-1, 5, (8, 6), '777']}

    def test_list_simple(self):
        lst = [1, 2, 3, 4, '5']
        func = get_recovery_func(lst)
        assert callable(func)
        assert lst is lst
        assert lst == [1, 2, 3, 4, '5']

        lst[0] = -1
        lst[-2:] = [7]
        lst.append(8)
        lst.append(9)
        lst.append(100)
        assert lst == [-1, 2, 3, 7, 8, 9, 100]

        lx = func()
        assert lx is lst
        assert lst == [1, 2, 3, 4, '5']

    def test_list_recursive(self):
        lst = [1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2]]
        func = get_recovery_func(lst)
        assert callable(func)
        assert lst is lst
        assert lst == [1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2]]

        lst[0] = -1
        lst[1].append(-9)
        lst[1][-2]['c'] = 2
        lst[2]['x'] = 2
        del lst[2]['y']
        lst[2]['z'] = 300
        lst[-1].append(3)
        lst[-2:] = [7]
        lst.append(8)
        lst.append(9)
        lst.append(100)
        assert lst == [-1, [5, (6, 7), {'a': 8, 'c': 2}, -9], {'x': 2, 'z': 300}, 7, 8, 9, 100]

        lx = func()
        assert lx is lst
        assert lst == [1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2]]

    def test_list_swallow(self):
        lst = [1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2]]
        func = get_recovery_func(lst, recursive=False)
        assert callable(func)
        assert lst is lst
        assert lst == [1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2]]

        lst[0] = -1
        lst[1].append(-9)
        lst[1][-2]['c'] = 2
        lst[2]['x'] = 2
        del lst[2]['y']
        lst[2]['z'] = 300
        lst[-1].append(3)
        lst[-2:] = [7]
        lst.append(8)
        lst.append(9)
        lst.append(100)
        assert lst == [-1, [5, (6, 7), {'a': 8, 'c': 2}, -9], {'x': 2, 'z': 300}, 7, 8, 9, 100]

        lx = func()
        assert lx is lst
        assert lst == [1, [5, (6, 7), {'a': 8, 'c': 2}, -9], {'x': 2, 'z': 300}, 4, [1, 2, 3]]

    def test_tuple_simple(self):
        t = (1, 2, 3, 'a')
        func = get_recovery_func(t)
        assert callable(func)
        assert t is t
        assert t == (1, 2, 3, 'a')

        tx = func()
        assert tx is t
        assert t == (1, 2, 3, 'a')

    def test_tuple_recursive(self):
        t = (1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2])
        func = get_recovery_func(t)
        assert callable(func)
        assert t is t
        assert t == (1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2])

        t[1].append(-9)
        t[1][-2]['c'] = 2
        t[2]['x'] = 2
        del t[2]['y']
        t[2]['z'] = 300
        t[-1].append(3)
        assert t == (1, [5, (6, 7), {'a': 8, 'c': 2}, -9], {'x': 2, 'z': 300}, 4, [1, 2, 3])

        tx = func()
        assert tx is t
        assert tx[1] is t[1]
        assert tx[2] is t[2]
        assert tx[4] is t[4]
        assert t == (1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2])

    def test_tuple_swallow(self):
        t = (1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2])
        func = get_recovery_func(t, recursive=False)
        assert callable(func)
        assert t is t
        assert t == (1, [5, (6, 7), {'a': 8}], {'x': 1, 'y': 22}, 4, [1, 2])

        t[1].append(-9)
        t[1][-2]['c'] = 2
        t[2]['x'] = 2
        del t[2]['y']
        t[2]['z'] = 300
        t[-1].append(3)
        assert t == (1, [5, (6, 7), {'a': 8, 'c': 2}, -9], {'x': 2, 'z': 300}, 4, [1, 2, 3])

        tx = func()
        assert tx is t
        assert tx[1] is t[1]
        assert tx[2] is t[2]
        assert tx[4] is t[4]
        assert t == (1, [5, (6, 7), {'a': 8, 'c': 2}, -9], {'x': 2, 'z': 300}, 4, [1, 2, 3])

    def test_raw(self):
        v = 1
        func = get_recovery_func(v)
        assert callable(func)
        assert v is v
        assert v == 1

        vx = func()
        assert vx is v
        assert vx == 1

    def test_generic_class(self):
        class MyClassA:
            def __init__(self, x, y, z):
                self.x = x
                self._y = y
                self.__z = z

            def result(self):
                return (self.x + self._y * 2) * self.__z

        v1 = MyClassA(2, 4, 5)
        f1 = get_recovery_func(v1)
        assert v1.result() == 50

        v1.x = 100
        assert v1.result() == 540

        v1._y = 20
        assert v1.result() == 700

        v1._MyClassA__z = 8
        assert v1.result() == 1120

        assert f1() is v1
        assert v1.result() == 50
