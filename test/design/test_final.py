import pytest

from hbutils.design import FinalMeta


@pytest.mark.unittest
class TestDesignFinal:
    def test_final_meta(self):
        class _FinalClass(metaclass=FinalMeta):
            pass

        assert isinstance(_FinalClass(), _FinalClass)

        with pytest.raises(TypeError):
            class _InvalidClass(_FinalClass):
                pass
