import pytest

from hbutils.system import is_binary_file, is_text_file
from ...testings import get_testfile_path


@pytest.mark.unittest
class TestSystemFilesystemBinary:
    @pytest.mark.parametrize(
        ['file', 'is_binary'],
        [
            ('igm/zip_template-simple.zip', True),
            ('igm/rar_template-simple.rar', True),
            ('igm/xztar_template-simple.tar.xz', True),
            ('igm/LICENSE', False),
            ('igm/README.md', False),
            ('chinese.txt', False),
            ('english.txt', False),
            ('japanese.txt', False),
            ('korean.txt', False),
            ('russian.txt', False),
            ('empty', False),
        ]
    )
    def test_is_binary_file(self, file, is_binary):
        assert is_binary_file(get_testfile_path(file)) == is_binary

    @pytest.mark.parametrize(
        ['file', 'is_text'],
        [
            ('igm/zip_template-simple.zip', False),
            ('igm/rar_template-simple.rar', False),
            ('igm/xztar_template-simple.tar.xz', False),
            ('igm/LICENSE', True),
            ('igm/README.md', True),
            ('chinese.txt', True),
            ('english.txt', True),
            ('japanese.txt', True),
            ('korean.txt', True),
            ('russian.txt', True),
            ('empty', True),
        ]
    )
    def test_is_text_file(self, file, is_text):
        assert is_text_file(get_testfile_path(file)) == is_text
