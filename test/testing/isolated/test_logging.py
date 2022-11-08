import logging
import pathlib
import sys

import pytest

from hbutils.testing import isolated_logger, capture_output, isolated_directory


@pytest.mark.unittest
class TestTestingIsolatedLogging:
    def test_isolated_logger(self):
        with capture_output() as co1:
            logging.error('this is error')
            logging.error('this is error')

        assert not co1.stdout.strip()
        assert not co1.stderr.strip()

        with isolated_directory():
            with capture_output() as co2:
                with isolated_logger(handlers=[
                    logging.StreamHandler(),
                    logging.StreamHandler(stream=sys.stdout),
                    logging.FileHandler('log.txt'),
                ]):
                    logging.error('this is error inside 1')
                    logging.error('this is error inside 2')

            assert 'this is error inside 1' in co2.stdout.strip()
            assert 'this is error inside 2' in co2.stderr.strip()
            assert 'this is error inside 1' in pathlib.Path('log.txt').read_text().strip()

        with capture_output() as co3:
            logging.error('this is error')
            logging.error('this is error')

        assert not co3.stdout.strip()
        assert not co3.stderr.strip()
