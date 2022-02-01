import pytest

from hbutils.model import get_repr_info


@pytest.mark.unittest
class TestModelRepr:
    def test_get_repr_info(self):
        class Sum:
            def __init__(self, a, b):
                self.__a = a
                self.__b = b

            def __repr__(self):
                return get_repr_info(
                    cls=self.__class__,
                    args=[
                        ('b', (lambda: self.__b, lambda: self.__b is not None)),
                        ('a', lambda: self.__a),
                    ]
                )

        assert repr(Sum(1, 2)) == '<Sum b: 2, a: 1>'
        assert repr(Sum(None, None)) == '<Sum a: None>'

        class Sumx:
            def __init__(self, a, b):
                self.__a = a
                self.__b = b

            def __repr__(self):
                return get_repr_info(
                    cls=self.__class__,
                    args=[
                        ('b', lambda: self.__b, lambda: self.__b is not None),
                        ('a', lambda: self.__a),
                    ]
                )

        assert repr(Sumx(1, 2)) == '<Sumx b: 2, a: 1>'
        assert repr(Sumx(None, None)) == '<Sumx a: None>'

        class Emp:
            def __repr__(self):
                return get_repr_info(
                    cls=self.__class__,
                    args=[]
                )

        assert repr(Emp()) == '<Emp>'

    def test_get_repr_info_invalid(self):
        class Sum:
            def __init__(self, a, b):
                self.__a = a
                self.__b = b

            def __repr__(self):
                return get_repr_info(
                    cls=self.__class__,
                    args=[
                        ('b',),
                        ('a', lambda: self.__a),
                    ]
                )

        with pytest.raises(ValueError):
            repr(Sum(1, 2))

        class Sumx:
            def __init__(self, a, b):
                self.__a = a
                self.__b = b

            def __repr__(self):
                return get_repr_info(
                    cls=self.__class__,
                    args=[
                        'b',
                        ('a', lambda: self.__a),
                    ]
                )

        with pytest.raises(TypeError):
            repr(Sumx(1, 2))
