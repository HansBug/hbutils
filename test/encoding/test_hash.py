import pytest

from hbutils.encoding import md5, sha1, sha224, sha256, sha384, sha512, sha3


@pytest.mark.unittest
class TestEncodingHash:
    def test_md5(self):
        assert md5(b'') == 'd41d8cd98f00b204e9800998ecf8427e'
        assert md5(b'this is a word') == 'cdfc9527f76e296c76cdb331ac2d1d88'

    def test_sha1(self):
        assert sha1(b'') == 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
        assert sha1(b'this is a word') == '7bf417a6503e185ea6352525b96a4d6ef3b9609b'

    def test_sha224(self):
        assert sha224(b'') == 'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f'
        assert sha224(b'this is a word') == '7b994bcffbc9a3689941e541a2e639c20e321b763b744c0d84f6899c'

    def test_sha256(self):
        assert sha256(b'') == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        assert sha256(b'this is a word') == '91ccca153f5d3739af1f0d304d033f193b25208d44d371c1304877a6503471bf'

    def test_sha384(self):
        assert sha384(b'') == '38b060a751ac96384cd9327eb1b1e36a21fdb71114be074' \
                              '34c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b'
        assert sha384(b'this is a word') == '37ae885a635d78e9067fdfe297e2d50d70de3670e4066bd541ac2' \
                                            '59b3ecdffb39a4c7b97211cb3967eac2188bb4b95f6'

    def test_sha512(self):
        assert sha512(b'') == 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a' \
                              '921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'
        assert sha512(b'this is a word') == '6e80a2fd5dcf382b443ddaa619833208a4f4ac9bbedb760d6c8aac26a12da8' \
                                            'dc6e2f6bc809091915db2e2d19bb66682db89e46c646a8ea7a5c6da57bf1a42b5c'

    def test_sha3(self):
        assert sha3(b'') == 'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a'
        assert sha3(b'this is a word') == '3e5a3507f625c8464fb282b451c8d82d78c3a232645e55c846d55551a7fe667c'
        assert sha3(b'', n=224) == '6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7'
        assert sha3(b'this is a word', n=224) == 'e0271d2734fc2c1a6dfcb6051bec6dc59e5f7fbec4b0d42ef1faee64'
