import os
import sys

import click
import pytest
from click.exceptions import ClickException

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


class _CustomClickException(ClickException):
    exit_code = 0x20


@pytest.fixture()
def cli1():
    @click.command('cli1', help='CLI-1 example', context_settings=CONTEXT_SETTINGS)
    @click.option('-c', type=int, help='optional C value', default=None, show_default=True)
    @click.argument('a', type=int)
    @click.argument('b', type=int)
    def cli1(a, b, c):
        if c is None:
            print(f'{a} + {b} = {a + b}')
        elif c < 0:
            raise ValueError('Uncaught value error', c)
        elif c > 1000:
            print('Well, well, well...')
            raise _CustomClickException(f'custom - {c!r}')
        elif os.environ.get('FAIL'):
            print('WTF?')
        else:
            print(f'{a} + {b} + {c} = {a + b + c}', file=sys.stderr)

    return cli1
