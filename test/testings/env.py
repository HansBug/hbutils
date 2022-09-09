import os

GITHUB_HOST = os.environ.get('GITHUB_HOST', 'github.com')


def _has_github():
    return not os.environ.get('NO_GITHUB')
