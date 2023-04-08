import pytest

from hbutils.system import urlsplit, SplitURL


@pytest.fixture()
def url_1():
    return 'https://www.baidu.com/dslkjf/sdfhk/asdasd.png?q=1&v=kdjf&q=2#fff'


@pytest.fixture()
def url_2():
    return 'http://api.baidu.com?q=1&v=kdjf&q=2&q=100&t'


@pytest.mark.unittest
class TestSystemNetworkUrl:
    def test_urlsplit_1(self, url_1):
        obj = urlsplit(url_1)
        assert isinstance(obj, SplitURL)
        assert obj.url == url_1
        assert obj.scheme == 'https'
        assert obj.host == 'www.baidu.com'
        assert obj.path == '/dslkjf/sdfhk/asdasd.png'
        assert obj.query == 'q=1&v=kdjf&q=2'
        assert obj.fragment == 'fff'

        assert obj.query_dict == {'q': ['1', '2'], 'v': 'kdjf'}
        assert obj.filename == 'asdasd.png'

        assert str(obj) == url_1
        assert repr(obj) == "SplitURL(scheme='https', host='www.baidu.com', path='/dslkjf/sdfhk/asdasd.png', " \
                            "query={'q': ['1', '2'], 'v': 'kdjf'}, fragment='fff')"

    def test_urlsplit_2(self, url_2):
        obj = urlsplit(url_2)
        assert isinstance(obj, SplitURL)
        assert obj.url == url_2
        assert obj.scheme == 'http'
        assert obj.host == 'api.baidu.com'
        assert obj.path == ''
        assert obj.query == 'q=1&v=kdjf&q=2&q=100&t'
        assert obj.fragment == ''

        assert obj.query_dict == {'q': ['1', '2', '100'], 't': None, 'v': 'kdjf'}
        assert obj.filename == ''

        assert str(obj) == url_2
        assert repr(obj) == "SplitURL(scheme='http', host='api.baidu.com', " \
                            "query={'q': ['1', '2', '100'], 'v': 'kdjf', 't': None})"
