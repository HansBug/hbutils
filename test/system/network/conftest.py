import os
import subprocess
import sys
from contextlib import contextmanager
from urllib.error import URLError

import pytest
import requests
from requests.exceptions import RequestException


@contextmanager
def start_http_server(port, silent: bool = True):
    with open(os.devnull, 'w') as nullfile:
        process = None
        try:
            process = subprocess.Popen(
                [sys.executable, '-m', 'http.server', str(port)],
                stdin=sys.stdin if not silent else None,
                stdout=sys.stdout if not silent else nullfile,
                stderr=sys.stderr if not silent else nullfile,
            )
            while True:
                try:
                    resp = requests.head(f'http://127.0.0.1:{port}', timeout=0.2)
                    resp.raise_for_status()
                except (URLError, RequestException, ConnectionError):
                    continue
                else:
                    break

            yield

        finally:
            if process is not None:
                process.kill()
                process.wait()


@pytest.fixture(scope='session', autouse=True)
def start_http_server_on_35127_and_35128():
    with start_http_server(35127), start_http_server(35128):
        yield
