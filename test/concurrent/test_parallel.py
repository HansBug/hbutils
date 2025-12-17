import time

import pytest

from hbutils.concurrent import parallel_call
from hbutils.testing import Impl, OS


@pytest.mark.unittest
class TestConcurrentParallel:
    def test_parallel_call(self):
        values = []

        def _fn(idx):
            time.sleep(0.3)
            values.append(idx)

        start_time = time.time()
        parallel_call(
            iterable=range(10),
            fn=_fn,
            max_workers=3,
            desc='test_parallel_call',
        )

        duration = time.time() - start_time
        if OS.linux and Impl.pypy:
            assert duration == pytest.approx(1.2, abs=5e-2)
        assert sorted(values) == list(range(10))

    def test_parallel_call_all_pending(self):
        values = []

        def _fn(idx):
            time.sleep(0.3)
            values.append(idx)

        start_time = time.time()
        parallel_call(
            iterable=range(10),
            fn=_fn,
            max_workers=3,
            max_pending=-1,
            desc='test_parallel_call_all_pending',
        )

        duration = time.time() - start_time
        if OS.linux and Impl.pypy:
            assert duration == pytest.approx(1.2, abs=5e-2)
        assert sorted(values) == list(range(10))

    def test_parallel_call_low_pending(self):
        values = []

        def _fn(idx):
            time.sleep(0.3)
            values.append(idx)

        start_time = time.time()
        parallel_call(
            iterable=range(10),
            fn=_fn,
            max_workers=3,
            max_pending=5,
            desc='test_parallel_call_low_pending',
        )

        duration = time.time() - start_time
        if OS.linux and Impl.pypy:
            assert duration == pytest.approx(1.2, abs=5e-2)
        assert sorted(values) == list(range(10))

    def test_parallel_call_exception(self):

        def _fn(idx):
            time.sleep(0.3)
            raise RuntimeError(f'Error - {idx!r}')

        start_time = time.time()
        parallel_call(
            iterable=range(10),
            fn=_fn,
            max_workers=3,
            max_pending=5,
            desc='test_parallel_call_exception',
        )

        duration = time.time() - start_time
        if OS.linux and Impl.pypy:
            assert duration == pytest.approx(1.2, abs=5e-2)
