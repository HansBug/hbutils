import os.path
import pathlib
import tempfile
import unittest
from contextlib import contextmanager
from multiprocessing import Process, Manager
from threading import Thread

import pytest

from hbutils.reflection import context, cwrap
from hbutils.reflection.context import ContextVars, nested_with
from hbutils.testing import OS, vpython


@contextmanager
def opent(x):
    with tempfile.TemporaryDirectory() as td:
        pathlib.Path(os.path.join(td, f'{x}.txt')).write_text(f'this is {x}!')
        yield td


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestReflectionContext:
    def test_context_simple(self):
        def var_detect():
            if context().get('var', None):
                return True
            else:
                return False

        assert not var_detect()
        with context().vars(var=1):
            assert var_detect()
        assert not var_detect()

    def test_context_plus(self):
        def get_plus():
            return context().get('a', 0) + context().get('b', 0)

        assert get_plus() == 0
        assert len(context()) == 0
        assert set(context().keys()) == set()

        with context().vars(a=1):
            assert get_plus() == 1
            assert len(context()) == 1
            assert set(context().keys()) == {'a'}

            with context().vars(b=2):
                assert get_plus() == 3
                assert len(context()) == 2
                assert set(context().keys()) == {'a', 'b'}

            assert get_plus() == 1
            assert len(context()) == 1
            assert set(context().keys()) == {'a'}

            with context().vars(a=3, b=2):
                assert get_plus() == 5
                assert len(context()) == 2
                assert set(context().keys()) == {'a', 'b'}

            assert get_plus() == 1
            assert len(context()) == 1
            assert set(context().keys()) == {'a'}

        assert get_plus() == 0
        assert len(context()) == 0
        assert set(context().keys()) == set()

    def test_context_threading(self):
        lst = []

        def get_plus():
            return context().get('a', 0) + context().get('b', 0)

        def run_result():
            lst.append(get_plus())
            with context().vars(a=2):
                lst.append(get_plus())
                with context().vars(b=3):
                    lst.append(get_plus())
                lst.append(get_plus())

                with context().vars(a=4, b=5):
                    lst.append(get_plus())
                lst.append(get_plus())
            lst.append(get_plus())

        with context().vars(a=1, b=2):  # no inherit
            lst.clear()
            t1 = Thread(target=run_result)
            t1.start()
            t1.join()

            assert lst == [0, 2, 5, 2, 9, 2, 0]

        with context().vars(a=1, b=2):  # inherit
            lst.clear()
            t1 = Thread(target=cwrap(run_result))
            t1.start()
            t1.join()

            assert lst == [3, 4, 5, 4, 9, 4, 3]

        with context().vars(a=1, b=2):  # inherit with extras
            lst.clear()
            t1 = Thread(target=cwrap(run_result, a=2))
            t1.start()
            t1.join()

            assert lst == [4, 4, 5, 4, 9, 4, 4]

    @unittest.skipIf(OS.windows or (OS.macos and vpython >= '3.8'), 'Process supported.')
    def test_context_process(self):
        manager = Manager()
        lst = manager.list([])

        def get_plus():
            return context().get('a', 0) + context().get('b', 0)

        def run_result():
            lst.append(get_plus())
            with context().vars(a=2):
                lst.append(get_plus())
                with context().vars(b=3):
                    lst.append(get_plus())
                lst.append(get_plus())

                with context().vars(a=4, b=5):
                    lst.append(get_plus())
                lst.append(get_plus())
            lst.append(get_plus())

        with context().vars(a=1, b=2):  # no inherit
            lst[:] = []
            t1 = Process(target=run_result)
            t1.start()
            t1.join()

            assert list(lst) == [0, 2, 5, 2, 9, 2, 0]

        with context().vars(a=1, b=2):  # inherit
            lst[:] = []
            t1 = Process(target=cwrap(run_result))
            t1.start()
            t1.join()

            assert list(lst) == [3, 4, 5, 4, 9, 4, 3]

        with context().vars(a=1, b=2):  # inherit with extras
            lst[:] = []
            t1 = Process(target=cwrap(run_result, a=2))
            t1.start()
            t1.join()

            assert list(lst) == [4, 4, 5, 4, 9, 4, 4]

    def test_context_inherit(self):
        cv = ContextVars(a=1, c=2)

        def get_sum():
            return context().get('a', 0) + context().get('b', 0) + context().get('c', 0)

        assert get_sum() == 0
        with context().vars(a=3, b=4):
            assert get_sum() == 7
            with context().inherit(cv):
                assert get_sum() == 3
            assert get_sum() == 7

        assert get_sum() == 0

    def test_actual_usage(self):
        @contextmanager
        def use_mul():
            with context().vars(mul=True):
                yield

        def calc(a, b):
            if context().get('mul', None):
                return a * b
            else:
                return a + b

        assert calc(3, 5) == 8
        with use_mul():
            assert calc(3, 5) == 15

        assert calc(3, 5) == 8

    def test_nested_with(self):
        with opent(1) as d:
            assert os.path.exists(d)
            assert os.listdir(d)
            assert os.path.exists(os.path.join(d, '1.txt'))
            assert pathlib.Path(os.path.join(d, '1.txt')).read_text().strip() == 'this is 1!'

        with nested_with(*map(opent, range(30))) as ds:
            for i, d in enumerate(ds):
                assert os.path.exists(d)
                assert os.listdir(d)
                assert os.path.exists(os.path.join(d, f'{i}.txt'))
                assert pathlib.Path(os.path.join(d, f'{i}.txt')).read_text().strip() == f'this is {i}!'

        for d in ds:
            assert not os.path.exists(d)
