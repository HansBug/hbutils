import logging
import os
from unittest.mock import patch, MagicMock

import pytest

from hbutils.logging import ColoredFormatter, ANSIColors, format_multiline_message


@pytest.fixture
def sample_log_record():
    return logging.LogRecord(
        name='test.logger',
        level=logging.INFO,
        pathname='/path/to/file.py',
        lineno=42,
        msg='Test message',
        args=(),
        exc_info=None
    )


@pytest.fixture
def multiline_log_record():
    return logging.LogRecord(
        name='test.logger',
        level=logging.WARNING,
        pathname='/path/to/file.py',
        lineno=42,
        msg='First line\nSecond line\nThird line',
        args=(),
        exc_info=None
    )


@pytest.fixture
def empty_message_record():
    return logging.LogRecord(
        name='test.logger',
        level=logging.DEBUG,
        pathname='/path/to/file.py',
        lineno=42,
        msg='',
        args=(),
        exc_info=None
    )


@pytest.fixture
def single_line_record():
    return logging.LogRecord(
        name='test.logger',
        level=logging.ERROR,
        pathname='/path/to/file.py',
        lineno=42,
        msg='Single line message',
        args=(),
        exc_info=None
    )


@pytest.fixture
def colored_formatter():
    return ColoredFormatter()


@pytest.fixture
def custom_datefmt_formatter():
    return ColoredFormatter(datefmt='%H:%M:%S')


@pytest.mark.unittest
class TestANSIColors:
    def test_ansi_colors_constants(self):
        # Test that all ANSI color constants are strings
        assert isinstance(ANSIColors.RESET, str)
        assert isinstance(ANSIColors.BOLD, str)
        assert isinstance(ANSIColors.UNDERLINE, str)
        assert isinstance(ANSIColors.BLACK, str)
        assert isinstance(ANSIColors.RED, str)
        assert isinstance(ANSIColors.GREEN, str)
        assert isinstance(ANSIColors.YELLOW, str)
        assert isinstance(ANSIColors.BLUE, str)
        assert isinstance(ANSIColors.MAGENTA, str)
        assert isinstance(ANSIColors.CYAN, str)
        assert isinstance(ANSIColors.WHITE, str)
        assert isinstance(ANSIColors.BRIGHT_BLACK, str)
        assert isinstance(ANSIColors.BRIGHT_RED, str)
        assert isinstance(ANSIColors.BRIGHT_GREEN, str)
        assert isinstance(ANSIColors.BRIGHT_YELLOW, str)
        assert isinstance(ANSIColors.BRIGHT_BLUE, str)
        assert isinstance(ANSIColors.BRIGHT_MAGENTA, str)
        assert isinstance(ANSIColors.BRIGHT_CYAN, str)
        assert isinstance(ANSIColors.BRIGHT_WHITE, str)

    def test_ansi_colors_values(self):
        # Test specific ANSI escape sequence values
        assert ANSIColors.RESET == "\033[0m"
        assert ANSIColors.BOLD == "\033[1m"
        assert ANSIColors.UNDERLINE == "\033[4m"
        assert ANSIColors.RED == "\033[31m"
        assert ANSIColors.GREEN == "\033[32m"
        assert ANSIColors.YELLOW == "\033[33m"
        assert ANSIColors.BLUE == "\033[34m"
        assert ANSIColors.BRIGHT_RED == "\033[91m"


@pytest.mark.unittest
class TestFormatMultilineMessage:
    def test_empty_message(self):
        result = format_multiline_message('', 4)
        assert result == ''

    def test_single_line_message(self):
        message = 'Single line'
        result = format_multiline_message(message, 4)
        assert result == 'Single line'

    def test_multiline_message_with_indent(self):
        message = 'First line\nSecond line\nThird line'
        result = format_multiline_message(message, 4)
        expected = f'First line{os.linesep}    Second line{os.linesep}    Third line'
        assert result == expected

    def test_multiline_message_zero_indent(self):
        message = 'First line\nSecond line'
        result = format_multiline_message(message, 0)
        expected = f'First line{os.linesep}Second line'
        assert result == expected

    def test_multiline_message_large_indent(self):
        message = 'Line 1\nLine 2'
        result = format_multiline_message(message, 10)
        expected = f'Line 1{os.linesep}          Line 2'
        assert result == expected

    def test_message_with_empty_lines(self):
        message = 'First\n\nThird'
        result = format_multiline_message(message, 2)
        expected = f'First{os.linesep}  {os.linesep}  Third'
        assert result == expected

    def test_message_ending_with_newline(self):
        message = 'First line\nSecond line\n'
        result = format_multiline_message(message, 4)
        expected = f'First line{os.linesep}    Second line'
        assert result == expected


@pytest.mark.unittest
class TestColoredFormatter:
    def test_init_default_datefmt(self, colored_formatter):
        assert colored_formatter.datefmt == '%Y-%m-%d %H:%M:%S'
        assert colored_formatter._indent_cache == {}

    def test_init_custom_datefmt(self, custom_datefmt_formatter):
        assert custom_datefmt_formatter.datefmt == '%H:%M:%S'

    def test_colors_mapping(self):
        expected_colors = {
            'DEBUG': ANSIColors.BLUE,
            'INFO': ANSIColors.GREEN,
            'WARNING': ANSIColors.YELLOW,
            'ERROR': ANSIColors.RED,
            'CRITICAL': ANSIColors.BOLD + ANSIColors.RED,
        }
        assert ColoredFormatter.COLORS == expected_colors

    def test_calculate_indent_length_caching(self, colored_formatter, sample_log_record):
        # First call should calculate and cache
        indent_length1 = colored_formatter._calculate_indent_length(sample_log_record)
        assert isinstance(indent_length1, int)
        assert indent_length1 > 0

        # Cache should contain the result
        cache_key = (sample_log_record.levelname, sample_log_record.name)
        assert cache_key in colored_formatter._indent_cache
        assert colored_formatter._indent_cache[cache_key] == indent_length1

        # Second call should use cached value
        indent_length2 = colored_formatter._calculate_indent_length(sample_log_record)
        assert indent_length2 == indent_length1

    def test_calculate_indent_length_different_records(self, colored_formatter):
        record1 = logging.LogRecord('logger1', logging.INFO, '', 0, 'msg', (), None)
        record2 = logging.LogRecord('logger2', logging.DEBUG, '', 0, 'msg', (), None)

        indent1 = colored_formatter._calculate_indent_length(record1)
        indent2 = colored_formatter._calculate_indent_length(record2)

        # Should have different cache entries
        assert len(colored_formatter._indent_cache) == 2
        assert ('INFO', 'logger1') in colored_formatter._indent_cache
        assert ('DEBUG', 'logger2') in colored_formatter._indent_cache

    @patch('logging.Formatter.format')
    @patch.object(ColoredFormatter, 'formatTime')
    def test_format_single_line(self, mock_format_time, mock_format, colored_formatter, single_line_record):
        mock_format_time.return_value = '2024-01-15 10:30:45'
        mock_format.return_value = 'formatted_output'

        result = colored_formatter.format(single_line_record)

        assert result == 'formatted_output'
        mock_format.assert_called_once()

    @patch('logging.Formatter.format')
    @patch.object(ColoredFormatter, 'formatTime')
    def test_format_multiline(self, mock_format_time, mock_format, colored_formatter, multiline_log_record):
        mock_format_time.return_value = '2024-01-15 10:30:45'
        mock_format.return_value = 'formatted_multiline_output'

        result = colored_formatter.format(multiline_log_record)

        assert result == 'formatted_multiline_output'
        mock_format.assert_called_once()

    @patch('logging.Formatter.format')
    @patch.object(ColoredFormatter, 'formatTime')
    def test_format_empty_message(self, mock_format_time, mock_format, colored_formatter, empty_message_record):
        mock_format_time.return_value = '2024-01-15 10:30:45'
        mock_format.return_value = 'formatted_empty_output'

        result = colored_formatter.format(empty_message_record)

        assert result == 'formatted_empty_output'
        mock_format.assert_called_once()

    def test_format_all_log_levels(self, colored_formatter):
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

        for level in levels:
            record = logging.LogRecord('test', level, '', 0, 'Test message', (), None)
            result = colored_formatter.format(record)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_format_unknown_log_level(self, colored_formatter):
        # Create a record with a custom log level
        record = logging.LogRecord('test', 25, '', 0, 'Custom level message', (), None)
        record.levelname = 'CUSTOM'

        result = colored_formatter.format(record)
        assert isinstance(result, str)
        assert len(result) > 0

    @patch('logging.makeLogRecord')
    @patch('logging.Formatter.format')
    @patch.object(ColoredFormatter, 'formatTime')
    def test_format_creates_record_copy(self, mock_format_time, mock_format, mock_make_log_record, colored_formatter,
                                        sample_log_record):
        mock_format_time.return_value = '2024-01-15 10:30:45'
        mock_format.return_value = 'formatted_output'
        mock_record_copy = MagicMock()
        mock_make_log_record.return_value = mock_record_copy

        colored_formatter.format(sample_log_record)

        # Verify that makeLogRecord was called with the original record's dict
        mock_make_log_record.assert_called_once_with(sample_log_record.__dict__)

        # Verify that the copy's msg and args were modified
        assert mock_record_copy.args is None

    def test_format_with_custom_datefmt(self, custom_datefmt_formatter, sample_log_record):
        result = custom_datefmt_formatter.format(sample_log_record)
        assert isinstance(result, str)
        assert len(result) > 0

    @patch.object(ColoredFormatter, '_calculate_indent_length')
    @patch('hbutils.logging.format.format_multiline_message')
    def test_format_calls_helper_functions(self, mock_format_multiline, mock_calc_indent, colored_formatter,
                                           sample_log_record):
        mock_calc_indent.return_value = 20
        mock_format_multiline.return_value = 'formatted message'

        colored_formatter.format(sample_log_record)

        mock_calc_indent.assert_called_once_with(sample_log_record)
        mock_format_multiline.assert_called_once_with('Test message', 20)

    def test_format_preserves_original_record(self, colored_formatter, sample_log_record):
        original_msg = sample_log_record.msg
        original_args = sample_log_record.args

        colored_formatter.format(sample_log_record)

        # Original record should be unchanged
        assert sample_log_record.msg == original_msg
        assert sample_log_record.args == original_args
