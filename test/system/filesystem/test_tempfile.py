import os.path
import pathlib

import pytest

from hbutils.system import TemporaryDirectory


@pytest.mark.unittest
class TestSystemFilesystemTempfile:
    def test_tempfile_directory(self):
        with TemporaryDirectory() as td:
            assert os.path.exists(td)
            with open(os.path.join(td, 'f.txt'), 'w') as f:
                f.write('233')

            assert pathlib.Path(os.path.join(td, 'f.txt')).read_text() == '233'

            os.makedirs(os.path.join(td, '1', '2', 'ksdjf'), exist_ok=True)
            with open(os.path.join(td, '1', '2', 'ksdjf', 'ttt.txt'), 'w') as f:
                f.write('dsjfieursjf9per8ghsperdg')
            assert pathlib.Path(os.path.join(td, '1', '2', 'ksdjf', 'ttt.txt')).read_text() == \
                   'dsjfieursjf9per8ghsperdg'

        assert not os.path.exists(td)
