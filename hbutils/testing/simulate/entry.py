"""
Overview:
    Simulation for CLI entry points. This module provides utilities to simulate the execution
    of command-line interface (CLI) entry functions in a controlled environment, capturing
    their output, exit codes, and exceptions for testing purposes.
"""
import io
import traceback
from contextlib import contextmanager
from functools import partial
from typing import Optional, List, Callable, Mapping, ContextManager
from unittest.mock import patch

from ..capture import capture_output, capture_exit

__all__ = [
    'simulate_entry', 'EntryRunResult',
]


class EntryRunResult:
    """
    Overview:
        Run result of one entry. This class encapsulates the results of executing a CLI entry
        function, including exit code, stdout/stderr output, and any uncaught exceptions.
    """

    def __init__(self, exitcode: int, stdout: Optional[str], stderr: Optional[str], error: Optional[BaseException]):
        """
        Constructor of :class:`EntryRunResult`.

        :param exitcode: Exit code returned by the entry function.
        :type exitcode: int
        :param stdout: Output captured from standard output stream.
        :type stdout: Optional[str]
        :param stderr: Output captured from standard error stream.
        :type stderr: Optional[str]
        :param error: Uncaught exception raised inside the entry function.
        :type error: Optional[BaseException]
        """
        self.__exitcode = exitcode
        self.__stdout = stdout
        self.__stderr = stderr
        self.__error = error

    @property
    def exitcode(self) -> int:
        """
        Exit code returned by the entry function.

        :return: The exit code value.
        :rtype: int
        """
        return self.__exitcode

    @property
    def stdout(self) -> Optional[str]:
        """
        Output captured from standard output stream.

        :return: The stdout content, or None if no output was captured.
        :rtype: Optional[str]
        """
        return self.__stdout

    @property
    def stderr(self) -> Optional[str]:
        """
        Output captured from standard error stream.

        :return: The stderr content, or None if no output was captured.
        :rtype: Optional[str]
        """
        return self.__stderr

    @property
    def error(self) -> Optional[BaseException]:
        """
        Uncaught exception raised inside the entry function.

        :return: The exception object, or None if no exception was raised.
        :rtype: Optional[BaseException]
        """
        return self.__error

    def _assert_okay_message(self) -> str:
        """
        Generate a detailed error message for assertion failures.

        :return: Formatted error message containing exit code, exception details, and output streams.
        :rtype: str
        """
        with io.StringIO() as sf:
            pp = partial(print, file=sf)
            if self.error is not None:
                pp(f'Exitcode - {self.exitcode!r}, with uncaught exception:')
                traceback.print_tb(self.error.__traceback__, file=sf)
                pp(f'{type(self.error)}: {self.error.args!r}')
            else:
                pp(f'Exitcode - {self.exitcode!r}.')

            if self.stdout:
                pp(f'---------------------------------')
                pp(f'[Stdout]')
                pp(self.stdout)
                pp()

            if self.stderr:
                pp(f'---------------------------------')
                pp(f'[Stderr]')
                pp(self.stderr)
                pp()

            return sf.getvalue()

    def assert_okay(self):
        """
        Assert that the entry execution was successful.

        Checks that the exit code is 0 and no uncaught exception was raised.
        If the assertion fails, a detailed error message is displayed.

        :raises AssertionError: If the exit code is not 0 or an exception was raised.

        Example::
            >>> result = simulate_entry(my_cli_function, ['mycli', 'arg1'])
            >>> result.assert_okay()  # Raises AssertionError if execution failed
        """
        assert self.exitcode == 0 and self.error is None, self._assert_okay_message()


# See: https://stackoverflow.com/questions/36136480/what-is-pythons-default-exit-code
_OKAY_EXITCODE = 0x0
_ERROR_EXITCODE = 0x1
_USAGE_EXITCODE = 0x2


@contextmanager
def _mock_argv(argv: Optional[List[str]] = None) -> ContextManager:
    """
    Context manager to mock sys.argv.

    :param argv: Command line arguments to mock. If None, sys.argv is not mocked.
    :type argv: Optional[List[str]]
    :return: Context manager for mocking sys.argv.
    :rtype: ContextManager
    :yields: None

    Example::
        >>> with _mock_argv(['script.py', 'arg1', 'arg2']):
        ...     print(sys.argv)
        ['script.py', 'arg1', 'arg2']
    """
    if argv is not None:
        with patch('sys.argv', argv):
            yield
    else:
        yield


@contextmanager
def _mock_environ(envs: Optional[Mapping[str, str]] = None) -> ContextManager:
    """
    Context manager to mock os.environ.

    :param envs: Environment variables to mock. If None, os.environ is not mocked.
    :type envs: Optional[Mapping[str, str]]
    :return: Context manager for mocking os.environ.
    :rtype: ContextManager
    :yields: None

    Example::
        >>> with _mock_environ({'MY_VAR': 'value'}):
        ...     print(os.environ['MY_VAR'])
        value
    """
    if envs is not None:
        with patch.dict('os.environ', envs, clear=False):
            yield
    else:
        yield


def simulate_entry(entry: Callable, argv: Optional[List[str]] = None,
                   envs: Optional[Mapping[str, str]] = None) -> EntryRunResult:
    """
    Overview:
        CLI entry's simulation. Executes a CLI entry function in a controlled environment,
        capturing its output, exit code, and any exceptions for testing purposes.

    :param entry: Entry function, should be a simple function without any arguments.
    :type entry: Callable
    :param argv: Command line arguments. Default is ``None``, which means do not mock ``sys.argv``.
    :type argv: Optional[List[str]]
    :param envs: Environment arguments. Default is ``None``, which means do not mock ``os.environ``.
    :type envs: Optional[Mapping[str, str]]
    :return: A result object containing exit code, stdout, stderr, and error information.
    :rtype: EntryRunResult

    Examples::
        We create a simple CLI code with `click package <https://click.palletsprojects.com/>`_, \
            named ``test_cli1.py``

        .. code-block:: python
           :linenos:

            import sys
            import click

            @click.command('cli1', help='CLI-1 example')
            @click.option('-c', type=int, help='optional C value', default=None)
            @click.argument('a', type=int)
            @click.argument('b', type=int)
            def cli1(a, b, c):
                if c is None:
                    print(f'{a} + {b} = {a + b}')
                else:
                    print(f'{a} + {b} + {c} = {a + b + c}', file=sys.stderr)

            if __name__ == '__main__':
                cli1()

        When we can try to simulate it.

            >>> from hbutils.testing import simulate_entry
            >>> from test_cli1 import cli1
            >>> r1 = simulate_entry(cli1, ['cli1', '2', '3'])
            >>> print(r1.exitcode)
            0
            >>> print(r1.stdout)
            2 + 3 = 5

            >>> r2 = simulate_entry(cli1, ['cli1', '2', '3', '-c', '24'])  # option
            >>> print(r2.exitcode)
            0
            >>> print(r2.stderr)
            2 + 3 + 24 = 29

            >>> r3 = simulate_entry(cli1, ['cli', '--help'])  # help
            >>> print(r3.stdout)
            Usage: cli [OPTIONS] A B
              CLI-1 example
            Options:
              -c INTEGER  optional C value
              --help      Show this message and exit.

            >>> r4 = simulate_entry(cli1, ['cli', 'dklsfj'])  # misusage
            >>> print(r4.exitcode)
            2
            >>> print(r4.stderr)
            Usage: cli [OPTIONS] A B
            Try 'cli --help' for help.
            Error: Invalid value for 'A': 'dklsfj' is not a valid integer.

        .. note::
            Please note that if there is uncaught exception raised inside the entry function, \
                it will be caught and put into ``error`` property instead of being printed \
                to ``stderr``. For example

            >>> from hbutils.testing import simulate_entry
            >>> def my_cli():
            ...     raise ValueError(233)
            >>>
            >>> r = simulate_entry(my_cli)
            >>> print(r.exitcode)  # will be 0x1
            1
            >>> print(r.stdout)  # nothing
            >>> print(r.stderr)  # nothing as well
            >>> print(repr(r.error))  # HERE!!!
            ValueError(233)
    """
    try:
        with capture_output() as _out, capture_exit(_OKAY_EXITCODE) as _exit, \
                _mock_argv(argv), _mock_environ(envs):
            entry()
    except BaseException as err:
        return EntryRunResult(_ERROR_EXITCODE, _out.stdout, _out.stderr, err)
    else:
        return EntryRunResult(_exit.exitcode, _out.stdout, _out.stderr, None)
