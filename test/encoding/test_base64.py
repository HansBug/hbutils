import pytest

from hbutils.encoding import base64_encode, base64_decode


@pytest.mark.unittest
class TestEncodingBase64:
    def test_base64(self):
        assert base64_encode(b'kjsdfhguioldsfhgipuhofjisghldkfjvg') == \
               'a2pzZGZoZ3Vpb2xkc2ZoZ2lwdWhvZmppc2dobGRrZmp2Zw=='
        assert base64_decode('a2pzZGZoZ3Vpb2xkc2ZoZ2lwdWhvZmppc2dobGRrZmp2Zw==') == \
               b'kjsdfhguioldsfhgipuhofjisghldkfjvg'

    def test_urlsafe_base64(self):
        assert base64_encode(b'kjsdfhguioldsfhgipuhofjisghldkfjvg', urlsafe=True) == \
               'a2pzZGZoZ3Vpb2xkc2ZoZ2lwdWhvZmppc2dobGRrZmp2Zw=='
        assert base64_decode('a2pzZGZoZ3Vpb2xkc2ZoZ2lwdWhvZmppc2dobGRrZmp2Zw==', urlsafe=True) == \
               b'kjsdfhguioldsfhgipuhofjisghldkfjvg'

        with pytest.warns(UserWarning):
            assert base64_encode(b'kjsdfhguioldsfhgipuhofjisghldkfjvg', altchars=b'++', urlsafe=True) == \
                   'a2pzZGZoZ3Vpb2xkc2ZoZ2lwdWhvZmppc2dobGRrZmp2Zw=='
        with pytest.warns(UserWarning):
            assert base64_decode('a2pzZGZoZ3Vpb2xkc2ZoZ2lwdWhvZmppc2dobGRrZmp2Zw==', altchars=b'++', urlsafe=True) == \
                   b'kjsdfhguioldsfhgipuhofjisghldkfjvg'
