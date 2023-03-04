import random
from unittest import skipUnless

import pytest

from hbutils.random import keep_global_state, global_seed, register_random_source, register_random_instance, \
    get_global_state, set_global_state, seedable_func
from hbutils.testing import vpip


@pytest.mark.unittest
class TestRandomState:
    @pytest.mark.parametrize(['seed'], [(i,) for i in range(10, 101, 10)])
    def test_keep_global_state(self, seed):
        with pytest.warns(None):
            random.seed(seed)
            before_data = [random.randint(0, 100) for _ in range(50)]
            after_data = [random.randint(0, 100) for _ in range(50)]

            random.seed(seed)
            before_data_2 = [random.randint(0, 100) for _ in range(50)]
            with keep_global_state():
                _ = [random.randint(0, 100) for _ in range(50)]

            after_data_2 = [random.randint(0, 100) for _ in range(50)]

            assert before_data == before_data_2
            assert after_data == after_data_2

    @skipUnless(vpip('numpy'), 'numpy required.')
    @pytest.mark.parametrize(['seed'], [(i,) for i in range(10, 101, 10)])
    def test_random_with_numpy(self, seed):
        import numpy as np

        with pytest.warns(None):
            global_seed(seed)
            before_data = np.random.randint(0, 100, (20, 30))
            after_data = np.random.randint(0, 100, (20, 30))

            global_seed(seed)
            before_data_2 = np.random.randint(0, 100, (20, 30))
            with keep_global_state():
                _ = np.random.randint(0, 100, (20, 30))
            after_data_2 = np.random.randint(0, 100, (20, 30))

            assert np.isclose(before_data, before_data_2).all()
            assert np.isclose(after_data, after_data_2).all()

    @skipUnless(vpip('torch'), 'torch required')
    @pytest.mark.parametrize(['seed'], [(i,) for i in range(10, 101, 10)])
    def test_random_with_torch(self, seed):
        import torch

        with pytest.warns(None):
            global_seed(seed)
            before_data = torch.randint(0, 100, (20, 30))
            after_data = torch.randint(0, 100, (20, 30))

            global_seed(seed)
            before_data_2 = torch.randint(0, 100, (20, 30))
            with keep_global_state():
                _ = torch.randint(0, 100, (20, 30))
            after_data_2 = torch.randint(0, 100, (20, 30))

            assert torch.isclose(before_data, before_data_2).all()
            assert torch.isclose(after_data, after_data_2).all()

    @skipUnless(vpip('faker'), 'faker required')
    @pytest.mark.parametrize(['seed'], [(i,) for i in range(10, 101, 10)])
    def test_random_with_faker(self, seed):
        from faker import Faker

        _FAKER = Faker()

        with pytest.warns(None):
            global_seed(seed)
            before_data = _FAKER.paragraph(10)
            after_data = _FAKER.paragraph(10)

            global_seed(seed)
            before_data_2 = _FAKER.paragraph(10)
            with keep_global_state():
                _ = _FAKER.paragraph(100)
            after_data_2 = _FAKER.paragraph(10)

            assert before_data == before_data_2
            assert after_data == after_data_2

    def test_register_error(self):
        rnd = random.Random()
        with pytest.raises(NameError):
            register_random_source('native_random', rnd.seed, rnd.getstate, rnd.setstate)
        with pytest.raises(NameError):
            register_random_instance('native_random', rnd)

    def test_set_state_warnings(self):
        states = get_global_state()
        assert isinstance(states, dict)
        with pytest.warns(None):
            set_global_state(states)

        states = get_global_state()
        states['not_found_source'] = 233.0
        with pytest.warns(Warning):
            set_global_state(states)

        states = get_global_state()
        del states['native_random']
        with pytest.warns(Warning):
            set_global_state(states)

    @pytest.mark.parametrize(['seed'], [(i,) for i in range(10, 101, 10)])
    def test_seedable_func(self, seed):
        @seedable_func
        def my_func(x, y):
            return x + 1 + 2 * y + random.random() * 3

        d = [my_func(1, 2) for _ in range(100)]
        assert not [d[0]] * 100 == pytest.approx(d)

        dx = [my_func(1, 2, seed=seed) for _ in range(100)]
        for i in range(1, len(dx)):
            assert dx[i] == pytest.approx(dx[0])

    @skipUnless(vpip('torch'), 'torch required')
    @pytest.mark.parametrize(['seed'], [(i,) for i in range(10, 101, 10)])
    def test_seedable_func_with_torch(self, seed):
        import torch

        @seedable_func
        def my_func(x, y):
            return x + 1 + 2 * y + torch.randn((20, 30))

        d1 = my_func(1, 2)
        d2 = my_func(1, 2)
        assert not torch.isclose(d1, d2).all()

        d3 = my_func(1, 2, seed=seed)
        d4 = my_func(1, 2, seed=seed)
        assert torch.isclose(d3, d4).all()
