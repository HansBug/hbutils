from unittest.mock import patch

import pytest

from hbutils.testing import simulate_entry


@pytest.mark.unittest
class TestTestingSimulateEntry:
    def test_simulate_entry_cli1(self, cli1):
        result = simulate_entry(cli1, ['cli1', '2', '3'])
        result.assert_okay()
        assert result.stdout.strip() == '2 + 3 = 5'
        assert not result.stderr.strip()

    def test_simulate_entry_cli1_misuse(self, cli1):
        result = simulate_entry(cli1, ['cli1', '2', 'd'])
        with pytest.raises(AssertionError):
            result.assert_okay()
        assert result.exitcode == 2
        assert result.error is None
        assert not result.stdout.strip()
        assert '\'d\' is not a valid integer' in result.stderr.strip()

    def test_simulate_entry_cli1_uncaught(self, cli1):
        result = simulate_entry(cli1, ['cli1', '2', '3', '-c', '-10'])
        with pytest.raises(AssertionError):
            result.assert_okay()
        assert result.exitcode == 1
        assert isinstance(result.error, ValueError)
        assert result.error.args == ('Uncaught value error', -10)
        assert not result.stdout.strip()
        assert not result.stderr.strip()

    def test_simulate_entry_cli1_normal_exit(self, cli1):
        result = simulate_entry(cli1, ['cli1', '2', '3', '-c', '2000'])
        with pytest.raises(AssertionError):
            result.assert_okay()
        assert result.exitcode == 0x20
        assert result.error is None
        assert result.stdout.strip() == 'Well, well, well...'
        assert result.stderr.strip() == 'Error: custom - 2000'

    def test_simulate_entry_cli_in_stderr(self, cli1):
        result = simulate_entry(cli1, ['cli1', '2', '3', '-c', '24'])
        result.assert_okay()
        assert not result.stdout.strip()
        assert result.stderr.strip() == '2 + 3 + 24 = 29'

    def test_simulate_entry_cli_with_env(self, cli1):
        result = simulate_entry(cli1, ['cli1', '2', '3', '-c', '24'], envs={'FAIL': '1'})
        result.assert_okay()
        assert result.stdout.strip() == 'WTF?'
        assert not result.stderr.strip()

    def test_simulate_entry_cli_help(self, cli1):
        result = simulate_entry(cli1, ['cli1', '-h'])
        result.assert_okay()
        assert 'CLI-1 example' in result.stdout.strip()
        assert not result.stderr.strip()

    def test_simulate_entry_without_args(self, cli1):
        with patch('sys.argv', ['cli1', '-h']):
            result = simulate_entry(cli1)
            result.assert_okay()
            assert 'CLI-1 example' in result.stdout.strip()
            assert not result.stderr.strip()
