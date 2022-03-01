import pytest

from hbutils.model import raw_support


@pytest.mark.unittest
class TestModelRaw:
    def test_raw_support(self):
        raw, unraw, RawProxy = raw_support(lambda x: isinstance(x, dict))
        assert raw(1) == 1
        assert raw([1, 2]) == [1, 2]
        rd = raw({'a': 1})
        assert isinstance(rd, RawProxy)
        assert rd == RawProxy({'a': 1})
        assert rd.value == {'a': 1}

        assert unraw(1) == 1
        assert unraw([1, 2]) == [1, 2]
        assert unraw(rd) == {'a': 1}

        assert raw.__name__ == 'raw'
        assert unraw.__name__ == 'unraw'
        assert RawProxy.__name__ == 'RawProxy'

    def test_raw_support_with_rename(self):
        raw, unraw, RawProxy = raw_support(lambda x: isinstance(x, dict), 'raw_dict', 'unraw_dict', '_DictProxy')
        assert raw(1) == 1
        assert raw([1, 2]) == [1, 2]
        rd = raw({'a': 1})
        assert isinstance(rd, RawProxy)
        assert rd == RawProxy({'a': 1})
        assert rd.value == {'a': 1}

        assert unraw(1) == 1
        assert unraw([1, 2]) == [1, 2]
        assert unraw(rd) == {'a': 1}

        assert raw.__name__ == 'raw_dict'
        assert unraw.__name__ == 'unraw_dict'
        assert RawProxy.__name__ == '_DictProxy'
