import os

GITHUB_HOST = os.environ.get('GITHUB_HOST', 'github.com')


def _has_github():
    return not os.environ.get('NO_GITHUB')


if _has_github():
    TEMPLATE_SIMPLE_REPO_GIT = f'git+https://{GITHUB_HOST}/igm4ai/template-simple.git'
else:
    TEMPLATE_SIMPLE_REPO_GIT = f'git+https://gitee.com/igm4ai/template-simple.git'
