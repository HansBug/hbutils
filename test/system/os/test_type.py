from hbutils.system import is_windows, is_darwin, is_macos, is_linux
from ...testings import linux_mark, windows_mark, macos_mark


class TestSystemOsType:
    @linux_mark
    def test_is_linux(self):
        assert is_linux()
        assert not is_windows()
        assert not is_macos()
        assert not is_darwin()

    @windows_mark
    def test_is_windows(self):
        assert not is_linux()
        assert is_windows()
        assert not is_macos()
        assert not is_darwin()

    @macos_mark
    def test_is_macos(self):
        assert not is_linux()
        assert not is_windows()
        assert is_macos()
        assert is_darwin()
