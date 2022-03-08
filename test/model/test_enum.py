from enum import IntEnum, Enum

import pytest

from hbutils.model import int_enum_loads, AutoIntEnum


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestReflectionEnum:
    def test_int_enum_loads_base(self):
        @int_enum_loads()
        class Enum1(IntEnum):
            A = 1
            B = 2
            C = 3

        assert Enum1.loads(Enum1.A) is Enum1.A
        assert Enum1.loads(Enum1.B) is Enum1.B
        assert Enum1.loads(Enum1.C) is Enum1.C
        assert Enum1.loads(1) is Enum1.A
        assert Enum1.loads(2) is Enum1.B
        assert Enum1.loads(3) is Enum1.C
        assert Enum1.loads('A') is Enum1.A
        assert Enum1.loads('B') is Enum1.B
        assert Enum1.loads('C') is Enum1.C
        with pytest.raises(TypeError):
            Enum1.loads(None)

    def test_int_enum_loads_error(self):
        with pytest.raises(TypeError):
            @int_enum_loads()
            class Enum1(Enum):
                A = 1
                B = 2
                C = 3

    def test_int_enum_disable_int(self):
        @int_enum_loads(enable_int=False)
        class Enum1(IntEnum):
            A = 1
            B = 2
            C = 3

        assert Enum1.loads(Enum1.A) is Enum1.A
        assert Enum1.loads(Enum1.B) is Enum1.B
        assert Enum1.loads(Enum1.C) is Enum1.C
        with pytest.raises(TypeError):
            assert Enum1.loads(1) is Enum1.A
        with pytest.raises(TypeError):
            assert Enum1.loads(2) is Enum1.B
        with pytest.raises(TypeError):
            assert Enum1.loads(3) is Enum1.C
        assert Enum1.loads('A') is Enum1.A
        assert Enum1.loads('B') is Enum1.B
        assert Enum1.loads('C') is Enum1.C
        with pytest.raises(TypeError):
            Enum1.loads(None)

    def test_int_enum_disable_str(self):
        @int_enum_loads(enable_str=False)
        class Enum1(IntEnum):
            A = 1
            B = 2
            C = 3

        assert Enum1.loads(Enum1.A) is Enum1.A
        assert Enum1.loads(Enum1.B) is Enum1.B
        assert Enum1.loads(Enum1.C) is Enum1.C
        assert Enum1.loads(1) is Enum1.A
        assert Enum1.loads(2) is Enum1.B
        assert Enum1.loads(3) is Enum1.C
        with pytest.raises(TypeError):
            assert Enum1.loads('A') is Enum1.A
        with pytest.raises(TypeError):
            assert Enum1.loads('B') is Enum1.B
        with pytest.raises(TypeError):
            assert Enum1.loads('C') is Enum1.C
        with pytest.raises(TypeError):
            Enum1.loads(None)

    def test_int_enum_extend_int(self):
        @int_enum_loads(value_preprocess=lambda x: abs(x))
        class Enum1(IntEnum):
            A = 1
            B = 2
            C = 3

        assert Enum1.loads(Enum1.A) is Enum1.A
        assert Enum1.loads(Enum1.B) is Enum1.B
        assert Enum1.loads(Enum1.C) is Enum1.C
        assert Enum1.loads(1) is Enum1.A
        assert Enum1.loads(2) is Enum1.B
        assert Enum1.loads(3) is Enum1.C
        assert Enum1.loads(-1) is Enum1.A
        assert Enum1.loads(-2) is Enum1.B
        assert Enum1.loads(-3) is Enum1.C
        assert Enum1.loads('A') is Enum1.A
        assert Enum1.loads('B') is Enum1.B
        assert Enum1.loads('C') is Enum1.C
        with pytest.raises(TypeError):
            Enum1.loads(None)

    def test_int_enum_extend_str(self):
        @int_enum_loads(name_preprocess=lambda x: x.lower())
        class Enum1(IntEnum):
            A = 1
            B = 2
            C = 3

        assert Enum1.loads(Enum1.A) is Enum1.A
        assert Enum1.loads(Enum1.B) is Enum1.B
        assert Enum1.loads(Enum1.C) is Enum1.C
        assert Enum1.loads(1) is Enum1.A
        assert Enum1.loads(2) is Enum1.B
        assert Enum1.loads(3) is Enum1.C
        assert Enum1.loads('A') is Enum1.A
        assert Enum1.loads('B') is Enum1.B
        assert Enum1.loads('C') is Enum1.C
        assert Enum1.loads('a') is Enum1.A
        assert Enum1.loads('b') is Enum1.B
        assert Enum1.loads('c') is Enum1.C
        with pytest.raises(TypeError):
            Enum1.loads(None)

    def test_int_enum_extend_else(self):
        @int_enum_loads(external_process=lambda x: None)
        class Enum1(IntEnum):
            A = 1
            B = 2
            C = 3

        assert Enum1.loads(Enum1.A) is Enum1.A
        assert Enum1.loads(Enum1.B) is Enum1.B
        assert Enum1.loads(Enum1.C) is Enum1.C
        assert Enum1.loads(1) is Enum1.A
        assert Enum1.loads(2) is Enum1.B
        assert Enum1.loads(3) is Enum1.C
        assert Enum1.loads('A') is Enum1.A
        assert Enum1.loads('B') is Enum1.B
        assert Enum1.loads('C') is Enum1.C
        assert Enum1.loads(None) is None
        assert Enum1.loads([1, 2]) is None

    def test_auto_int_enum(self):
        class MyEnum(AutoIntEnum):
            def __init__(self, v):
                self.v = v

            A = 'a_v'
            B = 'b_vv'
            C = 'c_vvv'

        assert MyEnum.A.value == 1
        assert MyEnum.A.v == 'a_v'
        assert MyEnum.B.value == 2
        assert MyEnum.B.v == 'b_vv'
        assert MyEnum.C.value == 3
        assert MyEnum.C.v == 'c_vvv'

    def test_auto_int_enum_with_int_enum_loads(self):
        @int_enum_loads(name_preprocess=str.upper)
        class MyEnum(AutoIntEnum):
            def __init__(self, v):
                self.v = v

            A = 'a_v'
            B = 'b_vv'
            C = 'c_vvv'

        assert MyEnum.loads('a') == MyEnum.A
        assert MyEnum.loads(1) == MyEnum.A
        assert MyEnum.loads('B') == MyEnum.B
        assert MyEnum.loads(2) == MyEnum.B
        assert MyEnum.loads('c') == MyEnum.C
        assert MyEnum.loads(3) == MyEnum.C
