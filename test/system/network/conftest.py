import os
import subprocess
import sys
import urllib.request
from contextlib import contextmanager
from http.client import HTTPException
from urllib.error import URLError

import pytest


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
                    urllib.request.urlopen(f'http://127.0.0.1:{port}', timeout=0.2)
                except (URLError, HTTPException):
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
