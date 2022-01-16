import re

import pytest

from hbutils.encoding import base64_decode
from hbutils.random import random_digits, random_bin_digits, random_hex_digits, random_md5, random_sha1, \
    random_base64, random_md5_with_timestamp, random_sha1_with_timestamp


@pytest.mark.unittest
class TestRandomString:
    def test_random_digits(self):
        _DEC_PATTERN = re.compile('^[0-9]+$')
        for i in range(1000):
            assert _DEC_PATTERN.fullmatch(random_digits())

        with pytest.raises(ValueError):
            random_digits(base=1)
        with pytest.raises(ValueError):
            random_digits(base=100)
        with pytest.raises(TypeError):
            random_digits(base=8.3)

    def test_random_bin_digits(self):
        _BIN_PATTERN = re.compile('^[0-1]+$')
        for i in range(1000):
            assert _BIN_PATTERN.fullmatch(random_bin_digits())

    def test_random_hex_digits(self):
        _HEX_PATTERN = re.compile('^[0-9abcdef]+$')
        for i in range(1000):
            assert _HEX_PATTERN.fullmatch(random_hex_digits())

        _HEX_UPPER_PATTERN = re.compile('^[0-9ABCDEF]+$')
        for i in range(1000):
            assert _HEX_UPPER_PATTERN.fullmatch(random_hex_digits(upper=True))

    def test_random_md5(self):
        _MD5_PATTERN = re.compile('^[0-9abcdef]{32}$')
        for i in range(1000):
            assert _MD5_PATTERN.fullmatch(random_md5())

    def test_random_sha1(self):
        _SHA1_PATTERN = re.compile('^[0-9abcdef]{40}$')
        for i in range(1000):
            assert _SHA1_PATTERN.fullmatch(random_sha1())

    def test_random_base64(self):
        for i in range(1000):
            assert len(base64_decode(random_base64(), urlsafe=True)) == 64

        for i in range(1000):
            assert len(base64_decode(random_base64(233), urlsafe=True)) == 233

    def test_random_md5_with_timestamp(self):
        _MD5_TIMESTAMP_PATTERN = re.compile('^[0-9]{20}_[0-9abcdef]{32}$')
        for i in range(1000):
            assert _MD5_TIMESTAMP_PATTERN.fullmatch(random_md5_with_timestamp())

    def test_random_sha1_with_timestamp(self):
        _SHA1_TIMESTAMP_PATTERN = re.compile('^[0-9]{20}_[0-9abcdef]{40}$')
        for i in range(1000):
            assert _SHA1_TIMESTAMP_PATTERN.fullmatch(random_sha1_with_timestamp())
