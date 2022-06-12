import pytest

from hbutils.algorithm import linear_map


@pytest.mark.unittest
class TestAlgorithmLinear:
    def test_linear_map_simple(self):
        f = linear_map((0, 1, 0.5))
        assert f(0) == pytest.approx(0.0)
        assert f(0.25) == pytest.approx(0.5)
        assert f(1 / 3) == pytest.approx(2 / 3)
        assert f(0.5) == pytest.approx(1.0)
        assert f(2 / 3) == pytest.approx(5 / 6)
        assert f(0.75) == pytest.approx(0.75)
        assert f(1) == pytest.approx(0.5)

        with pytest.raises(ValueError):
            f(-1)
        with pytest.raises(ValueError):
            f(-0.001)
        with pytest.raises(ValueError):
            f(1.001)
        with pytest.raises(ValueError):
            f(2)

    def test_linear_map_complex(self):
        f = linear_map((
            (-0.2, 0),
            (0.7, 1),
            (1.1, 0.5),
        ))
        assert f(-0.2) == pytest.approx(0.0)
        assert f(0) == pytest.approx(2 / 9)
        assert f(0.25) == pytest.approx(0.5)
        assert f(1 / 3) == pytest.approx(16 / 27)
        assert f(0.5) == pytest.approx(7 / 9)
        assert f(2 / 3) == pytest.approx(26 / 27)
        assert f(0.7) == pytest.approx(1.0)
        assert f(0.75) == pytest.approx(0.9375)
        assert f(0.8) == pytest.approx(0.875)
        assert f(1) == pytest.approx(0.625)
        assert f(1.1) == pytest.approx(0.5)

        with pytest.raises(ValueError):
            f(-1)
        with pytest.raises(ValueError):
            f(-0.201)
        with pytest.raises(ValueError):
            f(1.101)
        with pytest.raises(ValueError):
            f(2)

    def test_linear_map_invalid(self):
        with pytest.raises(AssertionError):
            linear_map((
                (1.2, 0),
                (-0.2, 1),
                (1.1, 0.5),
            ))
        with pytest.raises(AssertionError):
            linear_map(())
