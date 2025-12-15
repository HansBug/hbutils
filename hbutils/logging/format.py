"""
Overview:
    This module provides functionality to enhance logging output with colors for different log levels.
    It includes a `Colors` class defining ANSI escape sequences for various colors and styles,
    and a `ColoredFormatter` class to format log messages with these colors based on their severity level.
"""

# example:
# import logging
#
# from hbutils.logging import ColoredFormatter
#
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(ColoredFormatter())
# logger.addHandler(console_handler)
#
# # 测试多行消息
# logger.info("This is a single line message")
# logger.warning("This is a multi-line message:\nLine 2 content\nLine 3 content\nLine 4 content")
# logger.error(
#     "Error details:\n  - Error code: 500\n  - Error message: Internal server error\n  - Stack trace follows...")

import logging
import os

__all__ = [
    'ANSIColors',
    'ColoredFormatter',
]


class ANSIColors:
    """
    A collection of ANSI escape sequences for terminal text coloring and styling.
    These constants can be used to format strings with various colors and text styles.
    """
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def _format_multiline_message(message: str, indent_length: int):
    """
    Format a multi-line message with proper indentation.

    :param message: The message to format.
    :type message: str
    :param indent_length: The number of spaces to indent continuation lines.
    :type indent_length: int

    :return: The formatted message with proper indentation.
    :rtype: str
    """
    lines = message.splitlines(keepends=False)
    if len(lines) == 0:
        return ''

    # First line remains unchanged
    formatted_lines = [lines[0]]

    # Subsequent lines get indented
    indent = ' ' * indent_length
    for line in lines[1:]:
        formatted_lines.append(indent + line)

    return os.linesep.join(formatted_lines)


class ColoredFormatter(logging.Formatter):
    """
    A logging formatter that applies colors to log messages based on their severity level.

    The colors are defined in the `Colors` class and are applied to different parts of the log message
    such as the timestamp, log level, logger name, and the message itself.

    This formatter also supports multi-line messages with proper indentation alignment.
    """
    COLORS = {
        'DEBUG': ANSIColors.BLUE,
        'INFO': ANSIColors.GREEN,
        'WARNING': ANSIColors.YELLOW,
        'ERROR': ANSIColors.RED,
        'CRITICAL': ANSIColors.BOLD + ANSIColors.RED,
    }

    def __init__(self, datefmt: str = '%Y-%m-%d %H:%M:%S', *args, **kwargs):
        """
        Initialize the ColoredFormatter.

        :param args: Arguments passed to the parent Formatter class.
        :param kwargs: Keyword arguments passed to the parent Formatter class.
        """
        super().__init__(*args, **kwargs)
        self.datefmt = datefmt
        self._indent_cache = {}

    def _calculate_indent_length(self, record):
        """
        Calculate the length of the prefix (timestamp + level + name + separator) for indentation.

        :param record: The log record to be formatted.
        :type record: logging.LogRecord

        :return: The length of the prefix without ANSI color codes.
        :rtype: int
        """
        # Create a cache key based on level name and logger name
        cache_key = (record.levelname, record.name)

        if cache_key not in self._indent_cache:
            # Format timestamp part
            timestamp = self.formatTime(record, datefmt=self.datefmt)
            timestamp_part = f"[{timestamp}]"

            # Format level part (8 characters wide)
            level_part = f"{record.levelname:<8}"

            # Format logger name part
            name_part = f"{record.name}"

            # Calculate total length: [timestamp] + space + level + space + name + " "
            indent_length = len(timestamp_part) + 1 + len(level_part) + 1 + len(name_part) + 1
            self._indent_cache[cache_key] = indent_length

        return self._indent_cache[cache_key]

    def format(self, record):
        """
        Format the specified record as text, applying color based on the log level.
        Multi-line messages are properly indented to align with the message content.

        :param record: The log record to be formatted.
        :type record: logging.LogRecord

        :return: The formatted log message with appropriate colors and proper multi-line indentation.
        :rtype: str
        """
        log_color = self.COLORS.get(record.levelname, ANSIColors.RESET)

        # Build the format string
        format_str = f"{ANSIColors.BRIGHT_BLACK}[%(asctime)s]{ANSIColors.RESET} "
        format_str += f"{log_color}%(levelname)-8s{ANSIColors.RESET} "
        format_str += f"{ANSIColors.CYAN}%(name)s{ANSIColors.RESET} "
        format_str += f"%(message)s"

        # Calculate indent length for multi-line messages
        indent_length = self._calculate_indent_length(record)

        # Format multi-line message with proper indentation
        original_message = record.getMessage()
        formatted_message = _format_multiline_message(original_message, indent_length)

        # Create a new record with the formatted message
        record_copy = logging.makeLogRecord(record.__dict__)
        record_copy.msg = formatted_message
        record_copy.args = None  # Clear args since we've already formatted the message

        formatter = logging.Formatter(format_str, datefmt=self.datefmt)
        return formatter.format(record_copy)
